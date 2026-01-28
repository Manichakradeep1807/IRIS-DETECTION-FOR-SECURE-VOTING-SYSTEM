
import os
import sys

# Ensure project root is on sys.path
sys.path.append(os.getcwd())

from database_manager import db
from security_utils import hash_password_bcrypt

def reset_admin_final():
    username = 'admin'
    password = 'admin123'
    
    # Generate BCRYPT hash
    pwd_hash = hash_password_bcrypt(password)
    
    user = db.get_user(username)
    if user:
        print(f"Updating existing '{username}' user with direct hash...")
        # Use our new method to update EXACT hash without re-hashing
        db.update_user_password_hash(username, pwd_hash)
        
        # Ensure correct role
        db.set_user_role(username, 'admin')
        print(f"Admin password (bcrypt) updated.")
    else:
        print(f"Creating new '{username}' user...")
        db.create_user(username=username, password_hash=pwd_hash, role='admin', display_name='System Admin')
        print(f"Created admin user.")

if __name__ == "__main__":
    try:
        reset_admin_final()
    except Exception as e:
        print(f"Error: {e}")
