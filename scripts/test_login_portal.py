import os
import sys
import tkinter as tk

# Ensure project root is on sys.path when executed from scripts/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from auth_ui import show_admin_login, show_user_login
from admin_biometric import verify_admin_iris
from database_manager import db


def main():
    root = tk.Tk()
    root.title("Login Portal Test")
    root.geometry("300x180")
    frm = tk.Frame(root); frm.pack(expand=True)

    def on_admin():
        show_admin_login(lambda u: print("ADMIN OK", u['username']), verify_admin_iris)
    def on_user():
        show_user_login(lambda u: print("USER OK", u['username']))

    tk.Button(frm, text="Admin Login", command=on_admin).pack(pady=8)
    tk.Button(frm, text="User Login", command=on_user).pack(pady=8)
    root.mainloop()

if __name__ == '__main__':
    main()


