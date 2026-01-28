import os
import sys

# Ensure project root on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database_manager import db

def main():
    username = 'admin'
    user = db.get_user(username)
    if not user or not user.get('totp_secret'):
        print('ERROR No user/secret')
        return
    secret = user['totp_secret']
    issuer = 'IrisSystem'
    label = f'{issuer}:{username}'
    uri = f'otpauth://totp/{label}?secret={secret}&issuer={issuer}&digits=6&period=30&algorithm=SHA1'

    try:
        import qrcode
        img = qrcode.make(uri)
        out_path = os.path.join(PROJECT_ROOT, 'admin_totp_qr.png')
        img.save(out_path)
        print('OK', out_path)
    except Exception as e:
        print('ERROR', str(e))

if __name__ == '__main__':
    main()



