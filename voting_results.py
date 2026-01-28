#!/usr/bin/env python3
"""
Voting Results Dashboard
Real-time voting results and analytics with password protection
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
import json
import hashlib
import os
from voting_system import voting_system
from database_manager import db
from security_utils import verify_password_bcrypt, encrypt_file_to_zip, differential_privacy_count

# Password protection configuration
PASSWORD_FILE = "voting_results_password.txt"
DEFAULT_PASSWORD = "admin123"  # Default password (will be hashed)

class PasswordManager:
    """Manages password authentication for voting results"""

    def __init__(self):
        self.password_file = PASSWORD_FILE
        self.ensure_password_file_exists()

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def ensure_password_file_exists(self):
        """Create password file with default password if it doesn't exist"""
        if not os.path.exists(self.password_file):
            hashed_default = self.hash_password(DEFAULT_PASSWORD)
            with open(self.password_file, 'w') as f:
                f.write(hashed_default)

    def verify_password(self, password):
        """Verify if the provided password is correct"""
        try:
            with open(self.password_file, 'r') as f:
                stored_hash = f.read().strip()
            return self.hash_password(password) == stored_hash
        except Exception:
            return False

    def change_password(self, old_password, new_password):
        """Change the password if old password is correct"""
        if self.verify_password(old_password):
            hashed_new = self.hash_password(new_password)
            with open(self.password_file, 'w') as f:
                f.write(hashed_new)
            return True
        return False

# Global password manager instance
password_manager = PasswordManager()

def show_rbac_auth_dialog(parent=None):
    """Authenticate using RBAC users table with optional TOTP. Returns user dict or None."""
    auth_window = tk.Toplevel(parent) if parent else tk.Tk()
    auth_window.title("🔒 User Authentication")
    auth_window.geometry("420x380")
    auth_window.configure(bg='#1a1a2e')
    auth_window.resizable(False, False)

    if parent:
        auth_window.transient(parent)
        auth_window.grab_set()

    result = {'user': None}

    header = tk.Label(auth_window, text="Sign in to continue", font=('Segoe UI', 14, 'bold'), fg='white', bg='#1a1a2e')
    header.pack(pady=12)

    frame = tk.Frame(auth_window, bg='#2d2d44', relief='solid', bd=1)
    frame.pack(fill=tk.X, padx=20, pady=10)

    tk.Label(frame, text="Username", font=('Segoe UI', 11, 'bold'), fg='white', bg='#2d2d44').pack(pady=(12, 4))
    username_entry = tk.Entry(frame, font=('Segoe UI', 12), width=28, justify='center')
    username_entry.pack(pady=(0, 8))
    username_entry.focus()

    tk.Label(frame, text="Password", font=('Segoe UI', 11, 'bold'), fg='white', bg='#2d2d44').pack(pady=(6, 4))
    password_entry = tk.Entry(frame, font=('Segoe UI', 12), width=28, show='*', justify='center')
    password_entry.pack(pady=(0, 8))

    tk.Label(frame, text="TOTP (if enabled)", font=('Segoe UI', 11, 'bold'), fg='white', bg='#2d2d44').pack(pady=(6, 4))
    totp_entry = tk.Entry(frame, font=('Segoe UI', 12), width=28, justify='center')
    totp_entry.pack(pady=(0, 12))

    error_label = tk.Label(auth_window, text="", font=('Segoe UI', 10), fg='#f44336', bg='#1a1a2e')
    error_label.pack()

    def authenticate_user():
        username = username_entry.get().strip()
        password = password_entry.get()
        token = totp_entry.get().strip()
        if not username or not password:
            error_label.config(text="❌ Enter username and password")
            return
        user = db.get_user(username)
        if not user:
            error_label.config(text="❌ Invalid credentials")
            return
        # Verify password (support both DB-generated PBKDF2 and legacy/bcrypt)
        verified = False
        try:
            # Try DB's native verification first (handles pbkdf2_sha256$)
            if db.verify_password_with_pbkdf2(password, user['password_hash']):
                verified = True
        except AttributeError:
            # If db instance doesn't have the method or static access issue
             pass
             
        if not verified:
             if verify_password_bcrypt(password, user['password_hash']):
                 verified = True
                 
        if not verified:
            error_label.config(text="❌ Invalid credentials")
            return
        
        # If TOTP is configured, require valid token
        if user.get('totp_secret'):
            try:
                import pyotp
                totp = pyotp.TOTP(user['totp_secret'])
                if not token or not totp.verify(token, valid_window=1):
                    error_label.config(text="❌ Invalid TOTP token")
                    return
            except Exception:
                error_label.config(text="❌ TOTP verification error")
                return
        result['user'] = user
        auth_window.destroy()

    buttons = tk.Frame(auth_window, bg='#1a1a2e')
    buttons.pack(fill=tk.X, padx=20, pady=12)

    tk.Button(buttons, text="🔓 Sign In", command=authenticate_user, font=('Segoe UI', 12, 'bold'), fg='white', bg='#4CAF50', relief='flat', padx=20, pady=8).pack(side=tk.LEFT)
    tk.Button(buttons, text="❌ Cancel", command=auth_window.destroy, font=('Segoe UI', 12, 'bold'), fg='white', bg='#f44336', relief='flat', padx=20, pady=8).pack(side=tk.RIGHT)

    auth_window.bind('<Return>', lambda event: authenticate_user())
    auth_window.wait_window()
    return result['user']

