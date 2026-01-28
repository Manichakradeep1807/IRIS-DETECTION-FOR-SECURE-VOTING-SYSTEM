#!/usr/bin/env python3
"""
Test script to verify voting system fixes
This script helps identify and resolve common voting authentication errors
"""

import os
import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow: {tf.__version__}")
    except ImportError as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False
    
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        from voting_system import voting_system, show_enhanced_voting_interface
        print("✅ Voting system imports successful")
    except ImportError as e:
        print(f"❌ Voting system import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if required files exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'Main.py',
        'voting_system.py',
        'voting_results.py'
    ]
    
    optional_files = [
        'model/model.json',
        'model/model.weights.h5',
        'testSamples'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_good = False
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file} exists (optional)")
        else:
            print(f"⚠️ {file} missing (optional)")
    
    return all_good

def test_voting_system():
    """Test voting system functionality"""
    print("\n🔍 Testing voting system...")
    
    try:
        from voting_system import voting_system
        
        # Test database initialization
        parties = voting_system.get_parties()
        print(f"✅ Voting system initialized with {len(parties)} parties")
        
        # Test basic functionality
        test_person_id = 999
        if voting_system.has_voted(test_person_id):
            print(f"✅ Vote checking works (person {test_person_id} has voted)")
        else:
            print(f"✅ Vote checking works (person {test_person_id} has not voted)")
        
        return True
        
    except Exception as e:
        print(f"❌ Voting system test failed: {e}")
        traceback.print_exc()
        return False

def test_model_loading():
    """Test if model can be loaded"""
    print("\n🔍 Testing model loading...")
    
    try:
        if os.path.exists('model/model.json') and os.path.exists('model/model.weights.h5'):
            from tensorflow.keras.models import model_from_json
            
            with open('model/model.json', 'r') as json_file:
                loaded_model_json = json_file.read()
                model = model_from_json(loaded_model_json)
            
            model.load_weights('model/model.weights.h5')
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            
            print("✅ Model loaded successfully")
            print(f"   Input shape: {model.input_shape}")
            print(f"   Output shape: {model.output_shape}")
            return True
        else:
            print("⚠️ No trained model found (this is normal if you haven't trained yet)")
            return True
            
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        traceback.print_exc()
        return False

def test_iris_feature_extraction():
    """Test iris feature extraction"""
    print("\n🔍 Testing iris feature extraction...")
    
    try:
        # Check if testSamples directory exists
        if not os.path.exists('testSamples'):
            print("⚠️ testSamples directory not found")
            return True
        
        # Find a test image
        test_images = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            import glob
            test_images.extend(glob.glob(f'testSamples/{ext}'))
            test_images.extend(glob.glob(f'testSamples/**/{ext}', recursive=True))
        
        if not test_images:
            print("⚠️ No test images found in testSamples")
            return True
        
        # Test feature extraction with first image
        test_image = test_images[0]
        print(f"   Testing with: {os.path.basename(test_image)}")
        
        # Import the feature extraction function
        sys.path.append('.')
        from Main import getIrisFeatures
        
        features = getIrisFeatures(test_image)
        if features is not None:
            print(f"✅ Iris feature extraction successful")
            print(f"   Feature shape: {features.shape}")
            return True
        else:
            print("❌ Iris feature extraction returned None")
            return False
            
    except Exception as e:
        print(f"❌ Iris feature extraction test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 VOTING SYSTEM DIAGNOSTIC TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure),
        ("Voting System Test", test_voting_system),
        ("Model Loading Test", test_model_loading),
        ("Iris Feature Extraction Test", test_iris_feature_extraction)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
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
    
    if passed == total:
        print("🎉 All tests passed! The voting system should work correctly.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   • Install missing packages: pip install tensorflow opencv-python numpy")
        print("   • Train a model first using 'TRAIN MODEL' button")
        print("   • Add test images to testSamples folder")
        print("   • Check file permissions and paths")

if __name__ == "__main__":
    main()
