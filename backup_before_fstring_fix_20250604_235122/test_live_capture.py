#!/usr/bin/env python3
"""
Test script to verify live recognition image capture functionality
"""

import os
import cv2
import numpy as np
from datetime import datetime
import time

def test_live_recognition_capture():
    """Test the live recognition image capture process"""
    print("🔍 TESTING LIVE RECOGNITION IMAGE CAPTURE")
    print("=" * 60)
    
    try:
        # Import required modules
        from live_recognition import LiveIrisRecognition
        from Main import getIrisFeatures
        
        print("✅ Modules imported successfully")
        
        # Check if model exists
        model = None
        if os.path.exists('model/best_model.h5'):
            try:
                import tensorflow as tf
                from tensorflow import keras
                model = keras.models.load_model('model/best_model.h5')
                print("✅ Model loaded successfully")
            except Exception as e:
                print(f"⚠️ Could not load model: {e}")
        else:
            print("⚠️ No trained model found")
        
        # Create live recognition instance
        live_system = LiveIrisRecognition(model=model, iris_extractor=getIrisFeatures)
        print("✅ Live recognition system created")
        
        # Test image capture with dummy data
        print("\n🧪 Testing image capture process...")
        
        # Create dummy iris and eye images
        iris_image = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        eye_roi = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Create dummy prediction
        prediction = {
            'person_id': 2,
            'confidence': 0.92
        }
        
        # Count existing images
        capture_folder = "captured_iris"
        existing_files = []
        if os.path.exists(capture_folder):
            existing_files = [f for f in os.listdir(capture_folder) if f.endswith('.jpg')]
        
        print(f"📊 Images before capture: {len(existing_files)}")
        
        # Test the capture method
        live_system._capture_iris_image(iris_image, eye_roi, prediction)
        
        # Check if new image was created
        time.sleep(0.5)  # Give time for file to be written
        
        new_files = []
        if os.path.exists(capture_folder):
            new_files = [f for f in os.listdir(capture_folder) if f.endswith('.jpg')]
        
        print(f"📊 Images after capture: {len(new_files)}")
        
        if len(new_files) > len(existing_files):
            new_image = [f for f in new_files if f not in existing_files][0]
            print(f"✅ New image captured: {new_image}")
            
            # Check file size
            file_path = os.path.join(capture_folder, new_image)
            file_size = os.path.getsize(file_path)
            print(f"📁 File size: {file_size} bytes")
            
            if file_size > 0:
                print("✅ Image file is not empty")
                return True
            else:
                print("❌ Image file is empty")
                return False
        else:
            print("❌ No new image was captured")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def test_gallery_refresh():
    """Test if gallery can detect new images"""
    print("\n🔄 TESTING GALLERY REFRESH FUNCTIONALITY")
    print("=" * 60)
    
    try:
        # Count current images
        capture_folder = "captured_iris"
        if os.path.exists(capture_folder):
            current_files = [f for f in os.listdir(capture_folder) if f.endswith('.jpg')]
            print(f"📊 Current images in gallery: {len(current_files)}")
            
            if current_files:
                print("📋 Current images:")
                for i, filename in enumerate(current_files, 1):
                    file_path = os.path.join(capture_folder, filename)
                    file_size = os.path.getsize(file_path) / 1024  # KB
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    print(f"   {i}. {filename} ({file_size:.1f} KB) - {file_time.strftime('%H:%M:%S')}")
                
                print("✅ Gallery should be able to display these images")
                return True
            else:
                print("⚠️ No images found for gallery to display")
                return False
        else:
            print("❌ Capture folder does not exist")
            return False
            
    except Exception as e:
        print(f"❌ Error testing gallery refresh: {e}")
        return False

def test_main_gallery_integration():
    """Test if the main application gallery function works"""
    print("\n🖼️ TESTING MAIN APPLICATION GALLERY INTEGRATION")
    print("=" * 60)
    
    try:
        # Import the gallery function from Main.py
        import sys
        import tkinter as tk
        
        # Create a dummy root window
        root = tk.Tk()
        root.withdraw()  # Hide it
        
        # Import Main.py functions
        from Main import show_iris_gallery
        
        print("✅ Gallery function imported from Main.py")
        
        # Test if function exists and is callable
        if callable(show_iris_gallery):
            print("✅ Gallery function is callable")
            print("📝 Note: Gallery function is ready to use from main application")
            root.destroy()
            return True
        else:
            print("❌ Gallery function is not callable")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"❌ Error testing main gallery integration: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 LIVE RECOGNITION IMAGE CAPTURE TEST SUITE")
    print("=" * 60)
    print("This test verifies that images are being captured and stored")
    print("correctly during live recognition sessions.")
    print("=" * 60)
    
    # Run tests
    test1_result = test_live_recognition_capture()
    test2_result = test_gallery_refresh()
    test3_result = test_main_gallery_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Live Capture Process:     {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Gallery Refresh:          {'✅ PASS' if test2_result else '❌ FAIL'}")
    print(f"Main App Integration:     {'✅ PASS' if test3_result else '❌ FAIL'}")
    
    if test1_result and test2_result and test3_result:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Image capture system is working correctly")
        print("✅ Gallery can display captured images")
        print("✅ Main application integration is ready")
        print("\n💡 TROUBLESHOOTING TIPS:")
        print("   1. Make sure to run live recognition to capture new images")
        print("   2. Images are only captured when iris is successfully recognized")
        print("   3. Check the 'captured_iris' folder for saved images")
        print("   4. Use the gallery refresh button if images don't appear immediately")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("There may be issues with the image capture or gallery system")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
