import os
import sys
import subprocess
import tkinter as tk

# Ensure project root on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from auth_ui import show_admin_login, show_user_login
from admin_biometric import verify_admin_iris


def main():
    root = tk.Tk()
    root.title("Login Portal")
    root.geometry("300x180")
    root.configure(bg="#1a1a2e")
    
    frm = tk.Frame(root, bg="#1a1a2e")
    frm.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    tk.Label(frm, text="Select Login Type", font=("Segoe UI", 14, "bold"), 
             fg="white", bg="#1a1a2e").pack(pady=10)
    
    def on_admin_success(user):
        root.destroy()
        subprocess.Popen([sys.executable, os.path.join(PROJECT_ROOT, 'Main_final_cleaned.py')])
    
    def on_user_success(user):
        root.destroy()
        subprocess.Popen([sys.executable, os.path.join(PROJECT_ROOT, 'Main_final_cleaned.py')])
    
    def admin_login():
        show_admin_login(on_admin_success, verify_admin_iris)
    
    def user_login():
        show_user_login(on_user_success)
    
    tk.Button(frm, text="Admin Login", command=admin_login, 
              fg='white', bg='#4CAF50', width=20, font=("Segoe UI", 11)).pack(pady=8)
    tk.Button(frm, text="User Login", command=user_login, 
              fg='white', bg='#2196F3', width=20, font=("Segoe UI", 11)).pack(pady=8)
    
    root.mainloop()


if __name__ == '__main__':
    main()
