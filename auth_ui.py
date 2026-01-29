import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import threading
from database_manager import db
from security_utils import verify_password_bcrypt
import numpy as np

try:
    import cv2  # webcam support if available
    _CV2_OK = True
except Exception:
    _CV2_OK = False


def show_user_login(on_success):
    win = tk.Toplevel()
    win.title("User Login")
    win.geometry("420x360")
    win.configure(bg="#1a1a2e")
    tk.Label(win, text="USER LOGIN", font=("Segoe UI", 14, "bold"), fg="white", bg="#1a1a2e").pack(pady=12)
    frame = tk.Frame(win, bg="#2d2d44", relief="solid", bd=1)
    frame.pack(fill=tk.X, padx=20, pady=10)
    tk.Label(frame, text="Username", fg="white", bg="#2d2d44").pack(pady=(12, 4))
    e_user = tk.Entry(frame, justify="center"); e_user.pack()
    tk.Label(frame, text="Password", fg="white", bg="#2d2d44").pack(pady=(8, 4))
    e_pwd = tk.Entry(frame, show='*', justify="center"); e_pwd.pack()
    
    # Forgot Creds Links
    link_frame = tk.Frame(frame, bg="#2d2d44")
    link_frame.pack(fill=tk.X, pady=(4,0))
    
    def _forgot_user():
        phone = tk.simpledialog.askstring("Forgot Username", "Enter your registered mobile number:")
        if not phone: return
        try:
            # Find person with this phone
            # We need to search all persons? Or all users?
            # Creating a helper or doing a manual scan if db doesn't support it directly
            # For efficiency we should add get_user_by_phone to db, but here we can try scan
            # assuming small user base
            users = db.get_all_users()
            found_user = None
            for u in users:
                pid = u.get('person_id')
                if pid:
                    p = db.get_person(int(pid))
                    if p and p.get('phone') == phone:
                        found_user = u
                        break
            if found_user:
                messagebox.showinfo("Username Found", f"Your username is: {found_user['username']}")
            else:
                messagebox.showerror("Not Found", "No user found with that mobile number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _forgot_pass():
        u = tk.simpledialog.askstring("Forgot Password", "Enter your username:")
        if not u: return
        user = db.get_user(u)
        if not user:
            messagebox.showerror("Error", "User not found"); return
        
        # Verify identity via phone/biometric
        # Let's ask for phone
        phone = tk.simpledialog.askstring("Forgot Password", "Enter registered mobile number for verification:")
        if not phone: return
        
        try:
            pid = user.get('person_id')
            if not pid:
                messagebox.showerror("Error", "User not linked to profile"); return
            person = db.get_person(int(pid))
            if not person or person.get('phone') != phone:
                messagebox.showerror("Error", "Verification failed"); return
                
            # If verified, store new password
            new_p = tk.simpledialog.askstring("Reset Password", "Enter new password:", show='*')
            if new_p:
                from security_utils import hash_password_bcrypt
                db.update_user_password(u, hash_password_bcrypt(new_p))
                messagebox.showinfo("Success", "Password updated successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Label(link_frame, text="Forgot?", fg="#aaa", bg="#2d2d44", font=("Arial", 8)).pack(side=tk.LEFT)
    tk.Button(link_frame, text="Username", command=_forgot_user, bd=0, fg="#4fc3f7", bg="#2d2d44", font=("Arial", 8, "underline"), activebackground="#2d2d44", cursor="hand2").pack(side=tk.LEFT)
    tk.Label(link_frame, text="|", fg="#aaa", bg="#2d2d44", font=("Arial", 8)).pack(side=tk.LEFT, padx=3)
    tk.Button(link_frame, text="Password", command=_forgot_pass, bd=0, fg="#4fc3f7", bg="#2d2d44", font=("Arial", 8, "underline"), activebackground="#2d2d44", cursor="hand2").pack(side=tk.LEFT)

    err = tk.Label(win, text="", fg="#f44336", bg="#1a1a2e"); err.pack()

    # Face ID state for this dialog session
    face_verified = {'ok': False}

    def _face_vector_from_image(image_bgr):
        try:
            gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY) if _CV2_OK else image_bgr
        except Exception:
            gray = image_bgr
        try:
            if _CV2_OK:
                resized = cv2.resize(gray, (100, 100))
            else:
                # Fallback resize using numpy slicing/pooling if cv2 not available
                h, w = gray.shape[:2]
                sh, sw = max(1, h // 100), max(1, w // 100)
                resized = gray[::sh, ::sw]
                resized = resized[:100, :100]
        except Exception:
            return None
        vec = resized.astype(np.float32).flatten()
        norm = np.linalg.norm(vec) or 1.0
        return (vec / norm).astype(np.float32)

    def _capture_face_vector_with_webcam():
        if not _CV2_OK:
            return None
        cap = None
        try:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                return None
            # Warm up a few frames
            for _ in range(5):
                cap.read()
            ok, frame = cap.read()
            if not ok:
                return None
            return _face_vector_from_image(frame)
        except Exception:
            return None
        finally:
            try:
                if cap is not None:
                    cap.release()
            except Exception:
                pass

    def _capture_face_vector_via_file():
        path = filedialog.askopenfilename(title="Select Face Image", filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not path:
            return None
        try:
            if _CV2_OK:
                img = cv2.imread(path)
                if img is None:
                    return None
                return _face_vector_from_image(img)
            else:
                # Minimal fallback using PIL if available
                try:
                    from PIL import Image
                    img = Image.open(path).convert('L')
                    arr = np.array(img)
                    return _face_vector_from_image(arr)
                except Exception:
                    return None
        except Exception:
            return None

    def _get_linked_person(username: str):
        try:
            u = db.get_user(username)
            pid = (u or {}).get('person_id')
            if not pid:
                return None, None
            person = db.get_person(int(pid))
            return int(pid), person
        except Exception:
            return None, None

    def register_face_id():
        username = e_user.get().strip()
        if not username:
            err.config(text="Enter username to register Face ID"); return
        person_id, person = _get_linked_person(username)
        if not person_id:
            err.config(text="No linked person. Complete enrollment first."); return
        vec = _capture_face_vector_with_webcam()
        if vec is None:
            vec = _capture_face_vector_via_file()
        if vec is None:
            err.config(text="Failed to capture face image"); return
        # Prevent duplicate face enrollment by checking against existing faces
        try:
            existing = db.get_all_persons(active_only=True) or []
            duplicate_found = False
            dup_name = None
            for meta in existing:
                try:
                    pid = meta.get('id')
                    if not pid:
                        continue
                    pfull = db.get_person(int(pid))
                    ft = (pfull or {}).get('face_template')
                    if ft is None:
                        continue
                    a = ft.astype(np.float32); b = vec.astype(np.float32)
                    sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6))
                    if sim >= 0.85:
                        duplicate_found = True
                        dup_name = (pfull or {}).get('name') or 'existing user'
                        break
                except Exception:
                    continue
            if duplicate_found:
                messagebox.showerror("Face ID", "User already exists: face matches {}".format(dup_name))
                return
        except Exception:
            # If check fails, proceed cautiously but inform user
            pass
        try:
            ok = db.update_person(person_id, face_template=vec)
            if ok:
                messagebox.showinfo("Face ID", "Face ID registered successfully")
            else:
                err.config(text="Could not save Face ID")
        except Exception as e:
            err.config(text="Face ID error: " + str(e))

    def verify_face_id():
        username = e_user.get().strip()
        if not username:
            err.config(text="Enter username to verify Face ID"); return
        person_id, person = _get_linked_person(username)
        if not person_id or not person or not person.get('face_template') is not None:
            err.config(text="No Face ID on file. Please register first."); return
        stored_vec = person.get('face_template')
        vec = _capture_face_vector_with_webcam()
        if vec is None:
            vec = _capture_face_vector_via_file()
        if vec is None:
            err.config(text="Failed to capture face image"); return
        try:
            # Cosine similarity threshold
            a = stored_vec.astype(np.float32)
            b = vec.astype(np.float32)
            sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6))
            if sim >= 0.80:  # simple threshold
                face_verified['ok'] = True
                messagebox.showinfo("Face ID", "Face verified (similarity {:.2f})".format(sim))
            else:
                face_verified['ok'] = False
                err.config(text="Face mismatch (similarity {:.2f})".format(sim))
        except Exception as e:
            err.config(text="Verification failed: " + str(e))

    def verify_face_live():
        username = e_user.get().strip()
        if not username:
            err.config(text="Enter username to verify Face ID"); return
        person_id, person = _get_linked_person(username)
        if not person_id or not person or not (person.get('face_template') is not None):
            err.config(text="No Face ID on file. Please register first."); return
        stored_vec = person.get('face_template')
        ok_live = _live_verify_modal(win, stored_vec)
        if ok_live:
            face_verified['ok'] = True
            messagebox.showinfo("Face ID", "Live face verification successful")
        else:
            face_verified['ok'] = False
            err.config(text="Live face verification failed or cancelled")

    def _live_verify_modal(parent, stored_vec: np.ndarray) -> bool:
        # Live webcam verification modal; returns True on sufficient match
        if not _CV2_OK:
            # Fallback to single image selection when webcam unavailable
            path = filedialog.askopenfilename(title="Select Face Image", filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
            if not path:
                return False
            try:
                from PIL import Image
                img = Image.open(path).convert('L')
                arr = np.array(img)
                # Build vector (100x100 normalized)
                h, w = arr.shape[:2]
                sh, sw = max(1, h // 100), max(1, w // 100)
                small = arr[::sh, ::sw][:100, :100]
                v = small.astype(np.float32).flatten(); n = np.linalg.norm(v) or 1.0
                vec = (v / n).astype(np.float32)
                a = stored_vec.astype(np.float32); b = vec.astype(np.float32)
                sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6))
                return sim >= 0.80
            except Exception:
                return False

        modal = tk.Toplevel(parent)
        modal.title("Live Face Verification")
        modal.geometry("680x520")
        modal.configure(bg="#1a1a2e")
        modal.grab_set()
        tk.Label(modal, text="Align your face within the frame", fg="white", bg="#1a1a2e").pack(pady=8)
        sim_var = tk.StringVar(value="Similarity: --")
        tk.Label(modal, textvariable=sim_var, fg="#9ca3af", bg="#1a1a2e").pack()
        video = tk.Label(modal, bg="#000000"); video.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        btns = tk.Frame(modal, bg="#1a1a2e"); btns.pack(pady=8)
        result = {'ok': False}

        def _close():
            try:
                running['v'] = False
                if cap is not None:
                    try:
                        cap.release()
                    except Exception:
                        pass
                if modal.winfo_exists():
                    modal.destroy()
            except Exception:
                pass

        tk.Button(btns, text="Cancel", command=_close, fg="white", bg="#f44336").pack(side=tk.RIGHT, padx=6)

        # Optional PIL for rendering
        try:
            from PIL import Image, ImageTk
            _pil_ok = True
        except Exception:
            _pil_ok = False

        try:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        except Exception:
            cap = None
        if cap is None or not cap.isOpened():
            try:
                if cap is not None:
                    cap.release()
            except Exception:
                pass
            messagebox.showerror("Live Verify", "Cannot access camera")
            try:
                modal.destroy()
            except Exception:
                pass
            return False

        running = {'v': True}
        recent_pass = {'count': 0}

        def _frame_vec(frame_bgr):
            try:
                gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
                small = cv2.resize(gray, (100, 100))
                v = small.astype(np.float32).flatten()
                n = np.linalg.norm(v) or 1.0
                return (v / n).astype(np.float32)
            except Exception:
                return None

        def _tick():
            if not running['v']:
                return
            ok, frame = cap.read()
            if not ok:
                modal.after(50, _tick); return
            vec = _frame_vec(frame)
            sim_text = "Similarity: --"
            if vec is not None:
                try:
                    a = stored_vec.astype(np.float32); b = vec.astype(np.float32)
                    sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6))
                    sim_text = "Similarity: {:.2f}".format(sim)
                    if sim >= 0.80:
                        recent_pass['count'] = min(10, recent_pass['count'] + 1)
                    else:
                        recent_pass['count'] = max(0, recent_pass['count'] - 1)
                    if recent_pass['count'] >= 5:
                        result['ok'] = True
                        _close()
                        return
                except Exception:
                    pass
            sim_var.set(sim_text)
            try:
                if _pil_ok:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w = rgb.shape[:2]
                    scale = min(640 / max(1, w), 360 / max(1, h))
                    rgb = cv2.resize(rgb, (int(w * scale), int(h * scale)))
                    img = Image.fromarray(rgb)
                    tkimg = ImageTk.PhotoImage(img)
                    video.configure(image=tkimg)
                    video.image = tkimg
                else:
                    video.configure(text="Live...", fg="white", bg="#000000")
            except Exception:
                pass
            modal.after(33, _tick)

        def _on_close():
            _close()
        modal.protocol("WM_DELETE_WINDOW", _on_close)
        _tick()
        modal.wait_window()
        return result['ok']

    def do_login():
        u = e_user.get().strip(); p = e_pwd.get()
        # Use db internal authentication which handles hash verification and lockout
        success, msg = db.authenticate_user(u, p, require_totp_if_set=False)
        if not success:
            if msg == 'account_locked':
                err.config(text="Account locked due to too many failed attempts")
            elif msg == 'user_not_found':
                err.config(text="User not found")
            else:
                err.config(text="Invalid credentials")
            return
            
        user = db.get_user(u)
        # If a Face ID is registered for the linked person, require live verification
        try:
            pid = user.get('person_id')
            person = db.get_person(int(pid)) if pid else None
        except Exception:
            person = None
        if person and person.get('face_template') is not None:
            if not _live_verify_modal(win, person.get('face_template')):
                err.config(text="Face verification failed or cancelled"); return
        try:
            if win.winfo_exists():
                win.destroy()
        except Exception:
            pass
        try:
            on_success(user)
        except Exception:
            pass

    # Face ID actions
    face_row = tk.Frame(win, bg="#1a1a2e"); face_row.pack(pady=(6, 0))
    tk.Button(face_row, text="Register Face ID", command=register_face_id, fg="white", bg="#9C27B0").pack(side=tk.LEFT, padx=6)
    tk.Button(face_row, text="Verify Face (Live)", command=verify_face_live, fg="white", bg="#14b8a6").pack(side=tk.LEFT, padx=6)

    btns = tk.Frame(win, bg="#1a1a2e"); btns.pack(pady=10)
    tk.Button(btns, text="Login", command=do_login, fg="white", bg="#4CAF50").pack(side=tk.LEFT, padx=6)
    tk.Button(btns, text="Cancel", command=win.destroy, fg="white", bg="#f44336").pack(side=tk.LEFT, padx=6)
    win.grab_set(); win.wait_window()


