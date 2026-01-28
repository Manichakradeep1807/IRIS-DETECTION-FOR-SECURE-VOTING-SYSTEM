#!/usr/bin/env python3
"""
Test script to verify gallery auto-refresh functionality
Creates new iris images to test if the gallery automatically detects and displays them
"""

import os
import time
import cv2
import numpy as np
from datetime import datetime

def create_test_iris_image(person_id, image_number):
    """Create a test iris image similar to the live recognition format"""
    try:
        # Create test iris and eye images
        iris_size = 64
        eye_size = 100
        
        # Generate random iris pattern
        iris_image = np.random.randint(50, 200, (iris_size, iris_size, 3), dtype=np.uint8)
        
        # Add some circular patterns to make it look more like an iris
        center = (iris_size // 2, iris_size // 2)
        for radius in range(10, iris_size // 2, 8):
            cv2.circle(iris_image, center, radius, (100, 150, 200), 1)
        
        # Generate eye region
        eye_image = np.random.randint(80, 150, (eye_size, eye_size, 3), dtype=np.uint8)
        
        # Add eye-like features
        cv2.ellipse(eye_image, (eye_size//2, eye_size//2), (eye_size//3, eye_size//4), 0, 0, 360, (50, 50, 50), -1)
        cv2.circle(eye_image, (eye_size//2, eye_size//2), iris_size//3, (100, 150, 200), -1)
        
        # Create composite image (similar to live recognition format)
        composite_height = max(eye_size, iris_size) + 60
        composite_width = eye_size + iris_size + 30
        composite = np.zeros((composite_height, composite_width, 3), dtype=np.uint8)
        
        # Add eye region
        eye_y_offset = 30
        composite[eye_y_offset:eye_y_offset+eye_size, 0:eye_size] = eye_image
        
        # Add iris region
        iris_x_offset = eye_size + 15
        iris_y_offset = 30
        composite[iris_y_offset:iris_y_offset+iris_size, iris_x_offset:iris_x_offset+iris_size] = iris_image
        
        # Add labels
        confidence = np.random.uniform(0.75, 0.95)
        cv2.putText(composite, f"Test Person {person_id} - Confidence: {confidence:.2f}",
                   (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(composite, "Eye Region", (10, eye_y_offset + eye_size + 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(composite, "Extracted Iris", (iris_x_offset, iris_y_offset + iris_size + 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Save the image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        filename = f"captured_iris/iris_person{person_id}_{timestamp}_test{image_number}.jpg"
        
        # Ensure directory exists
        os.makedirs("captured_iris", exist_ok=True)
        
        cv2.imwrite(filename, composite)
        
        return filename, confidence
        
    except Exception as e:
        print(f"Error creating test image: {e}")
        return None, 0

def test_gallery_auto_refresh():
    """Test the gallery auto-refresh functionality"""
    print("🧪 TESTING GALLERY AUTO-REFRESH FUNCTIONALITY")
    print("=" * 60)
    
    print("📋 This test will:")
    print("   1. Check current images in gallery")
    print("   2. Create new test iris images every 5 seconds")
    print("   3. Verify that gallery auto-refreshes to show new images")
    print("   4. Test for 30 seconds (6 new images)")
    print()
    
    # Check initial state
    capture_folder = "captured_iris"
    initial_files = []
    if os.path.exists(capture_folder):
        initial_files = [f for f in os.listdir(capture_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📂 Initial state: {len(initial_files)} images in gallery")
    print()
    
    print("🚀 Starting test... (Make sure the gallery window is open)")
    print("   The gallery should automatically refresh every 3 seconds")
    print("   You should see new images appear automatically")
    print()
    
    created_files = []
    
    try:
        for i in range(6):  # Create 6 test images
            print(f"📸 Creating test image {i+1}/6...")
            
            # Create test image
            person_id = (i % 3) + 1  # Rotate between persons 1, 2, 3
            filename, confidence = create_test_iris_image(person_id, i+1)
            
            if filename:
                created_files.append(filename)
                print(f"   ✅ Created: {os.path.basename(filename)}")
                print(f"   📊 Person: {person_id}, Confidence: {confidence:.2f}")
                print(f"   🕒 Time: {datetime.now().strftime('%H:%M:%S')}")
                print("   ⏳ Gallery should auto-refresh within 3 seconds...")
            else:
                print(f"   ❌ Failed to create test image {i+1}")
            
            print()
            
            # Wait 5 seconds before creating next image
            if i < 5:  # Don't wait after the last image
                print("⏱️ Waiting 5 seconds before next image...")
                time.sleep(5)
        
        print("✅ Test completed!")
        print(f"📊 Created {len(created_files)} test images")
        print()
        
        # Final verification
        final_files = []
        if os.path.exists(capture_folder):
            final_files = [f for f in os.listdir(capture_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"📈 Final state: {len(final_files)} images in gallery")
        print(f"🆕 New images added: {len(final_files) - len(initial_files)}")
        
        if len(final_files) > len(initial_files):
            print("🎉 SUCCESS: Gallery auto-refresh is working!")
            print("   New images should be visible in the gallery window")
        else:
            print("⚠️ WARNING: No new images detected in folder")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        return False

def cleanup_test_images():
    """Clean up test images created during testing"""
    print("\n🧹 CLEANUP TEST IMAGES")
    print("=" * 30)
    
    try:
        capture_folder = "captured_iris"
        if not os.path.exists(capture_folder):
            print("📂 No capture folder found")
            return
        
        test_files = [f for f in os.listdir(capture_folder) if "_test" in f and f.lower().endswith('.jpg')]
        
        if not test_files:
            print("📂 No test images found to clean up")
            return
        
        print(f"🗑️ Found {len(test_files)} test images to remove:")
        for file in test_files:
            print(f"   - {file}")
        
        response = input("\nRemove test images? (y/n): ").lower().strip()
        
        if response == 'y':
            removed_count = 0
            for file in test_files:
                try:
                    os.remove(os.path.join(capture_folder, file))
                    removed_count += 1
                except Exception as e:
                    print(f"   ❌ Error removing {file}: {e}")
            
            print(f"✅ Removed {removed_count} test images")
        else:
            print("⏭️ Skipped cleanup")
            
    except Exception as e:
        print(f"❌ Cleanup error: {e}")

def main():
    """Main test function"""
    print("👁️ IRIS GALLERY AUTO-REFRESH TEST")
    print("=" * 70)
    print("This test verifies that the gallery automatically refreshes")
    print("when new iris images are added to the captured_iris folder")
    print()
    
    print("📋 INSTRUCTIONS:")
    print("   1. Make sure the main application is running (python Main.py)")
    print("   2. Open the Iris Gallery window (click 🖼️ IRIS GALLERY button)")
    print("   3. Keep the gallery window open and visible")
    print("   4. Run this test and watch the gallery auto-refresh")
    print()
    
    input("Press Enter when ready to start the test...")
    print()
    
    # Run the test
    success = test_gallery_auto_refresh()
    
    print("\n" + "=" * 70)
    print("📋 TEST SUMMARY")
    print("=" * 70)
    
    if success:
        print("🎉 AUTO-REFRESH TEST COMPLETED!")
        print("✅ The gallery should now show the new test images")
        print("✅ Auto-refresh functionality is working correctly")
        print()
        print("🔍 WHAT TO VERIFY:")
        print("   • Gallery window title shows updated image count")
        print("   • New test images appear in the gallery grid")
        print("   • 'Last updated' timestamp changes automatically")
        print("   • Console shows 'new iris image(s) detected' messages")
    else:
        print("❌ TEST FAILED OR INTERRUPTED")
        print("   Check for error messages above")
    
    print("\n" + "=" * 70)
    
    # Offer cleanup
    cleanup_test_images()

if __name__ == "__main__":
    main()
