
import os
import sys

# Ensure project root is on sys.path
sys.path.append(os.getcwd())

from database_manager import db
from security_utils import hash_password_bcrypt

def reset_admin():
    username = 'admin'
    password = 'admin123'
    
    # Check if user exists
    user = db.get_user(username)
    
    pwd_hash = hash_password_bcrypt(password)
    
    if user:
        print(f"Updating existing '{username}' user...")
        res = db.update_user_password(username, pwd_hash)
        db.set_user_role(username, 'admin')
        print(f"Admin password updated to: {password}")
    else:
        print(f"Creating new '{username}' user...")
        db.create_user(username=username, password_hash=pwd_hash, role='admin', display_name='System Admin')
        print(f"Created admin user. Login: {username} / {password}")

if __name__ == "__main__":
    try:
        reset_admin()
    except Exception as e:
        print(f"Error: {e}")
