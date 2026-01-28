"""
Audit logging system with tamper-evident JSON Lines (JSONL) logs.

Features:
- Append-only JSONL logs
- HMAC-SHA256 hash chain for tamper evidence
- Automatic log directory creation
- Simple verification helper

Usage:
    from audit_system import AuditLogger
    logger = AuditLogger()
    logger.log_event('vote_cast_attempt', {'person_id': 1, 'party_id': 2})
"""

import os
import json
import hmac
import hashlib
import threading
from datetime import datetime
from typing import Optional, Dict, Any, Tuple


class AuditLogger:
    """Thread-safe, tamper-evident audit logger."""

    def __init__(self,
                 log_dir: str = 'logs',
                 log_filename: str = 'audit.log.jsonl',
                 secret_env_var: str = 'AUDIT_LOG_SECRET'):
        self.log_dir = log_dir
        self.log_path = os.path.join(log_dir, log_filename)
        self.secret_env_var = secret_env_var
        self._lock = threading.Lock()
        self._ensure_log_dir()
        self._secret = self._load_or_create_secret()

    def _ensure_log_dir(self) -> None:
        try:
            os.makedirs(self.log_dir, exist_ok=True)
        except Exception:
            pass

    def _secret_file_path(self) -> str:
        return os.path.join(self.log_dir, '.audit_secret')

    def _load_or_create_secret(self) -> bytes:
        env_secret = os.environ.get(self.secret_env_var)
        if env_secret:
            return hashlib.sha256(env_secret.encode('utf-8')).digest()

        secret_path = self._secret_file_path()
        try:
            if os.path.exists(secret_path):
                with open(secret_path, 'rb') as f:
                    data = f.read()
                if data:
                    return hashlib.sha256(data).digest()
        except Exception:
            pass

        # Create a new random secret and persist it locally
        try:
            random_bytes = os.urandom(32)
            with open(secret_path, 'wb') as f:
                f.write(random_bytes)
            return hashlib.sha256(random_bytes).digest()
        except Exception:
            # Fallback to a process-random secret (not persisted)
            return hashlib.sha256(os.urandom(32)).digest()

    def _read_last_hash(self) -> str:
        try:
            if not os.path.exists(self.log_path):
                return ''
            with open(self.log_path, 'rb') as f:
                # Read last non-empty line efficiently
                f.seek(0, os.SEEK_END)
                position = f.tell()
                buffer = bytearray()
                while position:
                    position -= 1
                    f.seek(position)
                    byte = f.read(1)
                    if byte == b'\n' and buffer:
                        break
                    buffer.extend(byte)
                if not buffer:
                    return ''
                last_line = bytes(reversed(buffer)).decode('utf-8').strip()
                if not last_line:
                    return ''
                obj = json.loads(last_line)
                return obj.get('chain_hash', '')
        except Exception:
            return ''

    def _compute_chain_hash(self, payload: Dict[str, Any], prev_hash: str) -> str:
        msg = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
        data = prev_hash.encode('utf-8') + b'|' + msg
        mac = hmac.new(self._secret, data, hashlib.sha256).hexdigest()
        return mac

    def log_event(self, event_type: str, details: Optional[Dict[str, Any]] = None) -> None:
        record = {
            'timestamp': datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            'event': event_type,
            'details': details or {}
        }
        with self._lock:
            prev_hash = self._read_last_hash()
            chain_hash = self._compute_chain_hash(record, prev_hash)
            record['prev_hash'] = prev_hash
            record['chain_hash'] = chain_hash
            try:
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
            except Exception:
                # Best-effort logging; ignore failures to avoid breaking main flow
                pass

    def verify_chain(self) -> Tuple[bool, int]:
        """Verify the entire log chain. Returns (is_valid, checked_records)."""
        try:
            if not os.path.exists(self.log_path):
                return True, 0
            prev = ''
            count = 0
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    record = {k: obj[k] for k in ('timestamp', 'event', 'details') if k in obj}
                    expected = self._compute_chain_hash(record, prev)
                    if expected != obj.get('chain_hash') or prev != obj.get('prev_hash'):
                        return False, count
                    prev = obj.get('chain_hash', '')
                    count += 1
            return True, count
        except Exception:
            return False, 0


# Create a default module-level logger for convenience
default_audit_logger = AuditLogger()



