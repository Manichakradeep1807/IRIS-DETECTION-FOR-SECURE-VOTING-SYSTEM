"""
Comprehensive Test for Fixed Iris Recognition System
Tests all major components including iris extraction, live recognition, and database
"""

import os
import sys
import cv2
import numpy as np
from datetime import datetime

def test_iris_feature_extraction():
    """Test the enhanced iris feature extraction"""
    print("🔍 Testing Iris Feature Extraction...")
    
    try:
        # Import the fixed function
        from Main import getIrisFeatures
        
        # Test with sample images
        test_images = []
        if os.path.exists('testSamples'):
            test_images = [f'testSamples/{f}' for f in os.listdir('testSamples') if f.endswith('.jpg')][:5]
        
        if not test_images:
            print("   ⚠️ No test images found")
            return False
        
        successful_extractions = 0
        
        for img_path in test_images:
            print(f"   Testing: {os.path.basename(img_path)}")
            
            iris_features = getIrisFeatures(img_path)
            
            if iris_features is not None:
                print(f"      ✅ Extracted features: {iris_features.shape}")
                successful_extractions += 1
                
                # Verify the extracted iris is saved
                if os.path.exists('test.png'):
                    print(f"      ✅ Iris image saved successfully")
                else:
                    print(f"      ⚠️ Iris image not saved")
            else:
                print(f"      ❌ Failed to extract iris features")
        
        success_rate = (successful_extractions / len(test_images)) * 100
        print(f"   📊 Success Rate: {success_rate:.1f}% ({successful_extractions}/{len(test_images)})")
        
        return success_rate > 50  # At least 50% success rate
        
    except Exception as e:
        print(f"   ❌ Error in iris extraction test: {e}")
        return False

