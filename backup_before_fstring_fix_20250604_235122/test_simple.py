"""
Simple test to check if basic imports work
"""

print("Testing basic imports...")

try:
    import tkinter as tk
    print("✅ tkinter imported")
except Exception as e:
    print(f"❌ tkinter error: {e}")

try:
    import numpy as np
    print("✅ numpy imported")
except Exception as e:
    print(f"❌ numpy error: {e}")

try:
    import tensorflow as tf
    print("✅ tensorflow imported")
except Exception as e:
    print(f"❌ tensorflow error: {e}")

try:
    import cv2
    print("✅ opencv imported")
except Exception as e:
    print(f"❌ opencv error: {e}")

try:
    import pickle
    print("✅ pickle imported")
except Exception as e:
    print(f"❌ pickle error: {e}")

try:
    from datetime import datetime
    print("✅ datetime imported")
except Exception as e:
    print(f"❌ datetime error: {e}")

print("\nTesting simple GUI...")

try:
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("400x300")
    
    label = tk.Label(root, text="Test GUI Window", font=('Arial', 16))
    label.pack(pady=50)
    
    button = tk.Button(root, text="Close", command=root.destroy)
    button.pack(pady=20)
    
    print("✅ GUI created successfully")
    print("GUI window should appear - close it to continue")
    
    root.mainloop()
    
    print("✅ GUI test completed")
    
except Exception as e:
    print(f"❌ GUI error: {e}")
    import traceback
    traceback.print_exc()

print("\nAll tests completed!")
