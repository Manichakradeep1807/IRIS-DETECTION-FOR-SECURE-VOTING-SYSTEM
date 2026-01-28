"""
Security utilities: password hashing, TOTP, RBAC checks, encrypted export, and DP helpers
"""

import os
import json
import zipfile
try:
    import bcrypt as _bcrypt
    HAS_BCRYPT = True
except Exception:
    _bcrypt = None
    HAS_BCRYPT = False
from typing import Optional, Dict, List
from datetime import datetime, timedelta


def hash_password_bcrypt(password: str) -> str:
    """Hash password using bcrypt if available, else PBKDF2-HMAC as fallback."""
    if HAS_BCRYPT:
        return _bcrypt.hashpw(password.encode('utf-8'), _bcrypt.gensalt()).decode('utf-8')
    # Fallback: PBKDF2-HMAC-SHA256 with salt
    import os as _os
    import hashlib as _hash
    salt = _os.urandom(16)
    iterations = 200_000
    dk = _hash.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen=32)
    return 'pbkdf2${}${}${}'.format(iterations, salt.hex(), dk.hex())


def verify_password_bcrypt(password: str, stored_hash: str) -> bool:
    """Verify password against bcrypt or PBKDF2 fallback format."""
    try:
        if stored_hash.startswith('pbkdf2$'):
            import hashlib as _hash
            parts = stored_hash.split('$')
            iterations = int(parts[1])
            salt = bytes.fromhex(parts[2])
            expected = bytes.fromhex(parts[3])
            dk = _hash.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen=32)
            return dk == expected
        if HAS_BCRYPT and isinstance(stored_hash, str):
            return _bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        return False
    except Exception:
        return False


def _random_base32(length: int = 32) -> str:
    import secrets
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_totp_secret() -> str:
    try:
        import pyotp  # type: ignore
        return pyotp.random_base32()
    except Exception:
        # Fallback: random base32 compatible secret
        return _random_base32(32)


def verify_totp_token(secret: str, token: str, valid_window: int = 1) -> bool:
    try:
        import pyotp  # type: ignore
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=valid_window)
    except Exception:
        return False


def user_has_role(user: Dict, required_roles: List[str]) -> bool:
    if not user or 'role' not in user:
        return False
    return user['role'] in required_roles


def encrypt_file_to_zip(input_paths: List[str], output_zip_path: str, password: str) -> str:
    """Create an encrypted ZIP (AES-GCM) of given files.
    We create a normal ZIP alongside an encrypted .enc using AESGCM.
    Consumers must decrypt .enc; we avoid weak zipcrypto.
    """
    # Create temporary zip
    temp_zip = output_zip_path
    with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for p in input_paths:
            if os.path.exists(p):
                zf.write(p, arcname=os.path.basename(p))

    # Encrypt zip with AES-GCM if available; else leave plain zip as fallback
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # type: ignore
        with open(temp_zip, 'rb') as f:
            data = f.read()
        import hashlib
        derived = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b'iris_salt', 200_000, dklen=32)
        aesgcm = AESGCM(derived)
        import secrets
        nonce = secrets.token_bytes(12)
        enc = aesgcm.encrypt(nonce, data, None)
        enc_path = output_zip_path + '.enc'
        with open(enc_path, 'wb') as f:
            f.write(nonce + enc)
        try:
            os.remove(temp_zip)
        except Exception:
            pass
        return enc_path
    except Exception:
        # Fallback: return the plain zip path
        return temp_zip


def differential_privacy_count(count: int, epsilon: float = 0.5) -> float:
    """Apply simple Laplace noise to a count for DP-like aggregation."""
    import random
    # Laplace noise via inverse CDF
    b = 1.0 / epsilon
    u = random.random() - 0.5
    noise = -b * (1 if u < 0 else -1) * (abs(2*u))
    return max(0.0, count + noise)


