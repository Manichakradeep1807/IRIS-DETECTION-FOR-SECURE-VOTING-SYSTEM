import os
import shutil

ROOT_DIR = os.getcwd()

def restore_file(filename):
    src = os.path.join(ROOT_DIR, 'documentation', filename)
    dst = os.path.join(ROOT_DIR, filename)
    if os.path.exists(src):
        try:
            shutil.move(src, dst)
            print(f"Restored {filename} to root.")
        except Exception as e:
            print(f"Error restoring {filename}: {e}")
    else:
        print(f"File not found in documentation: {filename}")

def create_gitignore():
    content = """
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env

# Database (Sensitive Data)
*.db
*.sqlite3
voting_results_password.txt

# Biometric Data
captured_iris/
temp_iris_*.jpg
dataset/
testSamples/
sample_dataset/

# Logs and Receipts
logs/
receipts/
*.log
*.json

# VS Code
.vscode/

# Archive
dev_archive/

# OS
.DS_Store
Thumbs.db
"""
    with open(".gitignore", "w") as f:
        f.write(content.strip())
    print("\nCreated .gitignore file.")

if __name__ == "__main__":
    # Restore critical files that might have been moved
    restore_file("README.md")
    restore_file("voting_results_password.txt") 
    restore_file("voting.txt") # Maybe?
    
    # Create Git config
    create_gitignore()
    print("\nProject is ready for Git upload.")
