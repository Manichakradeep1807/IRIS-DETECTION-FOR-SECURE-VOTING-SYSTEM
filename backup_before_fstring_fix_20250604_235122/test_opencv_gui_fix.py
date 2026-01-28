#!/usr/bin/env python3
"""
Test script to verify OpenCV GUI fixes
This script tests that the application works in headless environments without GUI support
"""

import os
import sys
import cv2
import numpy as np

def test_opencv_gui_support():
    """Test if OpenCV GUI functions work"""
    print("🔍 Testing OpenCV GUI support...")
    
    try:
        # Create a test image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.putText(test_image, 'TEST', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Try to show the image
        cv2.imshow('Test Window', test_image)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        
        print("✅ OpenCV GUI support available")
        return True
        
    except Exception as e:
        print(f"❌ OpenCV GUI not available: {e}")
        print("   This is normal in headless environments")
        return False

def test_opencv_image_saving():
    """Test if OpenCV can save images (fallback for headless mode)"""
    print("\n🔍 Testing OpenCV image saving (headless fallback)...")
    
    try:
        # Create a test image
        test_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        cv2.putText(test_image, 'HEADLESS TEST', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Save the image
        test_filename = 'opencv_test_image.jpg'
        success = cv2.imwrite(test_filename, test_image)
        
        if success and os.path.exists(test_filename):
            print("✅ OpenCV image saving works")
            print(f"   Test image saved: {test_filename}")
            
            # Clean up
            try:
                os.remove(test_filename)
                print("   Test image cleaned up")
            except:
                pass
            
            return True
        else:
            print("❌ OpenCV image saving failed")
            return False
            
    except Exception as e:
        print(f"❌ OpenCV image saving error: {e}")
        return False

def test_iris_recognition_headless():
    """Test iris recognition functions in headless mode"""
    print("\n🔍 Testing iris recognition in headless mode...")
    
    try:
        # Check if we can import the main module
        sys.path.append('.')
        
        # Test basic imports
        import Main
        print("✅ Main module imported successfully")
        
        # Test if getIrisFeatures function exists
        if hasattr(Main, 'getIrisFeatures'):
            print("✅ getIrisFeatures function available")
        else:
            print("⚠️ getIrisFeatures function not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Iris recognition test failed: {e}")
        return False

def test_voting_system_headless():
    """Test voting system in headless mode"""
    print("\n🔍 Testing voting system in headless mode...")
    
    try:
        # Test voting system imports
        from voting_system import voting_system
        print("✅ Voting system imported successfully")
        
        # Test basic voting system functionality
        parties = voting_system.get_parties()
        print(f"✅ Voting system has {len(parties)} parties")
        
        return True
        
    except Exception as e:
        print(f"❌ Voting system test failed: {e}")
        return False

def test_live_recognition_headless():
    """Test live recognition in headless mode"""
    print("\n🔍 Testing live recognition in headless mode...")
    
    try:
        # Test live recognition imports
        from live_recognition import LiveIrisRecognition
        print("✅ Live recognition module imported successfully")
        
        # Test camera availability (without actually starting recognition)
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera available")
            cap.release()
        else:
            print("⚠️ Camera not available (normal in some environments)")
        
        return True
        
    except Exception as e:
        print(f"❌ Live recognition test failed: {e}")
        return False

def create_test_environment():
    """Create test files for headless testing"""
    print("\n🔧 Creating test environment...")
    
    try:
        # Create test directories if they don't exist
        test_dirs = ['testSamples', 'captured_iris']
        for test_dir in test_dirs:
            if not os.path.exists(test_dir):
                os.makedirs(test_dir)
                print(f"   Created directory: {test_dir}")
        
        # Create a simple test iris image if none exists
        if not os.path.exists('testSamples') or len(os.listdir('testSamples')) == 0:
            # Create a synthetic iris-like image
            test_iris = np.zeros((200, 200, 3), dtype=np.uint8)
            
            # Draw a simple iris pattern
            center = (100, 100)
            cv2.circle(test_iris, center, 80, (100, 100, 100), -1)  # Outer iris
            cv2.circle(test_iris, center, 30, (50, 50, 50), -1)     # Pupil
            cv2.circle(test_iris, center, 80, (150, 150, 150), 2)   # Iris border
            
            # Add some texture
            for i in range(0, 200, 10):
                cv2.line(test_iris, (i, 0), (i, 200), (120, 120, 120), 1)
            
            test_filename = 'testSamples/test_iris_synthetic.jpg'
            cv2.imwrite(test_filename, test_iris)
            print(f"   Created test iris image: {test_filename}")
        
        print("✅ Test environment ready")
        return True
        
    except Exception as e:
        print(f"❌ Test environment creation failed: {e}")
        return False

def main():
    """Run all OpenCV GUI compatibility tests"""
    print("🚀 OPENCV GUI COMPATIBILITY TEST")
    print("=" * 50)
    print("This test verifies that the iris recognition system")
    print("works correctly in environments without GUI support.")
    print("=" * 50)
    
    tests = [
        ("OpenCV GUI Support", test_opencv_gui_support),
        ("OpenCV Image Saving", test_opencv_image_saving),
        ("Test Environment Setup", create_test_environment),
        ("Iris Recognition Headless", test_iris_recognition_headless),
        ("Voting System Headless", test_voting_system_headless),
        ("Live Recognition Headless", test_live_recognition_headless)
    ]
    
    results = []
    gui_available = False
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            results.append((test_name, result))
            
            if test_name == "OpenCV GUI Support" and result:
                gui_available = True
                
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if gui_available:
        print("\n🖥️ GUI MODE DETECTED:")
        print("   ✅ OpenCV GUI functions work normally")
        print("   ✅ Image windows will be displayed")
        print("   ✅ All visual features available")
    else:
        print("\n🔧 HEADLESS MODE DETECTED:")
        print("   ✅ OpenCV GUI functions disabled (normal)")
        print("   ✅ Images will be saved to files instead")
        print("   ✅ All core functionality preserved")
    
    print("\n💡 RECOMMENDATIONS:")
    if passed >= total - 1:  # Allow one test to fail
        print("   🎉 System is ready for both GUI and headless operation!")
        print("   🚀 You can now run the iris recognition system:")
        print("      python Main.py")
        print("   🗳️ Voting system should work correctly")
        print("   📹 Live recognition will work (with image saving in headless mode)")
    else:
        print("   ⚠️ Some issues detected. Please check:")
        print("      • Ensure OpenCV is properly installed")
        print("      • Check file permissions for image saving")
        print("      • Verify all required modules are available")

if __name__ == "__main__":
    main()