def show_admin_login(on_success, iris_verify_func):
    win = tk.Toplevel()
    win.title("Admin Login")
    win.geometry("380x360")
    win.configure(bg="#1a1a2e")
    tk.Label(win, text="ADMIN LOGIN", font=("Segoe UI", 14, "bold"), fg="white", bg="#1a1a2e").pack(pady=12)
    frame = tk.Frame(win, bg="#2d2d44", relief="solid", bd=1)
    frame.pack(fill=tk.X, padx=20, pady=10)
    tk.Label(frame, text="Username", fg="white", bg="#2d2d44").pack(pady=(12, 4))
    e_user = tk.Entry(frame, justify="center"); e_user.pack()
    tk.Label(frame, text="Password", fg="white", bg="#2d2d44").pack(pady=(8, 4))
    e_pwd = tk.Entry(frame, show='*', justify="center"); e_pwd.pack()
    tk.Label(frame, text="TOTP", fg="white", bg="#2d2d44").pack(pady=(8, 4))
    e_totp = tk.Entry(frame, justify="center"); e_totp.pack()
    
    # Forgot Creds Links (Admin)
    link_frame = tk.Frame(frame, bg="#2d2d44")
    link_frame.pack(fill=tk.X, pady=(4,0))
    
    def _forgot_user_admin():
        # Admin recovery might be stricter, but using same phone logic for now
        phone = tk.simpledialog.askstring("Forgot Username", "Enter your registered mobile number:")
        if not phone: return
        try:
            users = db.get_all_users()
            found = None
            for u in users:
                if u.get('role') != 'admin': continue
                pid = u.get('person_id')
                if pid:
                    p = db.get_person(int(pid))
                    if p and p.get('phone') == phone:
                        found = u
                        break
            if found:
                messagebox.showinfo("Username Found", f"Your admin username is: {found['username']}")
            else:
                messagebox.showerror("Not Found", "No admin found with that mobile number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _forgot_pass_admin():
        u = tk.simpledialog.askstring("Forgot Password", "Enter your admin username:")
        if not u: return
        user = db.get_user(u)
        if not user or user.get('role') != 'admin':
            messagebox.showerror("Error", "Admin not found"); return
        
        phone = tk.simpledialog.askstring("Forgot Password", "Enter registered mobile number:")
        if not phone: return
        
        try:
            pid = user.get('person_id')
            if not pid:
                messagebox.showerror("Error", "Account not linked"); return
            person = db.get_person(int(pid))
            if not person or person.get('phone') != phone:
                messagebox.showerror("Error", "Verification failed"); return
            
            # Additional admin check: require Master Key or TOTP Secret hint?
            # For simplicity, just reset
            new_p = tk.simpledialog.askstring("Reset Password", "Enter new password:", show='*')
            if new_p:
                from security_utils import hash_password_bcrypt
                db.update_user_password(u, hash_password_bcrypt(new_p))
                messagebox.showinfo("Success", "Password updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Label(link_frame, text="Forgot?", fg="#aaa", bg="#2d2d44", font=("Arial", 8)).pack(side=tk.LEFT)
    tk.Button(link_frame, text="Username", command=_forgot_user_admin, bd=0, fg="#4fc3f7", bg="#2d2d44", font=("Arial", 8, "underline"), activebackground="#2d2d44", cursor="hand2").pack(side=tk.LEFT)
    tk.Label(link_frame, text="|", fg="#aaa", bg="#2d2d44", font=("Arial", 8)).pack(side=tk.LEFT, padx=3)
    tk.Button(link_frame, text="Password", command=_forgot_pass_admin, bd=0, fg="#4fc3f7", bg="#2d2d44", font=("Arial", 8, "underline"), activebackground="#2d2d44", cursor="hand2").pack(side=tk.LEFT)

    err = tk.Label(win, text="", fg="#f44336", bg="#1a1a2e"); err.pack()

    def do_login_admin():
        u = e_user.get().strip(); p = e_pwd.get(); t = e_totp.get().strip()
        user = db.get_user(u)
        if not user or not verify_password_bcrypt(p, user['password_hash']):
            err.config(text="Invalid credentials"); return
        if user.get('totp_secret'):
            try:
                import pyotp
                if not t or not pyotp.TOTP(user['totp_secret']).verify(t, valid_window=1):
                    err.config(text="Invalid TOTP"); return
            except Exception:
                err.config(text="TOTP error"); return
        if not iris_verify_func(user):
            err.config(text="Iris verification failed"); return
        try:
            if win.winfo_exists():
                win.destroy()
        except Exception:
            pass
        try:
            on_success(user)
        except Exception:
            pass

    def enroll_biometric():
        try:
            from admin_enroll import enroll_admin_biometric
        except Exception:
            messagebox.showerror("Feature Missing", "Enrollment module not available")
            return
        username = e_user.get().strip()
        if not username:
            messagebox.showerror("Username Required", "Enter username first")
            return
        threading.Thread(target=lambda: enroll_admin_biometric(username), daemon=True).start()

    btns = tk.Frame(win, bg="#1a1a2e"); btns.pack(pady=10)
    tk.Button(btns, text="Login", command=do_login_admin, fg="white", bg="#4CAF50").pack(side=tk.LEFT, padx=6)
    tk.Button(btns, text="Enroll Biometric", command=enroll_biometric, fg="white", bg="#9C27B0").pack(side=tk.LEFT, padx=6)
    tk.Button(btns, text="Cancel", command=win.destroy, fg="white", bg="#f44336").pack(side=tk.LEFT, padx=6)
    win.grab_set(); win.wait_window()
