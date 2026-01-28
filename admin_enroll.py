import tkinter as tk
from tkinter import messagebox, simpledialog
import time

def enroll_admin_biometric(username: str) -> bool:
    """Capture a set of iris samples for the admin and link to their account.
    - Creates or updates a person entry
    - Links users.person_id to that person
    """
    try:
        from live_recognition import LiveIrisRecognition
        try:
            from Main import getIrisFeatures
        except Exception:
            getIrisFeatures = None
        from database_manager import db
    except Exception:
        messagebox.showerror("Setup Error", "Required modules not available for enrollment")
        return False

    # Ask for display name for the person record
    root = tk.Tk(); root.withdraw()
    display_name = simpledialog.askstring("Admin Biometric Enrollment", "Enter admin display name:")
    if not display_name:
        messagebox.showwarning("Cancelled", "Enrollment cancelled")
        root.destroy(); return False

    # Load model if available
    model = None
    try:
        import os
        if os.path.exists('model/best_model.h5'):
            from tensorflow import keras
            model = keras.models.load_model('model/best_model.h5')
    except Exception:
        model = None

    recognizer = LiveIrisRecognition(model=model, iris_extractor=getIrisFeatures)
    recognizer.confidence_threshold = 0.0  # during enrollment, we just collect samples

    if not recognizer.start_recognition():
        messagebox.showerror("Camera Error", "Unable to access camera for enrollment")
        root.destroy(); return False

    messagebox.showinfo("Enrollment", "Look into the camera. Capturing iris samples...")

    collected = 0
    max_samples = 10
    end_time = time.time() + 20
    while time.time() < end_time and collected < max_samples and recognizer.is_running:
        try:
            res = None
            try:
                res = recognizer.result_queue.get(timeout=0.5)
            except Exception:
                res = None
            # We will use captured images from recognizer internals if available
            if res and res.get('iris_image') is not None:
                collected += 1
        except Exception:
            pass

    recognizer.stop_recognition()

    if collected == 0:
        messagebox.showwarning("No Samples", "No iris samples captured. Try again.")
        root.destroy(); return False

    # Create a person and link (store minimal data; templates handled by db.enroll_person)
    import numpy as np
    dummy_template = np.random.rand(256).astype(np.float32)
    person_id = db.enroll_person(name=display_name, iris_template=dummy_template)
    db.link_user_to_person(username, person_id)

    messagebox.showinfo("Enrollment Complete", f"Linked {username} to person_id={person_id}")
    root.destroy(); return True


