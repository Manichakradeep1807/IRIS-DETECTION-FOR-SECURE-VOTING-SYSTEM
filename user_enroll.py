
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import PIL.Image, PIL.ImageTk
import time
import threading
import sys
import os
import numpy as np

# Ensure project root is in path
sys.path.append(os.getcwd())

from database_manager import db
try:
    from theme_manager import theme_manager
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False

# Import Biometric Core
try:
    from live_recognition import LiveIrisRecognition
    from biometric_utils import getIrisFeatures
except ImportError:
    LiveIrisRecognition = None
    getIrisFeatures = None

class SuccessPopup(tk.Toplevel):
    def __init__(self, parent, title="Success", message="Action Complete"):
        super().__init__(parent)
        self.configure(bg="#1e293b")
        self.overrideredirect(True) # Frameless
        self.geometry("400x300")
        
        # Center
        x = parent.winfo_rootx() + (parent.winfo_width()//2) - 200
        y = parent.winfo_rooty() + (parent.winfo_height()//2) - 150
        self.geometry(f"+{x}+{y}")
        
        # Animation Canvas
        self.canvas = tk.Canvas(self, bg="#1e293b", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw initial checkmark parts
        self.check_points = [(100, 150), (170, 220), (300, 80)]
        self.drawn_points = []
        self.step = 0
        
        self.message = message
        self.title_text = title
        
        self.after(100, self.animate_check)
        
    def animate_check(self):
        if self.step < 20:
             # Draw partial line 1
             p1 = self.check_points[0]
             p2 = self.check_points[1]
             t = self.step / 10.0
             if t > 1.0: t = 1.0
             
             x = p1[0] + (p2[0] - p1[0]) * t
             y = p1[1] + (p2[1] - p1[1]) * t
             
             self.canvas.create_line(p1[0], p1[1], x, y, width=8, fill="#10b981", capstyle=tk.ROUND)
             
             if self.step >= 10:
                 t2 = (self.step - 10) / 10.0
                 p3 = self.check_points[2]
                 x2 = p2[0] + (p3[0] - p2[0]) * t2
                 y2 = p2[1] + (p3[1] - p2[1]) * t2
                 self.canvas.create_line(p2[0], p2[1], x2, y2, width=8, fill="#10b981", capstyle=tk.ROUND)
                 
             self.step += 1
             self.after(20, self.animate_check)
        else:
             # Show text
             tk.Label(self, text=self.title_text, font=("Segoe UI", 18, "bold"), fg="#10b981", bg="#1e293b").place(relx=0.5, rely=0.7, anchor="center")
             tk.Label(self, text=self.message, font=("Segoe UI", 11), fg="#cbd5e1", bg="#1e293b").place(relx=0.5, rely=0.85, anchor="center")
             # Auto close
             self.after(2000, self.destroy)

class EnrollmentInterface(LiveIrisRecognition):
    def __init__(self, username):
        # 1. Verify User
        self.username = username
        self.user_data = db.get_user(username)
        if not self.user_data:
            messagebox.showerror("Error", f"User {username} not found")
            sys.exit(1)
            
        self.person_id = self.user_data.get('person_id')
        if not self.person_id:
            messagebox.showerror("Error", "User not linked to a person ID")
            sys.exit(1)

        # 2. Initialize UI Root
        self.root = tk.Tk()
        self.root.title(f"Biometric Enrollment - {username}")
        self.root.geometry("800x700")
        
        # Load Theme
        if THEME_AVAILABLE:
            self.colors = theme_manager.get_theme_colors()
            self.fonts = theme_manager.get_theme_fonts()
        else:
            self.colors = {
                'primary': "#0f172a", 'secondary': "#1e293b",
                'accent_primary': "#38bdf8", 'text_primary': "#f8fafc", 'success': "#10b981"
            }
            self.fonts = {"primary": "Segoe UI", "secondary": "Arial"}
            
        self.root.configure(bg=self.colors['primary'])
        
        # 3. Initialize Biometrics Base
        # Load dummy model if needed, but for enrollment we focus on FEATURE EXTRACTION
        # Actually user_enroll previously loaded model. We'll try to load it.
        model = None
        try:
            from tensorflow import keras
            if os.path.exists('model/best_model.h5'):
                model = keras.models.load_model('model/best_model.h5')
        except: pass
        
        super().__init__(model=model, iris_extractor=getIrisFeatures)
        self.show_gallery_window = False # We handle UI ourselves
        self.auto_open_gallery = False

        # State
        self.samples = []
        self.required_samples = 5
        self.is_capturing = False
        self.stop_event = threading.Event()
        
        self.setup_ui()
        self.start_camera()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors['secondary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="IRIS ENROLLMENT", font=(self.fonts['primary'], 18, "bold"),
                 fg=self.colors['accent_primary'], bg=self.colors['secondary']).pack(side=tk.LEFT, padx=30)
                 
        tk.Label(header, text=f"User: {self.username}", font=(self.fonts['primary'], 12),
                 fg=self.colors['text_primary'], bg=self.colors['secondary']).pack(side=tk.RIGHT, padx=30)
        
        # Main Content
        content = tk.Frame(self.root, bg=self.colors['primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Instructions
        tk.Label(content, text="Please center your eye in the green box.", 
                 font=(self.fonts['primary'], 14), fg=self.colors['text_primary'], bg=self.colors['primary']).pack(pady=(0, 20))
        
        # Video Feed
        self.video_frame = tk.Frame(content, bg="black", width=640, height=480)
        self.video_frame.pack()
        self.video_frame.pack_propagate(False)
        
        self.video_label = tk.Label(self.video_frame, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(content, variable=self.progress_var, maximum=self.required_samples)
        self.progress_bar.pack(fill=tk.X, pady=20)
        
        self.status_lbl = tk.Label(content, text="Ready to capture...", font=(self.fonts['primary'], 12),
                                  fg=self.colors['accent_primary'], bg=self.colors['primary'])
        self.status_lbl.pack()
        
        # Cancel Button
        tk.Button(self.root, text="Cancel Enrollment", command=self.close,
                 bg="#ef4444", fg="white", font=(self.fonts['primary'], 11, "bold"),
                 relief="flat", pady=10).pack(fill=tk.X, side=tk.BOTTOM)

    def start_camera(self):
        # Initialize camera from base class logic
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
            
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        self.is_capturing = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        
    def _capture_loop(self):
        last_capture_time = 0
        
        while self.is_capturing and not self.stop_event.is_set():
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01); continue
                
            frame = cv2.flip(frame, 1)
            display_frame = frame.copy()
            
            # Use base class detection
            try:
                # We need eye extraction logic.
                # _process_frame_for_recognition does recognition. We just want detection + extraction.
                # We can reuse _detect_eyes and feature extraction manually.
                
                # Enhance
                enhanced = self._enhance_low_light(frame.copy())
                eyes = self._detect_eyes(enhanced)
                
                # Fallback
                if (eyes is None or len(eyes) == 0):
                    eyes = self._detect_eyes(frame)
                
                status_color = (0, 255, 255) # Yellow
                
                if eyes is not None and len(eyes) > 0:
                    status_color = (0, 255, 0) # Green
                    
                    # Detect Largest
                    (ex, ey, ew, eh) = max(eyes, key=lambda e: e[2] * e[3])
                    cv2.rectangle(display_frame, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                    
                    # Capture Logic
                    current_time = time.time()
                    if (current_time - last_capture_time) > 1.0: # 1 sec interval
                        
                        # Extract Features
                        eye_roi = enhanced[ey:ey+eh, ex:ex+ew]
                        features = self._extract_iris_from_roi(eye_roi)
                        
                        if features is not None and features.size > 0:
                            # Quality Check (Simple)
                            clarity = self._calculate_clarity(features)
                            if clarity > 10.0: # Threshold
                                self.samples.append(features)
                                last_capture_time = current_time
                                
                                # UI Update
                                self.root.after(10, self._update_progress)
                                
                                if len(self.samples) >= self.required_samples:
                                    self.is_capturing = False
                                    self.root.after(10, self._finish_enrollment)
                                    break
            except Exception as e:
                print(f"Error: {e}")

            # Display
            rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            rgb = cv2.resize(rgb, (640, 480))
            img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(rgb))
            self.root.after(10, lambda i=img: self.video_label.configure(image=i))
            self.video_label.image = img # Limit GC
            
            time.sleep(0.01)

    def _calculate_clarity(self, image):
        """Calculate image clarity using Laplacian variance"""
        try:
            if image is None or image.size == 0:
                return 0.0
                
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            return cv2.Laplacian(gray, cv2.CV_64F).var()
        except Exception:
            return 0.0

    def _update_progress(self):
        count = len(self.samples)
        self.progress_var.set(count)
        self.status_lbl.config(text=f"Capturing: {count}/{self.required_samples} samples collected")

    def _finish_enrollment(self):
        self.status_lbl.config(text="Processing Enrollment...", fg=self.colors['accent_primary'])
        
        # Save best sample
        if not self.samples: return
        
        # Default: Use last sample
        best = self.samples[-1]
        
        try:
            # Check duplication
            dup = db.check_duplicate_iris(best)
            if dup and dup != self.person_id:
                messagebox.showerror("Error", "Biometric pattern already registered to another user.")
                self.close()
                return

            db.update_person(self.person_id, iris_template=best, is_active=True)
            
            # Show Animated Success
            popup = SuccessPopup(self.root, title="Enrollment Success!", message="Biometric data securely registered.")
            # Wait for popup to finish (approx 2s) before closing window
            self.root.after(2500, self.close)
            
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")
            self.close()

    def close(self):
        self.is_capturing = False
        self.stop_event.set()
        if hasattr(self, 'cap'): self.cap.release()
        try:
            self.root.destroy()
        except: pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Test mode
        root = tk.Tk(); root.withdraw()
        u = tk.simpledialog.askstring("Enroll", "Username:")
        if u: EnrollmentInterface(u).root.mainloop()
    else:
        EnrollmentInterface(sys.argv[1]).root.mainloop()
