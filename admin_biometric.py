import tkinter as tk
from tkinter import messagebox
import time

def verify_admin_iris(user) -> bool:
    """Run a quick live iris verification for the given admin user.
    Returns True if recognition matches linked person_id with sufficient confidence.
    """
    try:
        from live_recognition import LiveIrisRecognition
        # Some projects expose getIrisFeatures in Main
        try:
            from Main import getIrisFeatures
        except Exception:
            getIrisFeatures = None

        # Load model if available
        model = None
        try:
            import os
            if os.path.exists('model/best_model.h5'):
                from tensorflow import keras
                model = keras.models.load_model('model/best_model.h5')
        except Exception:
            model = None

        # Build recognition system
        recognizer = LiveIrisRecognition(model=model, iris_extractor=getIrisFeatures)
        recognizer.confidence_threshold = 0.75

        # Start camera
        if not recognizer.start_recognition():
            messagebox.showerror("Camera Error", "Unable to start camera for iris verification")
            return False

        target_person_id = user.get('person_id')
        if not target_person_id:
            messagebox.showerror("Not Linked", "Admin account is not linked to a person profile for biometric verification")
            recognizer.stop()
            return False

        # Wait up to 15 seconds for a matching recognition
        end_time = time.time() + 15
        matched = False
        while time.time() < end_time and recognizer.is_running:
            try:
                result = None
                try:
                    result = recognizer.result_queue.get(timeout=0.5)
                except Exception:
                    result = None
                if result and isinstance(result, dict):
                    pid = result.get('person_id')
                    conf = result.get('confidence', 0)
                    if pid == target_person_id and conf >= recognizer.confidence_threshold:
                        matched = True
                        break
            except Exception:
                pass

        recognizer.stop_recognition()
        if not matched:
            messagebox.showwarning("Verification Failed", "Iris did not match the linked admin profile in time")
        return matched
    except Exception:
        messagebox.showerror("Verification Error", "Iris verification is not available on this setup")
        return False


