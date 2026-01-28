import os
import sys

# Ensure project root is on sys.path when executed from scripts/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database_manager import db
from security_utils import hash_password_bcrypt, generate_totp_secret

def main():
    username = 'admin'
    user = db.get_user(username)
    if not user:
        password = 'ChangeMeNow!'
        pwd_hash = hash_password_bcrypt(password)
        secret = generate_totp_secret()
        db.create_user(username=username, password_hash=pwd_hash, role='admin', display_name='Administrator', totp_secret=secret)
        print('CREATED', username, password, secret)
    else:
        print('EXISTS', username, user.get('totp_secret'))

if __name__ == '__main__':
    main()


