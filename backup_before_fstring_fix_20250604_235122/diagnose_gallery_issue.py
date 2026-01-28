#!/usr/bin/env python3
"""
Simple diagnostic script to identify gallery storage issues
"""

import os
import cv2
import numpy as np
from datetime import datetime
import time

def create_test_images():
    """Create some test images to verify gallery functionality"""
    print("🧪 CREATING TEST IMAGES FOR GALLERY")
    print("=" * 50)
    
    capture_folder = "captured_iris"
    
    # Ensure folder exists
    os.makedirs(capture_folder, exist_ok=True)
    print(f"✅ Folder created/verified: {capture_folder}")
    
    # Create 3 test images
    for i in range(1, 4):
        # Create a test composite image
        composite = np.zeros((200, 400, 3), dtype=np.uint8)
        
        # Add some visual content
        cv2.rectangle(composite, (10, 10), (190, 190), (0, 255, 0), 2)
        cv2.rectangle(composite, (210, 10), (390, 190), (255, 0, 0), 2)
        
        # Add text
        cv2.putText(composite, f"Test Person {i}", (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(composite, f"Confidence: 0.{85+i}", (20, 80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(composite, "Eye Region", (20, 170), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv2.putText(composite, "Extracted Iris", (220, 170), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        filename = f"{capture_folder}/iris_person{i}_{timestamp}_test.jpg"
        
        # Save image
        cv2.imwrite(filename, composite)
        print(f"✅ Created: {os.path.basename(filename)}")
        
        # Small delay to ensure different timestamps
        time.sleep(0.1)
    
    return True

def test_gallery_detection():
    """Test if gallery can detect and list images"""
    print("\n🔍 TESTING GALLERY IMAGE DETECTION")
    print("=" * 50)
    
    capture_folder = "captured_iris"
    
    if not os.path.exists(capture_folder):
        print(f"❌ Folder does not exist: {capture_folder}")
        return False
    
    # Get all image files
    image_files = []
    for file in os.listdir(capture_folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_files.append(os.path.join(capture_folder, file))
    
    print(f"📊 Found {len(image_files)} image files:")
    
    if not image_files:
        print("❌ No images found in gallery folder")
        return False
    
    # List all images with details
    for i, img_path in enumerate(image_files, 1):
        filename = os.path.basename(img_path)
        file_size = os.path.getsize(img_path)
        file_time = datetime.fromtimestamp(os.path.getmtime(img_path))
        
        print(f"   {i}. {filename}")
        print(f"      Size: {file_size} bytes ({file_size/1024:.1f} KB)")
        print(f"      Modified: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Verify image can be read
        try:
            img = cv2.imread(img_path)
            if img is not None:
                h, w, c = img.shape
                print(f"      Dimensions: {w}x{h}x{c}")
                print(f"      ✅ Image is readable")
            else:
                print(f"      ❌ Image cannot be read")
        except Exception as e:
            print(f"      ❌ Error reading image: {e}")
        
        print()
    
    return True

def test_main_gallery_function():
    """Test the main application gallery function"""
    print("🖼️ TESTING MAIN APPLICATION GALLERY FUNCTION")
    print("=" * 50)
    
    try:
        import tkinter as tk
        
        # Create a test root window
        root = tk.Tk()
        root.withdraw()  # Hide it
        
        # Try to import the gallery function
        from Main import show_iris_gallery
        
        print("✅ Gallery function imported successfully")
        print("📝 Function is available in Main.py")
        
        # Clean up
        root.destroy()
        
        return True
        
    except ImportError as e:
        print(f"❌ Could not import gallery function: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing gallery function: {e}")
        return False

def test_live_recognition_integration():
    """Test if live recognition can capture images"""
    print("\n📹 TESTING LIVE RECOGNITION INTEGRATION")
    print("=" * 50)
    
    try:
        # Count existing images
        capture_folder = "captured_iris"
        existing_files = []
        if os.path.exists(capture_folder):
            existing_files = [f for f in os.listdir(capture_folder) if f.endswith('.jpg')]
        
        print(f"📊 Current images: {len(existing_files)}")
        
        # Try to import live recognition
        from live_recognition import LiveIrisRecognition
        print("✅ Live recognition module imported")
        
        # Create instance without model (for testing)
        live_system = LiveIrisRecognition()
        print("✅ Live recognition instance created")
        
        # Test capture method with dummy data
        iris_image = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        eye_roi = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        prediction = {'person_id': 99, 'confidence': 0.95}
        
        # Capture image
        live_system._capture_iris_image(iris_image, eye_roi, prediction)
        
        # Check if new image was created
        time.sleep(0.5)
        new_files = []
        if os.path.exists(capture_folder):
            new_files = [f for f in os.listdir(capture_folder) if f.endswith('.jpg')]
        
        if len(new_files) > len(existing_files):
            print("✅ Live recognition can capture images")
            new_image = [f for f in new_files if f not in existing_files][0]
            print(f"   New image: {new_image}")
            return True
        else:
            print("❌ Live recognition did not capture new image")
            return False
            
    except Exception as e:
        print(f"❌ Error testing live recognition: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🔧 IRIS GALLERY DIAGNOSTIC TOOL")
    print("=" * 60)
    print("This tool diagnoses issues with iris image storage and gallery display")
    print("=" * 60)
    
    # Run tests
    test1 = create_test_images()
    test2 = test_gallery_detection()
    test3 = test_main_gallery_function()
    test4 = test_live_recognition_integration()
    
    # Summary
    print("=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"Test Image Creation:      {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Gallery Image Detection:  {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Main Gallery Function:    {'✅ PASS' if test3 else '❌ FAIL'}")
    print(f"Live Recognition Capture: {'✅ PASS' if test4 else '❌ FAIL'}")
    
    if all([test1, test2, test3, test4]):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Gallery system is working correctly")
        print("\n💡 NEXT STEPS:")
        print("   1. Run the main application: python Main.py")
        print("   2. Click '🖼️ IRIS GALLERY' to view test images")
        print("   3. Start live recognition to capture real iris images")
        print("   4. Images will appear in the gallery automatically")
    else:
        print("\n⚠️ SOME ISSUES DETECTED")
        print("Check the failed tests above for specific problems")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