def show_password_dialog(parent=None):
    """Show password authentication dialog"""

    # Create password dialog window
    password_window = tk.Toplevel(parent) if parent else tk.Tk()
    password_window.title("🔒 Authentication Required")
    password_window.geometry("400x300")
    password_window.configure(bg='#1a1a2e')
    password_window.resizable(False, False)

    # Center the window
    password_window.transient(parent)
    password_window.grab_set()

    # Result variable
    authentication_result = {'success': False}

    # Header
    header_frame = tk.Frame(password_window, bg='#1a1a2e')
    header_frame.pack(fill=tk.X, padx=20, pady=20)

    title_label = tk.Label(header_frame,
                          text="🔒 SECURE ACCESS REQUIRED",
                          font=('Segoe UI', 16, 'bold'),
                          fg='white', bg='#1a1a2e')
    title_label.pack()

    subtitle_label = tk.Label(header_frame,
                             text="Enter password to view voting results",
                             font=('Segoe UI', 12),
                             fg='#CCCCCC', bg='#1a1a2e')
    subtitle_label.pack(pady=(5, 0))

    # Input frame
    input_frame = tk.Frame(password_window, bg='#2d2d44', relief='solid', bd=1)
    input_frame.pack(fill=tk.X, padx=20, pady=20)

    tk.Label(input_frame,
             text="Password:",
             font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#2d2d44').pack(pady=(15, 5))

    password_entry = tk.Entry(input_frame,
                             font=('Segoe UI', 12),
                             width=25,
                             show='*',
                             justify='center')
    password_entry.pack(pady=(0, 15))
    password_entry.focus()

    # Error label
    error_label = tk.Label(password_window,
                          text="",
                          font=('Segoe UI', 10),
                          fg='#f44336', bg='#1a1a2e')
    error_label.pack()

    def authenticate():
        password = password_entry.get()
        if password_manager.verify_password(password):
            authentication_result['success'] = True
            password_window.destroy()
        else:
            error_label.config(text="❌ Incorrect password. Please try again.")
            password_entry.delete(0, tk.END)
            password_entry.focus()

    def cancel_auth():
        password_window.destroy()

    # Buttons frame
    buttons_frame = tk.Frame(password_window, bg='#1a1a2e')
    buttons_frame.pack(fill=tk.X, padx=20, pady=20)

    # Login button
    login_btn = tk.Button(buttons_frame,
                         text="🔓 Login",
                         command=authenticate,
                         font=('Segoe UI', 12, 'bold'),
                         fg='white', bg='#4CAF50',
                         relief='flat', padx=20, pady=10)
    login_btn.pack(side=tk.LEFT, padx=(0, 10))

    # Cancel button
    cancel_btn = tk.Button(buttons_frame,
                          text="❌ Cancel",
                          command=cancel_auth,
                          font=('Segoe UI', 12, 'bold'),
                          fg='white', bg='#f44336',
                          relief='flat', padx=20, pady=10)
    cancel_btn.pack(side=tk.RIGHT)

    # Change password button
    def show_change_password():
        show_change_password_dialog(password_window)

    change_pwd_btn = tk.Button(buttons_frame,
                              text="🔑 Change Password",
                              command=show_change_password,
                              font=('Segoe UI', 10),
                              fg='white', bg='#2196F3',
                              relief='flat', padx=15, pady=8)
    change_pwd_btn.pack()

    # Bind Enter key to authenticate
    password_entry.bind('<Return>', lambda event: authenticate())

    # Info label
    info_label = tk.Label(password_window,
                         text="Default password: admin123\n(Change it for security)",
                         font=('Segoe UI', 9),
                         fg='#888888', bg='#1a1a2e',
                         justify=tk.CENTER)
    info_label.pack(pady=(10, 0))

    # Wait for window to close
    password_window.wait_window()

    return authentication_result['success']

def show_change_password_dialog(parent=None):
    """Show change password dialog"""

    change_window = tk.Toplevel(parent) if parent else tk.Tk()
    change_window.title("🔑 Change Password")
    change_window.geometry("400x350")
    change_window.configure(bg='#1a1a2e')
    change_window.resizable(False, False)

    if parent:
        change_window.transient(parent)
        change_window.grab_set()

    # Header
    header_label = tk.Label(change_window,
                           text="🔑 CHANGE PASSWORD",
                           font=('Segoe UI', 16, 'bold'),
                           fg='white', bg='#1a1a2e')
    header_label.pack(pady=20)

    # Input frame
    input_frame = tk.Frame(change_window, bg='#2d2d44', relief='solid', bd=1)
    input_frame.pack(fill=tk.X, padx=20, pady=20)

    # Current password
    tk.Label(input_frame,
             text="Current Password:",
             font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#2d2d44').pack(pady=(15, 5))

    current_password_entry = tk.Entry(input_frame,
                                     font=('Segoe UI', 12),
                                     width=25,
                                     show='*',
                                     justify='center')
    current_password_entry.pack(pady=(0, 10))
    current_password_entry.focus()

    # New password
    tk.Label(input_frame,
             text="New Password:",
             font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#2d2d44').pack(pady=(5, 5))

    new_password_entry = tk.Entry(input_frame,
                                 font=('Segoe UI', 12),
                                 width=25,
                                 show='*',
                                 justify='center')
    new_password_entry.pack(pady=(0, 10))

    # Confirm password
    tk.Label(input_frame,
             text="Confirm New Password:",
             font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#2d2d44').pack(pady=(5, 5))

    confirm_password_entry = tk.Entry(input_frame,
                                     font=('Segoe UI', 12),
                                     width=25,
                                     show='*',
                                     justify='center')
    confirm_password_entry.pack(pady=(0, 15))

    # Status label
    status_label = tk.Label(change_window,
                           text="",
                           font=('Segoe UI', 10),
                           fg='#f44336', bg='#1a1a2e')
    status_label.pack()

    def change_password():
        current_pwd = current_password_entry.get()
        new_pwd = new_password_entry.get()
        confirm_pwd = confirm_password_entry.get()

        if not current_pwd or not new_pwd or not confirm_pwd:
            status_label.config(text="❌ Please fill all fields", fg='#f44336')
            return

        if new_pwd != confirm_pwd:
            status_label.config(text="❌ New passwords don't match", fg='#f44336')
            return

        if len(new_pwd) < 6:
            status_label.config(text="❌ Password must be at least 6 characters", fg='#f44336')
            return

        if password_manager.change_password(current_pwd, new_pwd):
            status_label.config(text="✅ Password changed successfully!", fg='#4CAF50')
            change_window.after(2000, change_window.destroy)
        else:
            status_label.config(text="❌ Current password is incorrect", fg='#f44336')

    # Buttons
    buttons_frame = tk.Frame(change_window, bg='#1a1a2e')
    buttons_frame.pack(fill=tk.X, padx=20, pady=20)

    change_btn = tk.Button(buttons_frame,
                          text="🔑 Change Password",
                          command=change_password,
                          font=('Segoe UI', 12, 'bold'),
                          fg='white', bg='#4CAF50',
                          relief='flat', padx=20, pady=10)
    change_btn.pack(side=tk.LEFT, padx=(0, 10))

    cancel_btn = tk.Button(buttons_frame,
                          text="❌ Cancel",
                          command=change_window.destroy,
                          font=('Segoe UI', 12, 'bold'),
                          fg='white', bg='#f44336',
                          relief='flat', padx=20, pady=10)
    cancel_btn.pack(side=tk.RIGHT)

def show_voting_results():
    """Show comprehensive voting results dashboard with password protection"""

    # First, authenticate the user (RBAC). Fallback to legacy password if no users exist.
    user = show_rbac_auth_dialog()
    if not user:
        # Optionally fallback
        try:
            # If users table empty, allow legacy password
            from database_manager import db as _db
            if not _db.get_user('admin'):
                if not show_password_dialog():
                    return
            else:
                return
        except Exception:
            return

    # Create results window
    results_window = tk.Toplevel()
    results_window.title("🗳️ Voting Results Dashboard")
    results_window.geometry("1200x800")
    results_window.configure(bg='#1a1a2e')
    
    # Get voting results
    results_data = voting_system.get_voting_results()
    
    # Header
    header_frame = tk.Frame(results_window, bg='#1a1a2e')
    header_frame.pack(fill=tk.X, padx=20, pady=20)
    
    title_label = tk.Label(header_frame,
                          text="🗳️ VOTING RESULTS DASHBOARD",
                          font=('Segoe UI', 20, 'bold'),
                          fg='white', bg='#1a1a2e')
    title_label.pack()
    
    # Summary stats (with optional DP noise)
    stats_frame = tk.Frame(results_window, bg='#2d2d44', relief='solid', bd=1)
    stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    stats_container = tk.Frame(stats_frame, bg='#2d2d44')
    stats_container.pack(pady=15)
    
    # Total votes
    noisy_total = int(differential_privacy_count(results_data['total_votes']))
    total_votes_label = tk.Label(stats_container,
                                text="📊 Total Votes (DP): {}".format(noisy_total),
                                font=('Segoe UI', 14, 'bold'),
                                fg='#4CAF50', bg='#2d2d44')
    total_votes_label.pack(side=tk.LEFT, padx=20)

    # Total voters
    noisy_voters = int(differential_privacy_count(results_data['total_voters']))
    total_voters_label = tk.Label(stats_container,
                                 text="👥 Total Voters (DP): {}".format(noisy_voters),
                                 font=('Segoe UI', 14, 'bold'),
                                 fg='#2196F3', bg='#2d2d44')
    total_voters_label.pack(side=tk.LEFT, padx=20)

    # Turnout percentage (assuming 108 registered voters)
    turnout = (results_data['total_voters'] / 108) * 100 if results_data['total_voters'] > 0 else 0
    turnout_label = tk.Label(stats_container,
                            text="📈 Turnout: {:.1f}%".format(turnout),
                            font=('Segoe UI', 14, 'bold'),
                            fg='#FF9800', bg='#2d2d44')
    turnout_label.pack(side=tk.LEFT, padx=20)

    # Last updated
    updated_label = tk.Label(stats_container,
                            text="🕒 Updated: {}".format(datetime.now().strftime('%H:%M:%S')),
                            font=('Segoe UI', 12),
                            fg='#CCCCCC', bg='#2d2d44')
    updated_label.pack(side=tk.RIGHT, padx=20)

    # WINNER ANNOUNCEMENT SECTION - NEW FEATURE
    if results_data['total_votes'] > 0:
        # Find the winning party (highest votes)
        winning_party = max(results_data['results'], key=lambda x: x['votes'])

        # Check if there's a clear winner (not a tie)
        max_votes = winning_party['votes']
        parties_with_max_votes = [p for p in results_data['results'] if p['votes'] == max_votes]

        # Winner announcement frame
        winner_frame = tk.Frame(results_window, bg='#1a1a2e')
        winner_frame.pack(fill=tk.X, padx=20, pady=(10, 0))

        # Winner container with special styling
        winner_container = tk.Frame(winner_frame, bg='#4CAF50', relief='solid', bd=3)
        winner_container.pack(fill=tk.X, pady=10)

        if len(parties_with_max_votes) == 1 and max_votes > 0:
            # Clear winner
            winner_title = tk.Label(winner_container,
                                  text="🏆 ELECTION WINNER 🏆",
                                  font=('Segoe UI', 18, 'bold'),
                                  fg='white', bg='#4CAF50')
            winner_title.pack(pady=(15, 5))

            winner_party = tk.Label(winner_container,
                                  text="{} {}".format(winning_party['symbol'], winning_party['party']),
                                  font=('Segoe UI', 24, 'bold'),
                                  fg='white', bg='#4CAF50')
            winner_party.pack(pady=5)

            winner_stats = tk.Label(winner_container,
                                  text="{} votes ({:.1f}% of total votes)".format(
                                      winning_party['votes'],
                                      winning_party['percentage']),
                                  font=('Segoe UI', 14),
                                  fg='white', bg='#4CAF50')
            winner_stats.pack(pady=(5, 15))

        elif len(parties_with_max_votes) > 1 and max_votes > 0:
            # Tie situation
            winner_container.configure(bg='#FF9800')  # Orange for tie

            tie_title = tk.Label(winner_container,
                               text="🤝 ELECTION TIE 🤝",
                               font=('Segoe UI', 18, 'bold'),
                               fg='white', bg='#FF9800')
            tie_title.pack(pady=(15, 5))

            tie_parties_text = " & ".join(["{} {}".format(p['symbol'], p['party']) for p in parties_with_max_votes])
            tie_parties = tk.Label(winner_container,
                                 text=tie_parties_text,
                                 font=('Segoe UI', 20, 'bold'),
                                 fg='white', bg='#FF9800')
            tie_parties.pack(pady=5)

            tie_stats = tk.Label(winner_container,
                               text="Each with {} votes ({:.1f}% of total votes)".format(
                                   max_votes,
                                   (max_votes / results_data['total_votes']) * 100),
                               font=('Segoe UI', 14),
                               fg='white', bg='#FF9800')
            tie_stats.pack(pady=(5, 15))

        else:
            # No votes cast yet
            winner_container.configure(bg='#607D8B')  # Gray for no votes

            no_votes_title = tk.Label(winner_container,
                                    text="📊 NO VOTES CAST YET",
                                    font=('Segoe UI', 18, 'bold'),
                                    fg='white', bg='#607D8B')
            no_votes_title.pack(pady=(15, 5))

            no_votes_msg = tk.Label(winner_container,
                                  text="Start voting to see election results!",
                                  font=('Segoe UI', 14),
                                  fg='white', bg='#607D8B')
            no_votes_msg.pack(pady=(5, 15))
    
    # Main content frame
    content_frame = tk.Frame(results_window, bg='#1a1a2e')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    # Left side - Results table
    left_frame = tk.Frame(content_frame, bg='#1a1a2e')
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    # Results table
    table_label = tk.Label(left_frame,
                          text="📋 DETAILED RESULTS",
                          font=('Segoe UI', 16, 'bold'),
                          fg='white', bg='#1a1a2e')
    table_label.pack(pady=(0, 10))
    
    # Create table frame
    table_frame = tk.Frame(left_frame, bg='#2d2d44', relief='solid', bd=1)
    table_frame.pack(fill=tk.BOTH, expand=True)
    
    # Table headers
    headers_frame = tk.Frame(table_frame, bg='#3d3d54')
    headers_frame.pack(fill=tk.X, padx=2, pady=2)
    
    tk.Label(headers_frame, text="Party", font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#3d3d54', width=20).pack(side=tk.LEFT, padx=5, pady=8)
    tk.Label(headers_frame, text="Votes", font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#3d3d54', width=10).pack(side=tk.LEFT, padx=5, pady=8)
    tk.Label(headers_frame, text="Percentage", font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#3d3d54', width=12).pack(side=tk.LEFT, padx=5, pady=8)
    tk.Label(headers_frame, text="Bar", font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#3d3d54', width=20).pack(side=tk.LEFT, padx=5, pady=8)
    
    # Scrollable results
    results_canvas = tk.Canvas(table_frame, bg='#2d2d44', highlightthickness=0)
    results_scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=results_canvas.yview)
    results_scrollable = tk.Frame(results_canvas, bg='#2d2d44')
    
    results_scrollable.bind(
        "<Configure>",
        lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
    )
    
    results_canvas.create_window((0, 0), window=results_scrollable, anchor="nw")
    results_canvas.configure(yscrollcommand=results_scrollbar.set)
    
    results_canvas.pack(side="left", fill="both", expand=True)
    results_scrollbar.pack(side="right", fill="y")
    
    # Add results rows
    for i, result in enumerate(results_data['results']):
        row_bg = '#2d2d44' if i % 2 == 0 else '#3d3d54'
        
        row_frame = tk.Frame(results_scrollable, bg=row_bg)
        row_frame.pack(fill=tk.X, padx=2, pady=1)
        
        # Party name with symbol
        party_label = tk.Label(row_frame,
                              text="{} {}".format(result['symbol'], result['party']),
                              font=('Segoe UI', 11),
                              fg='white', bg=row_bg, width=20, anchor='w')
        party_label.pack(side=tk.LEFT, padx=5, pady=5)

        # Vote count
        votes_label = tk.Label(row_frame,
                              text=str(result['votes']),
                              font=('Segoe UI', 11, 'bold'),
                              fg='#4CAF50', bg=row_bg, width=10)
        votes_label.pack(side=tk.LEFT, padx=5, pady=5)

        # Percentage
        percentage_label = tk.Label(row_frame,
                                   text="{:.1f}%".format(result['percentage']),
                                   font=('Segoe UI', 11),
                                   fg='#2196F3', bg=row_bg, width=12)
        percentage_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Progress bar
        bar_frame = tk.Frame(row_frame, bg=row_bg, width=200, height=20)
        bar_frame.pack(side=tk.LEFT, padx=5, pady=5)
        bar_frame.pack_propagate(False)
        
        if results_data['total_votes'] > 0:
            bar_width = int((result['percentage'] / 100) * 180)
            if bar_width > 0:
                bar_canvas = tk.Canvas(bar_frame, bg=row_bg, highlightthickness=0, width=200, height=20)
                bar_canvas.pack()
                bar_canvas.create_rectangle(0, 2, bar_width, 18, fill=result['color'], outline="")
                bar_canvas.create_text(90, 10, text="{:.1f}%".format(result['percentage']),
                                     fill='white', font=('Segoe UI', 8, 'bold'))
    
    # Right side - Chart
    right_frame = tk.Frame(content_frame, bg='#1a1a2e')
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    chart_label = tk.Label(right_frame,
                          text="📊 VISUAL RESULTS",
                          font=('Segoe UI', 16, 'bold'),
                          fg='white', bg='#1a1a2e')
    chart_label.pack(pady=(0, 10))
    
    # Create chart
    if results_data['total_votes'] > 0:
        # Prepare data for chart
        parties = [r['party'] for r in results_data['results'] if r['votes'] > 0]
        votes = [r['votes'] for r in results_data['results'] if r['votes'] > 0]
        colors = [r['color'] for r in results_data['results'] if r['votes'] > 0]
        
        if parties:  # Only create chart if there are votes
            # Create matplotlib figure
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
            fig.patch.set_facecolor('#1a1a2e')
            
            # Pie chart
            ax1.pie(votes, labels=parties, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Vote Distribution', color='white', fontsize=14, fontweight='bold')
            ax1.set_facecolor('#1a1a2e')
            
            # Bar chart
            bars = ax2.bar(parties, votes, color=colors)
            ax2.set_title('Vote Counts', color='white', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Political Parties', color='white')
            ax2.set_ylabel('Number of Votes', color='white')
            ax2.set_facecolor('#1a1a2e')
            ax2.tick_params(colors='white')
            
            # Rotate x-axis labels for better readability
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        '{}'.format(int(height)), ha='center', va='bottom', color='white')
            
            plt.tight_layout()
            
            # Embed chart in tkinter
            chart_canvas = FigureCanvasTkAgg(fig, right_frame)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            # No votes yet
            no_votes_label = tk.Label(right_frame,
                                     text="📊 No votes cast yet\n\nStart voting to see results!",
                                     font=('Segoe UI', 14),
                                     fg='#888888', bg='#1a1a2e',
                                     justify=tk.CENTER)
            no_votes_label.pack(expand=True)
    else:
        # No votes yet
        no_votes_label = tk.Label(right_frame,
                                 text="📊 No votes cast yet\n\nStart voting to see results!",
                                 font=('Segoe UI', 14),
                                 fg='#888888', bg='#1a1a2e',
                                 justify=tk.CENTER)
        no_votes_label.pack(expand=True)
    
    # Bottom buttons
    buttons_frame = tk.Frame(results_window, bg='#1a1a2e')
    buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    # Refresh button
    def refresh_results():
        results_window.destroy()
        show_voting_results()
    
    refresh_btn = tk.Button(buttons_frame,
                           text="🔄 Refresh Results",
                           command=refresh_results,
                           font=('Segoe UI', 12, 'bold'),
                           fg='white', bg='#4CAF50',
                           relief='flat', padx=20, pady=10)
    refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    # Export results button (admin only)
    def export_results():
        try:
            filename = voting_system.export_results()
            # Secure export: wrap file in encrypted archive
            export_enc = encrypt_file_to_zip([filename], 'voting_results_export.zip', password='ChangeMe!')
            try:
                db.write_audit_log(actor_username=user['username'], action='export_results', resource=export_enc, details={'source': filename})
            except Exception:
                pass
            messagebox.showinfo("Export Successful",
                              "Encrypted export created: {}".format(export_enc))
        except Exception as e:
            messagebox.showerror("Export Error", "Failed to export results: {}".format(str(e)))
    
    export_btn = tk.Button(buttons_frame,
                          text="📄 Export Results",
                          command=export_results,
                          font=('Segoe UI', 12, 'bold'),
                          fg='white', bg='#2196F3',
                          relief='flat', padx=20, pady=10)
    export_btn.pack(side=tk.LEFT, padx=(0, 10))
    # Disable export for non-admins
    try:
        if user.get('role') != 'admin':
            export_btn.configure(state='disabled', bg='#3a6f8f')
    except Exception:
        pass

    # Password management button
    def manage_password():
        show_change_password_dialog(results_window)

    password_btn = tk.Button(buttons_frame,
                            text="🔑 Manage Password",
                            command=manage_password,
                            font=('Segoe UI', 12, 'bold'),
                            fg='white', bg='#9C27B0',
                            relief='flat', padx=20, pady=10)
    password_btn.pack(side=tk.LEFT, padx=(0, 10))

    # Audit open event
    try:
        db.write_audit_log(actor_username=user['username'], action='view_results', resource='dashboard', details={'total_votes': results_data['total_votes']})
    except Exception:
        pass

    # Close button
    close_btn = tk.Button(buttons_frame,
                         text="❌ Close",
                         command=results_window.destroy,
                         font=('Segoe UI', 12, 'bold'),
                         fg='white', bg='#f44336',
                         relief='flat', padx=20, pady=10)
    close_btn.pack(side=tk.RIGHT)

def show_individual_vote_lookup():
    """Show interface to lookup individual votes with password protection"""

    # First, authenticate the user
    if not show_password_dialog():
        # Authentication failed or cancelled
        return

    lookup_window = tk.Toplevel()
    lookup_window.title("🔍 Individual Vote Lookup")
    lookup_window.geometry("500x400")
    lookup_window.configure(bg='#1a1a2e')
    
    # Header
    header_label = tk.Label(lookup_window,
                           text="🔍 INDIVIDUAL VOTE LOOKUP",
                           font=('Segoe UI', 16, 'bold'),
                           fg='white', bg='#1a1a2e')
    header_label.pack(pady=20)
    
    # Input frame
    input_frame = tk.Frame(lookup_window, bg='#2d2d44', relief='solid', bd=1)
    input_frame.pack(fill=tk.X, padx=20, pady=20)
    
    tk.Label(input_frame,
             text="Enter Person ID:",
             font=('Segoe UI', 12),
             fg='white', bg='#2d2d44').pack(pady=(15, 5))
    
    person_id_entry = tk.Entry(input_frame,
                              font=('Segoe UI', 12),
                              width=20,
                              justify='center')
    person_id_entry.pack(pady=(0, 15))
    
    # Results frame
    results_frame = tk.Frame(lookup_window, bg='#1a1a2e')
    results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    def lookup_vote():
        try:
            person_id = int(person_id_entry.get())
            vote_info = voting_system.get_vote_by_person(person_id)
            
            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            if vote_info:
                # Show vote information
                info_frame = tk.Frame(results_frame, bg='#2d2d44', relief='solid', bd=1)
                info_frame.pack(fill=tk.X, pady=10)
                
                tk.Label(info_frame,
                         text="✅ Vote Found for Person {}".format(person_id),
                         font=('Segoe UI', 14, 'bold'),
                         fg='#4CAF50', bg='#2d2d44').pack(pady=10)

                tk.Label(info_frame,
                         text="Party: {} {}".format(vote_info['symbol'], vote_info['party']),
                         font=('Segoe UI', 12),
                         fg='white', bg='#2d2d44').pack(pady=2)

                tk.Label(info_frame,
                         text="Time: {}".format(vote_info['timestamp']),
                         font=('Segoe UI', 12),
                         fg='white', bg='#2d2d44').pack(pady=2)

                tk.Label(info_frame,
                         text="Confidence: {:.1%}".format(vote_info['confidence']),
                         font=('Segoe UI', 12),
                         fg='white', bg='#2d2d44').pack(pady=(2, 10))
            else:
                # No vote found
                tk.Label(results_frame,
                         text="❌ No vote found for Person {}".format(person_id),
                         font=('Segoe UI', 14),
                         fg='#f44336', bg='#1a1a2e').pack(pady=20)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid Person ID (number)")
        except Exception as e:
            messagebox.showerror("Lookup Error", "Error looking up vote: {}".format(str(e)))
    
    # Lookup button
    lookup_btn = tk.Button(input_frame,
                          text="🔍 Lookup Vote",
                          command=lookup_vote,
                          font=('Segoe UI', 12, 'bold'),
                          fg='white', bg='#2196F3',
                          relief='flat', padx=20, pady=8)
    lookup_btn.pack(pady=(0, 15))
    
    # Close button
    close_btn = tk.Button(lookup_window,
                         text="❌ Close",
                         command=lookup_window.destroy,
                         font=('Segoe UI', 12, 'bold'),
                         fg='white', bg='#f44336',
                         relief='flat', padx=20, pady=10)
    close_btn.pack(pady=20)

if __name__ == "__main__":
    # Test the results dashboard
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    show_voting_results()
    
    root.mainloop()
