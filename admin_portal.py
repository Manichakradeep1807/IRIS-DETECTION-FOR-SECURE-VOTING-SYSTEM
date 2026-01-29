import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import sys
import os
import json
from datetime import datetime

# Import Theme
try:
    from theme_manager import theme_manager
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False

# Import Database
try:
    from database_manager import db
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    
try:
    import cv2
    import numpy as np
    from biometric_utils import capture_face_vector_from_camera
except ImportError:
    pass

try:
    from voting_system import voting_system
except ImportError:
    pass

class AdminPortal:
    def __init__(self, root, admin_data, logout_callback=None):
        self.root = root
        self.admin_data = admin_data
        self.logout_callback = logout_callback
        
        # Load Theme
        if THEME_AVAILABLE:
            self.colors = theme_manager.get_theme_colors()
            self.fonts = theme_manager.get_theme_fonts()
        else:
            self.colors = {
                'primary': "#0f172a", 'secondary': "#1e293b",
                'accent_primary': "#38bdf8", 'accent_secondary': "#818cf8",
                'success': "#10b981", 'warning': "#f59e0b", 'danger': "#ef4444",
                'text_primary': "#f8fafc", 'text_secondary': "#94a3b8"
            }
            self.fonts = {"primary": "Segoe UI", "secondary": "Arial"}

        self.root.configure(bg=self.colors['primary'])
        self.root.title(f"Admin Portal - {admin_data.get('username', 'Admin')}")
        self.root.geometry("1200x800")
        
        self.setup_ui()

    def setup_ui(self):
        # --- Sidebar ---
        sidebar = tk.Frame(self.root, bg=self.colors['secondary'], width=260)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Brand
        tk.Label(sidebar, text="🛡️ ADMIN CORE", font=(self.fonts['primary'], 16, "bold"),
                 fg=self.colors['accent_primary'], bg=self.colors['secondary']).pack(pady=40)

        # Navigation Buttons
        self.create_nav_btn(sidebar, "📊 Dashboard", self.show_dashboard)
        self.create_nav_btn(sidebar, "👥 User Management", self.show_user_mgmt)
        self.create_nav_btn(sidebar, "🛠️ AI Workbench", self.launch_legacy_tools)
        self.create_nav_btn(sidebar, "⚙️ Settings", self.open_settings)
        
        # Logout
        tk.Button(sidebar, text="Log Out", command=self.logout,
                 bg=self.colors['danger'], fg="white", font=(self.fonts['primary'], 11, "bold"),
                 relief="flat", pady=10).pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=40)

        # --- Main Content Area ---
        self.content_area = tk.Frame(self.root, bg=self.colors['primary'])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Initialize with Dashboard
        self.show_dashboard()

    def create_nav_btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, command=cmd,
                       bg=self.colors['secondary'], fg=self.colors['text_primary'],
                       font=(self.fonts['primary'], 11), anchor="w", padx=20, pady=12,
                       relief="flat", activebackground=self.colors['primary'], activeforeground=self.colors['accent_primary'])
        btn.pack(fill=tk.X)
        return btn

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- Pages ---

    # --- Pages ---

    def show_dashboard(self):
        self.clear_content()
        
        # Header
        tk.Label(self.content_area, text="System Overview", font=(self.fonts['primary'], 24, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['primary']).pack(anchor="w", pady=(0, 20))
        
        # Stats Grid
        stats_frame = tk.Frame(self.content_area, bg=self.colors['primary'])
        stats_frame.pack(fill=tk.X, pady=20)
        stats_frame.columnconfigure(0, weight=1); stats_frame.columnconfigure(1, weight=1); stats_frame.columnconfigure(2, weight=1)
        
        self.create_stat_card(stats_frame, 0, "Total Users", self.get_total_users(), "👥", self.colors['accent_primary'])
        self.create_stat_card(stats_frame, 1, "Votes Cast", self.get_total_votes(), "🗳️", self.colors['success'])
        self.create_stat_card(stats_frame, 2, "System Health", "Optimal", "✅", self.colors['warning'])
        
        # Quick Actions
        tk.Label(self.content_area, text="Quick Actions", font=(self.fonts['primary'], 18, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['primary']).pack(anchor="w", pady=(40, 15))
        
        actions_frame = tk.Frame(self.content_area, bg=self.colors['primary'])
        actions_frame.pack(fill=tk.X, anchor="w")
        
        self.create_action_btn(actions_frame, "Add New Admin", self.show_add_admin_modal, self.colors['accent_secondary'])
        self.create_action_btn(actions_frame, "View Audit Logs", self.show_audit_logs, self.colors['secondary'])
        self.create_action_btn(actions_frame, "Open Iris Gallery", self.show_iris_gallery, self.colors['accent_primary'])

        # Election Controls
        tk.Label(self.content_area, text="Election Controls", font=(self.fonts['primary'], 18, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['primary']).pack(anchor="w", pady=(40, 15))
        
        election_frame = tk.Frame(self.content_area, bg=self.colors['primary'])
        election_frame.pack(fill=tk.X, anchor="w")

        self.create_action_btn(election_frame, "🔄 Refresh Votes (Reset)", self.initiate_vote_reset, self.colors['danger'])
        self.create_action_btn(election_frame, "👤 Register Admin Face", self.register_admin_face, self.colors['warning'])

    def show_iris_gallery(self):
        self.clear_content()
        tk.Label(self.content_area, text="Iris Image Gallery", font=(self.fonts['primary'], 24, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['primary']).pack(anchor="w", pady=(0, 20))

        # Toolbar
        toolbar = tk.Frame(self.content_area, bg=self.colors['primary'])
        toolbar.pack(fill=tk.X, pady=20)
        
        def open_folder():
            folder = "captured_iris"
            if not os.path.exists(folder):
                os.makedirs(folder)
            os.startfile(os.path.abspath(folder))
            
        tk.Button(toolbar, text="📂 Open Gallery Folder", command=open_folder,
                 bg=self.colors['accent_primary'], fg="black", font=(self.fonts['primary'], 12, "bold"),
                 relief="flat", padx=20, pady=10).pack(side=tk.LEFT)
                 
        tk.Label(toolbar, text="Images are stored in 'captured_iris' folder", 
                fg=self.colors['text_secondary'], bg=self.colors['primary'], font=(self.fonts['primary'], 10)).pack(side=tk.LEFT, padx=20)

        # File List
        list_frame = tk.Frame(self.content_area, bg=self.colors['secondary'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(list_frame, text="Recent Captures", bg=self.colors['secondary'], fg=self.colors['text_primary'],
                font=(self.fonts['primary'], 12, "bold")).pack(anchor="w", padx=10, pady=10)
        
        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        file_list = tk.Listbox(list_frame, bg=self.colors['secondary'], fg=self.colors['text_primary'],
                        font=("Consolas", 10), bd=0, yscrollcommand=scroll.set)
        file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        scroll.config(command=file_list.yview)
        
        # Populate
        folder = "captured_iris"
        if os.path.exists(folder):
            try:
                files = os.listdir(folder)
                files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
                for f in files:
                    file_list.insert(tk.END, f)
            except Exception as e:
                file_list.insert(tk.END, f"Error reading folder: {e}")
        else:
            file_list.insert(tk.END, "Gallery folder not found.")

    def show_user_mgmt(self):
        self.clear_content()
        tk.Label(self.content_area, text="User Management", font=(self.fonts['primary'], 24, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['primary']).pack(anchor="w", pady=(0, 20))
        
        # Tabs
        style = ttk.Style()
        style.configure("TNotebook", background=self.colors['primary'], borderwidth=0)
        style.configure("TNotebook.Tab", padding=[15, 5], font=(self.fonts['primary'], 11))
        
        notebook = ttk.Notebook(self.content_area)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: System Admins
        self.tab_admins = tk.Frame(notebook, bg=self.colors['primary'])
        notebook.add(self.tab_admins, text="  System Admins  ")
        self.setup_admin_tab(self.tab_admins)
        
        # Tab 2: Enrolled Persons
        self.tab_persons = tk.Frame(notebook, bg=self.colors['primary'])
        notebook.add(self.tab_persons, text="  Enrolled Persons  ")
        self.setup_persons_tab(self.tab_persons)

    def setup_admin_tab(self, parent):
        # Toolbar
        toolbar = tk.Frame(parent, bg=self.colors['primary'])
        toolbar.pack(fill=tk.X, pady=20)
        
        tk.Button(toolbar, text="+ Register New Admin", command=self.show_add_admin_modal,
                 bg=self.colors['success'], fg="white", font=(self.fonts['primary'], 11, "bold"),
                 relief="flat", padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
                 
        tk.Button(toolbar, text="🗑️ Delete Selected Admin(s)", command=self.delete_selected_admin,
                 bg=self.colors['danger'], fg="white", font=(self.fonts['primary'], 11, "bold"),
                 relief="flat", padx=15, pady=8).pack(side=tk.LEFT)
        
        # User List
        list_frame = tk.Frame(parent, bg=self.colors['secondary'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable MULTIPLE selection (EXTENDED allows shift-click and ctrl-click)
        self.admin_listbox = tk.Listbox(list_frame, bg=self.colors['secondary'], fg=self.colors['text_primary'],
                        font=("Consolas", 11), bd=0, yscrollcommand=scroll.set, height=15, selectmode=tk.EXTENDED)
        self.admin_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll.config(command=self.admin_listbox.yview)
        
        # Populate
        self.load_admin_list()

    def load_admin_list(self):
        self.admin_listbox.delete(0, tk.END)
        if DB_AVAILABLE:
            users = db.get_all_users()
            for u in users:
                role_icon = "🛡️" if u['role'] == 'admin' else "👤"
                self.admin_listbox.insert(tk.END, f"{u['username']} | Role: {u['role']}")

    def delete_selected_admin(self):
        sel = self.admin_listbox.curselection()
        if not sel:
            messagebox.showwarning("Selection", "Please select admin(s) to delete.")
            return
            
        # Collect usernames
        usernames = []
        for idx in sel:
            item_text = self.admin_listbox.get(idx)
            username = item_text.split('|')[0].strip()
            usernames.append(username)

        # Safety Check
        if self.admin_data.get('username') in usernames:
            messagebox.showerror("Error", "You cannot delete your own account! Deselect your username.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Permanently delete {len(usernames)} admin account(s)?\nThis cannot be undone."):
            success_count = 0
            fail_count = 0
            
            if DB_AVAILABLE:
                for username in usernames:
                    if db.delete_user_permanently(username):
                        success_count += 1
                    else:
                        fail_count += 1
                
                msg = f"Deleted: {success_count}"
                if fail_count > 0: msg += f"\nFailed: {fail_count}"
                
                messagebox.showinfo("Result", msg)
                self.load_admin_list()

    def setup_persons_tab(self, parent):
        # Toolbar
        toolbar = tk.Frame(parent, bg=self.colors['primary'])
        toolbar.pack(fill=tk.X, pady=20)
        
        tk.Button(toolbar, text="🗑️ Delete Selected Person(s)", command=self.delete_selected_person,
                 bg=self.colors['danger'], fg="white", font=(self.fonts['primary'], 11, "bold"),
                 relief="flat", padx=15, pady=8).pack(side=tk.LEFT)
        
        # Person List
        list_frame = tk.Frame(parent, bg=self.colors['secondary'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable MULTIPLE selection
        self.person_listbox = tk.Listbox(list_frame, bg=self.colors['secondary'], fg=self.colors['text_primary'],
                        font=("Consolas", 11), bd=0, yscrollcommand=scroll.set, height=15, selectmode=tk.EXTENDED)
        self.person_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll.config(command=self.person_listbox.yview)
        
        # Populate
        self.load_person_list()

    def load_person_list(self):
        self.person_listbox.delete(0, tk.END)
        if DB_AVAILABLE:
            persons = db.get_all_persons()
            for p in persons:
                self.person_listbox.insert(tk.END, f"ID: {p['id']} | {p['name']} | Dept: {p.get('department','N/A')}")

    def delete_selected_person(self):
        sel = self.person_listbox.curselection()
        if not sel:
            messagebox.showwarning("Selection", "Please select person(s) to delete.")
            return
            
        pids = []
        for idx in sel:
            item_text = self.person_listbox.get(idx)
            try:
                pid_part = item_text.split('|')[0]
                pid = int(pid_part.replace("ID:", "").strip())
                pids.append(pid)
            except:
                pass
        
        if not pids:
             messagebox.showerror("Error", "Could not parse selected IDs.")
             return

        if messagebox.askyesno("Confirm Deletion", f"Permanently delete {len(pids)} Person profile(s)?\nAll biometric data, logs, and vote records will be removed."):
            success_count = 0
            fail_count = 0
            
            if DB_AVAILABLE:
                for pid in pids:
                    if db.delete_person_permanently(pid):
                        success_count += 1
                    else:
                        fail_count += 1
            
            msg = f"Deleted: {success_count}"
            if fail_count > 0: msg += f"\nFailed: {fail_count}"
            
            messagebox.showinfo("Result", msg)
            self.load_person_list()

    def show_audit_logs(self):
        self.clear_content()
        tk.Label(self.content_area, text="System Audit Logs", font=(self.fonts['primary'], 24, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['primary']).pack(anchor="w", pady=(0, 20))
        
        # Tools
        tools = tk.Frame(self.content_area, bg=self.colors['primary'])
        tools.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(tools, text="🔄 Refresh Logs", command=self.show_audit_logs,
                 bg=self.colors['accent_secondary'], fg="#0f172a", font=(self.fonts['primary'], 10, "bold"),
                 relief="flat", padx=15).pack(side=tk.LEFT)
        
        # Log Table
        list_frame = tk.Frame(self.content_area, bg=self.colors['secondary'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        cols = ("Time", "User", "Action", "Status/Details")
        
        tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        
        # Style Treeview
        style = ttk.Style()
        style.configure("Treeview", 
                        background=self.colors['secondary'], 
                        foreground=self.colors['text_primary'],
                        fieldbackground=self.colors['secondary'],
                        font=(self.fonts['secondary'], 10))
        style.configure("Treeview.Heading", font=(self.fonts['primary'], 10, "bold"))
        style.map('Treeview', background=[('selected', self.colors['accent_primary'])])
        
        tree.heading("Time", text="Timestamp")
        tree.heading("User", text="Actor")
        tree.heading("Action", text="Action")
        tree.heading("Status/Details", text="Details")
        
        tree.column("Time", width=150)
        tree.column("User", width=100)
        tree.column("Action", width=150)
        tree.column("Status/Details", width=300)
        
        v_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=v_scroll.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        if DB_AVAILABLE:
            try:
                # Use SQL directly if specific method missing
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    # Try access logs + audit logs or just one?
                    # Let's show access logs first as they are most relevant for "audit" of entry
                    cursor.execute('''
                        SELECT access_time, person_id, access_type, access_granted, confidence_score 
                        FROM access_logs 
                        ORDER BY access_time DESC LIMIT 100
                    ''')
                    logs = cursor.fetchall()
                    
                    for log in logs:
                        status = "✅ Granted" if log['access_granted'] else "❌ Denied"
                        details = f"Score: {log['confidence_score']:.2f}"
                        # Resolve person name if possible
                        p_name = f"ID: {log['person_id']}"
                        
                        tree.insert("", "end", values=(log['access_time'], p_name, log['access_type'], f"{status} | {details}"))
            except Exception as e:
                tree.insert("", "end", values=("Error", "DB Error", str(e), ""))

    def show_add_admin_modal(self):
        modal = tk.Toplevel(self.root)
        modal.title("Register New Admin")
        modal.geometry("500x500")
        modal.configure(bg=self.colors['secondary'])
        
        # Center
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 250
        modal.geometry(f"+{x}+{y}")
        
        tk.Label(modal, text="New Admin Registration", font=(self.fonts['primary'], 16, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['secondary']).pack(pady=30)
        
        # Form
        form = tk.Frame(modal, bg=self.colors['secondary'])
        form.pack(padx=50, fill=tk.X)
        
        def entry(label, show=None):
            tk.Label(form, text=label, font=(self.fonts['primary'], 11), fg=self.colors['text_secondary'], bg=self.colors['secondary']).pack(anchor="w", pady=(10, 5))
            e = tk.Entry(form, font=(self.fonts['primary'], 12), show=show, bg="#0f172a", fg="white", insertbackground="white", relief="flat")
            e.pack(fill=tk.X, ipady=5)
            return e
            
        u_entry = entry("Username")
        p_entry = entry("Password", show="*")
        c_entry = entry("Confirm Password", show="*")
        
        def save():
            u = u_entry.get().strip()
            p = p_entry.get()
            c = c_entry.get()
            
            if not u or not p:
                messagebox.showerror("Error", "All fields are required", parent=modal)
                return
            if p != c:
                messagebox.showerror("Error", "Passwords do not match", parent=modal)
                return
                
            if DB_AVAILABLE:
                try:
                    # Create Admin
                    db.create_user_with_password(u, p, role='admin', display_name=u)
                    messagebox.showinfo("Success", f"Admin '{u}' created successfully!", parent=modal)
                    modal.destroy()
                    self.show_user_mgmt() # Refresh list
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to create admin: {e}", parent=modal)
            else:
                 messagebox.showerror("Error", "Database not available", parent=modal)

        tk.Button(modal, text="Create Admin Account", command=save,
                 bg=self.colors['accent_primary'], fg="#0f172a", font=(self.fonts['primary'], 12, "bold"),
                 relief="flat", pady=10).pack(pady=40, padx=50, fill=tk.X)

    def register_admin_face(self):
        """Register face for the current admin"""
        username = self.admin_data.get('username')
        
        if not messagebox.askyesno("Face Registration", 
                "You are about to register your face for high-security actions actions (like resetting votes).\n\n"
                "Please look directly at the camera and ensure good lighting.\n\nReady?"):
            return

        try:
            messagebox.showinfo("Instructions", "Camera will open. Look at the camera until capture completes.")
            face_vec = capture_face_vector_from_camera()
            
            if face_vec is None:
                messagebox.showerror("Error", "Failed to capture face. Please try again.")
                return
                
            # Convert numpy array to bytes for storage
            face_blob = face_vec.tobytes()
            
            if db.update_user_face(username, face_blob):
                messagebox.showinfo("Success", "Face registered successfully! You can now use biometric verification.")
            else:
                messagebox.showerror("Error", "Failed to save face data to database.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def initiate_vote_reset(self):
        """Secure vote reset with biometric verification"""
        username = self.admin_data.get('username')
        
        # 1. Check if face is registered
        stored_face_blob = db.get_user_face(username)
        if not stored_face_blob:
            messagebox.showwarning("Not Registered", 
                "You must register your face first to use this feature.\n"
                "Please click 'Register Admin Face' button.")
            return

        # 2. Warning
        if not messagebox.askyesno("Security Check", 
                "⚠️ CRITICAL ACTION ⚠️\n\n"
                "You are attempting to DELETE ALL VOTES to start a new election.\n"
                "This action requires Biometric Face Verification.\n\n"
                "Proceed with verification?"):
            return

        # 3. Capture Live Face
        messagebox.showinfo("Verification", "Please look at the camera for verification.")
        try:
            live_vec = capture_face_vector_from_camera()
            if live_vec is None:
                messagebox.showerror("Error", "Could not capture face.")
                return

            # 4. Compare
            stored_vec = np.frombuffer(stored_face_blob, dtype=np.float32)
            
            # Cosine Similarity
            dot_product = np.dot(live_vec, stored_vec)
            norm_a = np.linalg.norm(live_vec)
            norm_b = np.linalg.norm(stored_vec)
            similarity = dot_product / (norm_a * norm_b)
            
            print(f"DEBUG: Admin Face Auth Similarity: {similarity}")

            if similarity > 0.6:  # Threshold for verification
                # 5. Final Confirmation
                if messagebox.askyesno("Final Confirmation", 
                        "✅ Identity Verified.\n\n"
                        "Are you absolutely sure you want to DELETE ALL VOTES?\n"
                        "This will reset the election results permanently!"):
                    
                    if voting_system.clear_all_votes():
                        messagebox.showinfo("Success", "All votes have been deleted. The election has been reset.")
                        # Refresh Dashboard
                        self.show_dashboard()
                    else:
                        messagebox.showerror("Error", "Failed to clear votes from database.")
            else:
                messagebox.showerror("Access Denied", "Face verification failed. Identity not confirmed.")

        except Exception as e:
            messagebox.showerror("Error", f"Verification process failed: {e}")

    # --- Helpers ---
    def create_stat_card(self, parent, col, title, value, icon, color):
        card = tk.Frame(parent, bg=self.colors['secondary'], padx=20, pady=20)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        
        tk.Label(card, text=icon, font=("Segoe UI Emoji", 24), bg=self.colors['secondary'], fg=color).pack(anchor="ne")
        tk.Label(card, text=value, font=(self.fonts['primary'], 28, "bold"), bg=self.colors['secondary'], fg=self.colors['text_primary']).pack(anchor="w")
        tk.Label(card, text=title, font=(self.fonts['primary'], 11), bg=self.colors['secondary'], fg=self.colors['text_secondary']).pack(anchor="w")

    def create_action_btn(self, parent, text, cmd, color):
        tk.Button(parent, text=text, command=cmd,
                 bg=color, fg="#0f172a", font=(self.fonts['primary'], 11, "bold"),
                 relief="flat", padx=20, pady=10).pack(side=tk.LEFT, padx=(0, 15))

    def get_total_users(self):
        if DB_AVAILABLE:
            try: return str(len(db.get_all_persons()))
            except: return "0"
        return "N/A"
        
    def get_total_votes(self):
        if DB_AVAILABLE:
            try: return str(db.get_system_statistics().get('today_votes', 0)) # Or total
            except: return "0"
        return "N/A"

    def launch_legacy_tools(self):
        # Open AI Workbench
        try:
            import ai_workbench
            
            # Helper to return to dashboard
            def back_to_dash():
                # Re-initialize the entire portal since root was cleared
                show_admin_portal(self.root, self.admin_data)

            ai_workbench.show_workbench(self.root, close_cmd=back_to_dash)
            
        except ImportError as e:
            messagebox.showerror("Error", f"AI Workbench module missing: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch AI Workbench: {e}")

    def open_settings(self):
        try:
            subprocess.Popen([sys.executable, "settings_window.py"])
        except:
            messagebox.showinfo("Settings", "Settings window script not found.")

    def logout(self):
        if self.logout_callback: self.logout_callback()
        else: self.root.destroy()

def show_admin_portal(root, admin_data):
    # Clear root
    for w in root.winfo_children(): w.destroy()
    
    def on_logout():
        root.destroy()
        try:
            import welcome_interface
            import importlib
            importlib.reload(welcome_interface)
            welcome_interface.main()
        except: pass

    AdminPortal(root, admin_data, logout_callback=on_logout)

if __name__ == "__main__":
    r = tk.Tk()
    show_admin_portal(r, {'username': 'SuperAdmin'})
    r.mainloop()
