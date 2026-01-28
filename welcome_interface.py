#!/usr/bin/env python3
"""
Animated Welcome Interface for the Iris Recognition Project
Features:
- Premium Aesthetic Design (Deep Navy/Gold/Teal)
- Responsive Layout
- Clear entry points
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
import random
import sys
import os
from PIL import Image, ImageTk

try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    CV2_AVAILABLE = False
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

    PIL_AVAILABLE = False

# Import Theme Manager
try:
    from theme_manager import theme_manager
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False

try:
    from auth_ui import show_user_login, show_admin_login
    AUTH_AVAILABLE = True
except Exception:
    AUTH_AVAILABLE = False

class SuccessPopup(tk.Toplevel):
    def __init__(self, parent, title="Success", message="Action Completed Successfully", callback=None):
        super().__init__(parent)
        self.callback = callback
        self.configure(bg='#1a1a2e')
        self.overrideredirect(True) # Frameless
        self.attributes('-topmost', True)
        
        # Center on parent
        w, h = 400, 250
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (w // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        
        # Canvas for animation
        self.canvas = tk.Canvas(self, width=w, height=h, bg='#1a1a2e', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Checkmark setup
        self.cx, self.cy = w//2, h//2 - 20
        self.radius = 40
        self.circle_angle = 0
        self.tick_progress = 0
        
        self.message = message
        self.title_text = title
        
        self.after(50, self.animate_circle)
        
        # Close button (delayed appearance)
        self.close_btn = tk.Button(self, text="Enroll Biometrics", command=self.on_enroll, 
                                 bg='#4CAF50', fg='white', font=("Segoe UI", 10, "bold"), relief="flat", padx=20)
        self.skip_btn = tk.Button(self, text="Finish", command=self.close_popup, 
                                bg='#f44336', fg='white', font=("Segoe UI", 10, "bold"), relief="flat", padx=20)

    def on_enroll(self):
        self.destroy()
        if self.callback:
            self.callback(True)

    def close_popup(self):
        self.destroy()
        if self.callback:
            self.callback(False)

    def animate_circle(self):
        if self.circle_angle < 360:
            self.circle_angle += 20
            self.canvas.delete("circle")
            self.canvas.create_arc(self.cx-self.radius, self.cy-self.radius, 
                                 self.cx+self.radius, self.cy+self.radius, 
                                 start=90, extent=-self.circle_angle, style=tk.ARC, outline="#4CAF50", width=4, tags="circle")
            self.after(10, self.animate_circle)
        else:
            self.animate_tick()

    def animate_tick(self):
        if self.tick_progress < 1.0:
            self.tick_progress += 0.1
            self.canvas.delete("tick")
            
            # Checkmark points
            start = (self.cx - 20, self.cy)
            mid = (self.cx - 5, self.cy + 15)
            end = (self.cx + 25, self.cy - 15)
            
            # Draw partial checkmark
            if self.tick_progress <= 0.5:
                p = self.tick_progress * 2
                cur_x = start[0] + (mid[0] - start[0]) * p
                cur_y = start[1] + (mid[1] - start[1]) * p
                self.canvas.create_line(start[0], start[1], cur_x, cur_y, fill="#4CAF50", width=4, tags="tick", capstyle=tk.ROUND)
            else:
                self.canvas.create_line(start[0], start[1], mid[0], mid[1], fill="#4CAF50", width=4, tags="tick", capstyle=tk.ROUND)
                p = (self.tick_progress - 0.5) * 2
                cur_x = mid[0] + (end[0] - mid[0]) * p
                cur_y = mid[1] + (end[1] - mid[1]) * p
                self.canvas.create_line(mid[0], mid[1], cur_x, cur_y, fill="#4CAF50", width=4, tags="tick", capstyle=tk.ROUND)
                
            self.after(10, self.animate_tick)
        else:
            self.show_text()

    def show_text(self):
        self.canvas.create_text(self.cx, self.cy + 60, text=self.title_text, font=("Segoe UI", 16, "bold"), fill="white")
        self.canvas.create_text(self.cx, self.cy + 90, text=self.message, font=("Segoe UI", 10), fill="#aaa")
        
        self.close_btn.place(relx=0.3, rely=0.85, anchor="center")
        self.skip_btn.place(relx=0.7, rely=0.85, anchor="center")

class AnimatedWelcome:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Iris Recognition Platform")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 768)
        
        # Load Theme Colors
        if THEME_AVAILABLE:
            self.colors = theme_manager.get_theme_colors()
            self.fonts = theme_manager.get_theme_fonts()
        else:
            self.colors = {
                'primary': '#0f172a',    # Deep Slate
                'secondary': '#1e293b',  # Lighter Slate
                'accent_primary': '#38bdf8',   # Sky Blue
                'accent_secondary': '#818cf8', # Indigo
                'text_primary': '#f8fafc',
                'text_secondary': '#94a3b8'
            }
            self.fonts = {'primary': 'Segoe UI', 'secondary': 'Arial'}

        self.root.configure(bg=self.colors['primary'])
        self._closed = False
        self._anim_after = None

        # Center window
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._start_animation()

    def _on_close(self):
        self._closed = True
        try:
            if self._anim_after:
                self.root.after_cancel(self._anim_after)
            self.root.destroy()
        except:
            pass

    def _build_ui(self):
        # Canvas for background animation
        self.canvas = tk.Canvas(self.root, bg=self.colors['primary'], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Main Container (Centered)
        # We use a window on the canvas to hold standard widgets
        self.main_frame = tk.Frame(self.canvas, bg=self.colors['primary'])
        # Initial placement at center of default 1280x800 window
        self.canvas_window = self.canvas.create_window(640, 400, window=self.main_frame, anchor='center')
        
        # Layout: Split 60/40 approx
        # Left: Info/Hero
        # Right: Actions
        
        container = tk.Frame(self.main_frame, bg=self.colors['secondary'], padx=0, pady=0) 
        # Add shadow/border effect? Simple border for now
        container.configure(highlightbackground=self.colors['accent_secondary'], highlightthickness=1)
        container.pack(ipadx=0, ipady=0)

        # Split Container
        left_panel = tk.Frame(container, bg=self.colors['secondary'], width=600, height=500)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=40, pady=40)
        
        right_panel = tk.Frame(container, bg="#111827", width=400, height=500) # Slightly darker for contrast
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=0, pady=0)
        
        # --- Left Panel Content ---
        tk.Label(left_panel, text="IRIS RECOGNITION", font=(self.fonts['primary'], 12, "bold"), 
                 fg=self.colors['accent_primary'], bg=self.colors['secondary']).pack(anchor='w', pady=(0, 20))
        
        tk.Label(left_panel, text="Secure.\nFast.\nReliable.", 
                 font=(self.fonts['primary'], 48, "bold"), fg=self.colors['text_primary'], bg=self.colors['secondary'], justify="left").pack(anchor='w')
        
        tk.Label(left_panel, text="Advanced biometric voting and identification system.\nExperience the future of secure authentication.", 
                 font=(self.fonts['primary'], 12), fg=self.colors['text_secondary'], bg=self.colors['secondary'], justify="left").pack(anchor='w', pady=(20, 40))
        
        # Features list
        features = ["✓ 99.9% Accuracy", "✓ Live Liveness Detection", "✓ Homomorphic Encryption"]
        for f in features:
            tk.Label(left_panel, text=f, font=(self.fonts['primary'], 11), fg=self.colors['text_primary'], bg=self.colors['secondary']).pack(anchor='w', pady=2)

        # --- Right Panel Content (Login Options) ---
        # Padding wrapper
        r_content = tk.Frame(right_panel, bg="#111827", padx=40, pady=40)
        r_content.pack(fill=tk.BOTH, expand=True)

        tk.Label(r_content, text="Welcome Back", font=(self.fonts['primary'], 24, "bold"), 
                 fg=self.colors['text_primary'], bg="#111827").pack(anchor='center', pady=(0, 10))
        tk.Label(r_content, text="Please select your portal", font=(self.fonts['primary'], 11), 
                 fg=self.colors['text_secondary'], bg="#111827").pack(anchor='center', pady=(0, 40))

        # Buttons
        self._create_btn(r_content, "User Login", self._user_login, self.colors['accent_primary']).pack(fill=tk.X, pady=10)
        self._create_btn(r_content, "Registration", self._open_registration, self.colors['success']).pack(fill=tk.X, pady=10)
        self._create_btn(r_content, "Admin Portal", self._admin_login, self.colors['warning']).pack(fill=tk.X, pady=10)

        # Footer Link
        tk.Button(r_content, text="View Public Results →", command=self._open_results,
                  bg="#111827", fg=self.colors['accent_secondary'], font=(self.fonts['primary'], 10),
                  bd=0, activebackground="#111827", cursor="hand2").pack(pady=(30, 0))

    def _center_frame_on_canvas(self, event=None):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w < 100 or h < 100:
             w = 1280
             h = 800
        self.canvas.coords(self.canvas_window, w/2, h/2)

    def _create_btn(self, parent, text, cmd, color):
        btn = tk.Button(
            parent, text=text, command=cmd,
            bg=color, fg="#0f172a",
            font=(self.fonts['primary'], 11, "bold"),
            relief="flat", bd=0, padx=20, pady=12,
            activebackground="#ffffff", activeforeground=color,
            cursor="hand2"
        )
        return btn

    def _play_intro_video(self, video_path):
        if not CV2_AVAILABLE or not PIL_AVAILABLE:
            print("OpenCV or PIL not available. Skipping intro video.")
            self._start_animation() # Start animation immediately if video cannot play
            return

        if not os.path.exists(video_path):
            print(f"Intro video not found: {video_path}")
            self._start_animation() # Start animation immediately if video not found
            return

        # Cover everything with a black frame
        intro_frame = tk.Frame(self.root, bg="black")
        intro_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        video_lbl = tk.Label(intro_frame, bg="black")
        video_lbl.pack(fill=tk.BOTH, expand=True)
        
        cap = cv2.VideoCapture(video_path)
        
        def stream():
            if not cap.isOpened():
                finish()
                return
                
            ret, frame = cap.read()
            if ret:
                # Resize to fit window
                w = self.root.winfo_width()
                h = self.root.winfo_height()
                if w > 10 and h > 10: # Avoid startup constraints
                    frame = cv2.resize(frame, (w, h))
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                video_lbl.config(image=imgtk)
                video_lbl.image = imgtk
                
                # Next frame (approx 30fps -> 33ms)
                self.root.after(33, stream)
            else:
                finish()
                
        def finish():
            cap.release()
            intro_frame.destroy()
            # Start particle animation after video
            self._start_animation()
            # Force layout update
            self.root.update_idletasks()
            self._center_frame_on_canvas()
            
        stream()

    # _create_btn and _center_frame_on_canvas were duplicates here, removed.

    def _start_animation(self):
        # Subtle particle system
        self.particles = []
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, 2000),
                'y': random.randint(0, 1200),
                'r': random.randint(2, 6),
                'dx': random.uniform(-0.5, 0.5),
                'dy': random.uniform(-0.5, 0.5),
                'alpha': random.randint(50, 150) # Simulated opacity via color
            })
        self._animate()

    def _animate(self):
        if self._closed: return
        
        self.canvas.delete("p")
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            
            # Wrap
            if p['x'] < 0: p['x'] = w
            if p['x'] > w: p['x'] = 0
            if p['y'] < 0: p['y'] = h
            if p['y'] > h: p['y'] = 0
            
            # Draw
            # Simulate transparency by blending with bg color (rough approx)
            # Actually just use accent color
            col = self.colors['accent_secondary']
            self.canvas.create_oval(p['x'], p['y'], p['x']+p['r'], p['y']+p['r'], fill=col, outline="", tags="p")

        self.canvas.tag_lower("p") # Keep behind the main frame
        self._anim_after = self.root.after(50, self._animate)

    def _user_login(self):
        if not AUTH_AVAILABLE:
            messagebox.showerror("Error", "Authentication module not found.")
            return

        def on_success(user_data):
            # Close welcome screen
            self._on_close()
            
            # Open User Portal
            try:
                # We need to run the UserPortal on a fresh root or the existing one?
                # UserPortal expects a root. Since we destroyed ours, we create new one.
                # Or wait, _on_close destroys root.
                
                # We should launch a new script or create new root.
                # Ideally, we call a function that creates a new root and mainloop.
                
                # Import here to avoid early execution
                import user_portal
                
                new_root = tk.Tk()
                new_root.geometry("1400x900")
                user_portal.show_user_portal(new_root, user_data)
                new_root.mainloop()
                
            except Exception as e:
                # Fallback
                messagebox.showerror("Error", f"Failed to launch User Portal: {e}")
                import traceback
                traceback.print_exc()

        show_user_login(on_success)

    def _admin_login(self):
        if not AUTH_AVAILABLE: return
        
        def iris_verify_stub(u): return True # Simplify for now
        
        def on_success(user_data):
            self._on_close()
            try:
                import admin_portal
                new_root = tk.Tk()
                new_root.geometry("1400x900")
                admin_portal.show_admin_portal(new_root, user_data)
                new_root.mainloop()
            except Exception as e:
                 # Fallback
                 import traceback
                 traceback.print_exc()
                 messagebox.showerror("Error", f"Failed to launch Admin Portal: {e}")

        show_admin_login(on_success, iris_verify_stub)

    def _open_registration(self):
        try:
            from database_manager import db
        except ImportError:
            messagebox.showerror("Error", "Database module not available.")
            return

        reg_win = tk.Toplevel(self.root)
        reg_win.title("Voter Registration")
        reg_win.geometry("500x600")
        reg_win.configure(bg=self.colors['secondary'])
        
        # Center
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 300
        reg_win.geometry(f"+{x}+{y}")
        
        tk.Label(reg_win, text="Member Registration", font=(self.fonts['primary'], 20, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['secondary']).pack(pady=(40, 30))
        
        # Container for Canvas + Scrollbar
        container_frame = tk.Frame(reg_win, bg=self.colors['secondary'])
        container_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(container_frame, bg=self.colors['secondary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        
        # Scrollable Frame
        form = tk.Frame(canvas, bg=self.colors['secondary'])
        
        # Configure scrolling
        canvas.create_window((0, 0), window=form, anchor="nw", tags="form_window")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def _on_canvas_configure(event):
            # Ensure form fills canvas width
            canvas.itemconfig("form_window", width=event.width)

        form.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        # Pack layout
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add padding inside form
        tk.Frame(form, bg=self.colors['secondary'], height=20).pack() 

        def entry(label, show=None):
            tk.Label(form, text=label, font=(self.fonts['primary'], 11), 
                     fg=self.colors['text_secondary'], bg=self.colors['secondary']).pack(anchor="w", pady=(10, 5), padx=30)
            e = tk.Entry(form, font=(self.fonts['primary'], 12), show=show, 
                         bg="#1f2937", fg="white", insertbackground="white", 
                         relief="flat")
            e.pack(fill=tk.X, ipady=8, padx=30)
            return e
            
        u_entry = entry("Username")
        d_entry = entry("Full Name")
        phone_entry = entry("Mobile Number")
        addr_entry = entry("Address")
        vid_entry = entry("Voter ID")
        p_entry = entry("Password", show="*")
        c_entry = entry("Confirm Password", show="*")
        
        def do_register():
            u = u_entry.get().strip()
            d = d_entry.get().strip()
            phone = phone_entry.get().strip()
            addr = addr_entry.get().strip()
            vid = vid_entry.get().strip()
            p = p_entry.get()
            c = c_entry.get()
            
            if not u or not p:
                messagebox.showerror("Error", "Username and Password are required.", parent=reg_win)
                return
            
            if not phone:
                messagebox.showerror("Error", "Mobile Number is required.", parent=reg_win)
                return

            if p != c:
                messagebox.showerror("Error", "Passwords do not match.", parent=reg_win)
                return

            if not d:
                messagebox.showerror("Error", "Full Name is required.", parent=reg_win)
                return
                
            if not vid:
                messagebox.showerror("Error", "Voter ID is required.", parent=reg_win)
                return
                
            if not addr:
                messagebox.showerror("Error", "Address is required.", parent=reg_win)
                return
                
            try:
                # Check exist
                if db.get_user(u):
                    messagebox.showerror("Error", "Username already exists.", parent=reg_win)
                    return
                
                if db.check_phone_exists(phone):
                    messagebox.showerror("Error", "Mobile number already exists.", parent=reg_win)
                    return
                
                # Check Name exist
                if db.check_person_name_exists(d):
                    messagebox.showerror("Error", "A person with this Name is already registered.", parent=reg_win)
                    return

                # 1. Create Person Entry
                pid = db.enroll_person(
                    name=d,
                    iris_template=None,
                    phone=phone,
                    role='voter',
                    address=addr,
                    voter_id=vid
                )

                # 2. Create User Entry linked to Person ID
                db.create_user_with_password(u, p, role='voter', display_name=d)
                
                # 3. Link them manually (or ensure create_user did it if updated)
                # Just to be safe:
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET person_id = ? WHERE username = ?", (pid, u))
                    conn.commit()
                
                # Success
                def on_popup_choice(enroll):
                    reg_win.destroy()
                    if enroll:
                        try:
                            import subprocess
                            subprocess.Popen([sys.executable, "user_enroll.py", u])
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to launch enrollment: {e}")

                SuccessPopup(reg_win, title="Registered!", 
                           message=f"User {u} successfully registered.", 
                           callback=on_popup_choice)
                
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {e}", parent=reg_win)

        tk.Button(form, text="Create Account", command=do_register,
                  bg=self.colors['accent_primary'], fg="#0f172a", 
                  font=(self.fonts['primary'], 12, "bold"),
                  relief="flat", pady=12, cursor="hand2").pack(fill=tk.X, padx=30, pady=40)

    def _open_results(self):
        try:
            from voting_results import show_voting_results
            show_voting_results()
        except:
             messagebox.showerror("Error", "Results module unavailable")

def main():
    app = AnimatedWelcome()
    app.root.mainloop()

if __name__ == "__main__":
    main()