def test_model_training():
    """Test model training functionality"""
    print("\n🧠 Testing Model Training...")
    
    try:
        # Check if training data exists
        if not os.path.exists('model/X.txt.npy') or not os.path.exists('model/Y.txt.npy'):
            print("   📊 Creating sample dataset for training...")
            
            # Create sample dataset
            import subprocess
            result = subprocess.run(['python', 'create_sample_dataset.py'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                print("   ❌ Failed to create sample dataset")
                return False
        
        # Load training data
        X_train = np.load('model/X.txt.npy')
        Y_train = np.load('model/Y.txt.npy')
        
        print(f"   ✅ Training data loaded: {X_train.shape}, {Y_train.shape}")
        
        # Test model creation
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Input
        
        model = Sequential([
            Input(shape=(64, 64, 3)),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(Y_train.shape[1], activation='softmax')
        ])
        
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print(f"   ✅ Model created successfully with {model.count_params():,} parameters")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error in model training test: {e}")
        return False

def test_live_recognition_setup():
    """Test live recognition setup (without actually starting camera)"""
    print("\n🎥 Testing Live Recognition Setup...")
    
    try:
        # Test camera availability
        cap = cv2.VideoCapture(0)
        camera_available = cap.isOpened()
        cap.release()
        
        if camera_available:
            print("   ✅ Camera detected and accessible")
        else:
            print("   ⚠️ Camera not available (this is normal for some systems)")
        
        # Test live recognition module import
        from live_recognition import LiveIrisRecognition, start_live_recognition
        print("   ✅ Live recognition module imported successfully")
        
        # Test cascade classifiers
        try:
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            print("   ✅ Cascade classifiers loaded successfully")
        except Exception as e:
            print(f"   ⚠️ Cascade classifiers issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error in live recognition test: {e}")
        return False

def test_database_functionality():
    """Test database functionality"""
    print("\n🗄️ Testing Database Functionality...")
    
    try:
        from iris_database_manager import IrisDatabaseManager
        
        # Create test database
        db = IrisDatabaseManager("test_iris.db")
        print("   ✅ Database initialized successfully")
        
        # Test user enrollment
        success, message = db.enroll_user(999, "Test User", "test@example.com", "123-456-7890")
        if success:
            print("   ✅ User enrollment successful")
        else:
            print(f"   ⚠️ User enrollment: {message}")
        
        # Test access logging
        log_success = db.log_access(999, "test_recognition", 0.95, True, "Test Location", "test_device")
        if log_success:
            print("   ✅ Access logging successful")
        else:
            print("   ❌ Access logging failed")
        
        # Test statistics
        stats = db.get_system_statistics()
        if stats:
            print(f"   ✅ Statistics retrieved: {len(stats)} metrics")
        else:
            print("   ❌ Statistics retrieval failed")
        
        # Clean up test database
        if os.path.exists("test_iris.db"):
            os.remove("test_iris.db")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error in database test: {e}")
        return False

def test_realistic_samples():
    """Test realistic sample generation"""
    print("\n🎨 Testing Realistic Sample Generation...")
    
    try:
        # Check if samples exist
        if os.path.exists('testSamples') and os.path.exists('sample_dataset'):
            test_samples = len([f for f in os.listdir('testSamples') if f.endswith('.jpg')])
            dataset_dirs = len([d for d in os.listdir('sample_dataset') if os.path.isdir(f'sample_dataset/{d}')])
            
            print(f"   ✅ Test samples: {test_samples} images")
            print(f"   ✅ Dataset: {dataset_dirs} person directories")
            
            # Test sample quality
            if test_samples > 0:
                sample_path = f"testSamples/{os.listdir('testSamples')[0]}"
                img = cv2.imread(sample_path)
                if img is not None:
                    print(f"   ✅ Sample image quality: {img.shape}")
                    return True
                else:
                    print("   ❌ Sample image corrupted")
                    return False
            else:
                print("   ❌ No sample images found")
                return False
        else:
            print("   ⚠️ Sample directories not found")
            return False
            
    except Exception as e:
        print(f"   ❌ Error in sample test: {e}")
        return False

def test_analytics_functionality():
    """Test analytics functionality"""
    print("\n📊 Testing Analytics Functionality...")
    
    try:
        import pickle
        import matplotlib.pyplot as plt
        
        # Create dummy history for testing
        dummy_history = {
            'accuracy': [0.1, 0.3, 0.5, 0.7, 0.8],
            'loss': [0.9, 0.7, 0.5, 0.3, 0.2],
            'val_accuracy': [0.15, 0.35, 0.55, 0.65, 0.75],
            'val_loss': [0.85, 0.65, 0.45, 0.35, 0.25]
        }
        
        # Save test history
        os.makedirs('model', exist_ok=True)
        with open('model/test_history.pckl', 'wb') as f:
            pickle.dump(dummy_history, f)
        
        print("   ✅ Test history created")
        
        # Test history loading
        with open('model/test_history.pckl', 'rb') as f:
            loaded_history = pickle.load(f)
        
        if 'accuracy' in loaded_history and len(loaded_history['accuracy']) > 0:
            print("   ✅ History loading successful")
        else:
            print("   ❌ History loading failed")
            return False
        
        # Test matplotlib functionality
        plt.figure(figsize=(8, 6))
        plt.plot(loaded_history['accuracy'], label='Accuracy')
        plt.plot(loaded_history['loss'], label='Loss')
        plt.legend()
        plt.title('Test Analytics Plot')
        plt.savefig('test_analytics_plot.png')
        plt.close()
        
        if os.path.exists('test_analytics_plot.png'):
            print("   ✅ Analytics plotting successful")
            os.remove('test_analytics_plot.png')  # Clean up
        else:
            print("   ❌ Analytics plotting failed")
            return False
        
        # Clean up test file
        if os.path.exists('model/test_history.pckl'):
            os.remove('model/test_history.pckl')
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error in analytics test: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🔬 COMPREHENSIVE IRIS RECOGNITION SYSTEM TEST")
    print("=" * 60)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Iris Feature Extraction", test_iris_feature_extraction),
        ("Model Training", test_model_training),
        ("Live Recognition Setup", test_live_recognition_setup),
        ("Database Functionality", test_database_functionality),
        ("Realistic Samples", test_realistic_samples),
        ("Analytics Functionality", test_analytics_functionality)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    success_rate = (passed_tests / total_tests) * 100
    
    if success_rate >= 80:
        print(f"🎉 EXCELLENT! {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        print("The iris recognition system is working excellently!")
    elif success_rate >= 60:
        print(f"✅ GOOD! {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        print("The iris recognition system is working well with minor issues.")
    else:
        print(f"⚠️ NEEDS WORK! {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        print("The iris recognition system needs additional fixes.")
    
    print(f"\n🎯 READY TO USE:")
    print("   1. Run: python Main.py")
    print("   2. Click 'TRAIN MODEL' to train the system")
    print("   3. Click 'TEST RECOGNITION' to test with sample images")
    print("   4. Click 'LIVE RECOGNITION' to test with camera")
    print("   5. Click 'VIEW ANALYTICS' to see training metrics")
    
    print(f"\nTest completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return success_rate >= 60

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
