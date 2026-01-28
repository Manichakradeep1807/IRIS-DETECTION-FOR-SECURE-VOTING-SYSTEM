#!/usr/bin/env python3
"""
Verify Iris Capture Features
Quick test to verify the new image capture functionality
"""

import os
import cv2
import numpy as np

def test_capture_folder_creation():
    """Test if capture folder is created"""
    print("🔍 Testing capture folder creation...")
    
    try:
        from live_recognition import LiveIrisRecognition
        
        # Create instance
        live_system = LiveIrisRecognition()
        
        # Check if folder was created
        if os.path.exists('captured_iris'):
            print("✅ Capture folder created successfully")
            return True
        else:
            print("❌ Capture folder not created")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_image_capture_method():
    """Test the image capture method"""
    print("\n🔍 Testing image capture method...")
    
    try:
        from live_recognition import LiveIrisRecognition
        
        # Create instance
        live_system = LiveIrisRecognition()
        
        # Create dummy iris and eye images
        iris_image = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        eye_roi = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Create dummy prediction
        prediction = {
            'person_id': 1,
            'confidence': 0.85
        }
        
        # Test capture method
        live_system._capture_iris_image(iris_image, eye_roi, prediction)
        
        # Check if file was created
        if os.path.exists('captured_iris'):
            files = [f for f in os.listdir('captured_iris') if f.endswith('.jpg')]
            if files:
                print(f"✅ Image capture method works - {len(files)} file(s) created")
                print(f"   Latest file: {files[-1]}")
                return True
        
        print("❌ No image files created")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_display_methods():
    """Test the display methods"""
    print("\n🔍 Testing display methods...")
    
    try:
        from live_recognition import LiveIrisRecognition
        
        # Create instance
        live_system = LiveIrisRecognition()
        
        # Test toggle method
        live_system._toggle_iris_window()
        print("✅ Toggle iris window method works")
        
        # Test show captured images (should handle empty list gracefully)
        live_system._show_captured_images()
        print("✅ Show captured images method works")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_new_features():
    """Show the new features that were added"""
    print("\n" + "="*60)
    print("🆕 NEW IRIS CAPTURE FEATURES ADDED")
    print("="*60)
    
    features = [
        {
            "name": "📸 Automatic Image Capture",
            "description": "Captures iris images automatically when recognition occurs",
            "location": "_capture_iris_image() method"
        },
        {
            "name": "👁️ Real-time Display Window",
            "description": "Shows captured iris in separate 'Captured Iris' window",
            "location": "_update_iris_display() method"
        },
        {
            "name": "🖼️ Composite Images",
            "description": "Creates images showing both eye region and extracted iris",
            "location": "Saved in captured_iris/ folder"
        },
        {
            "name": "🔍 Grid View",
            "description": "View all captured images in a grid layout",
            "location": "_show_captured_images() method"
        },
        {
            "name": "⚙️ Toggle Controls",
            "description": "Press 'i' to toggle iris window on/off",
            "location": "_toggle_iris_window() method"
        },
        {
            "name": "📁 Organized Storage",
            "description": "All images saved with person ID and timestamp",
            "location": "captured_iris/ folder"
        }
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"\n{i}. {feature['name']}")
        print(f"   {feature['description']}")
        print(f"   Location: {feature['location']}")
    
    print(f"\n🎮 NEW KEYBOARD CONTROLS:")
    print(f"   'i' → Toggle iris capture window ON/OFF")
    print(f"   'c' → View all captured iris images in grid")
    
    print(f"\n💾 FILE STORAGE:")
    print(f"   Folder: captured_iris/")
    print(f"   Format: iris_person[ID]_[timestamp].jpg")
    print(f"   Content: Composite image with eye region + extracted iris")

def main():
    """Main verification function"""
    print("🧪 IRIS CAPTURE FEATURES VERIFICATION")
    print("="*60)
    
    tests = [
        ("Capture Folder Creation", test_capture_folder_creation),
        ("Image Capture Method", test_image_capture_method),
        ("Display Methods", test_display_methods)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))
    
    # Show results
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    # Show new features
    show_new_features()
    
    print("\n" + "="*60)
    print("🎯 HOW TO USE THE NEW FEATURES")
    print("="*60)
    
    print("""
1. 🚀 Start live recognition from the main application
2. 👁️ Position your eye in front of the camera
3. 📸 When recognition occurs, iris image is automatically captured
4. 🖼️ Check the 'Captured Iris' window for real-time display
5. 🎮 Use new keyboard controls:
   - Press 'i' to toggle the iris window
   - Press 'c' to view all captured images
6. 📁 Find saved images in the 'captured_iris/' folder

💡 Each captured image shows:
   - Original eye region (left side)
   - Extracted iris features (right side)
   - Person ID and confidence score
   - Timestamp information
""")
    
    if passed == len(results):
        print("🎉 All tests passed! The iris capture features are ready to use.")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()
