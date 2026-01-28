"""
Comprehensive Test Suite for Iris Recognition System
Tests all major functions and identifies issues
"""

import os
import sys
import time
import traceback
import subprocess
import numpy as np
import cv2
import pickle
from datetime import datetime

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    issues = []
    
    try:
        import tkinter as tk
        print("   ✅ tkinter")
    except ImportError as e:
        issues.append("tkinter: {}".format(e))
        
    try:
        import numpy as np
        print("   ✅ numpy")
    except ImportError as e:
        issues.append("numpy: {}".format(e))
        
    try:
        import cv2
        print("   ✅ opencv-python")
    except ImportError as e:
        issues.append("opencv-python: {}".format(e))
        
    try:
        import matplotlib.pyplot as plt
        print("   ✅ matplotlib")
    except ImportError as e:
        issues.append("matplotlib: {}".format(e))
        
    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
        print("   ✅ tensorflow/keras")
    except ImportError as e:
        issues.append("tensorflow: {}".format(e))
        
    try:
        from sklearn.model_selection import train_test_split
        print("   ✅ scikit-learn")
    except ImportError as e:
        issues.append("scikit-learn: {}".format(e))
        
    try:
        import pyttsx3
        print("   ✅ pyttsx3")
    except ImportError as e:
        issues.append("pyttsx3: {}".format(e))
        
    return issues

def test_file_structure():
    """Test required files and directories"""
    print("\n📁 Testing file structure...")
    issues = []
    
    required_files = [
        'Main.py',
        'advanced_models.py',
        'analytics_dashboard.py',
        'data_augmentation.py',
        'database_manager.py',
        'live_recognition.py',
        'performance_monitor.py',
        'create_sample_dataset.py'
    ]
    
    required_dirs = [
        'model',
        'testSamples',
        'sample_dataset'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print("   ✅ {}".format(file))
        else:
            issues.append("Missing file: {}".format(file))
            print("   ❌ {}".format(file))
    
    for dir in required_dirs:
        if os.path.exists(dir):
            print("   ✅ {}/".format(dir))
        else:
            issues.append("Missing directory: {}".format(dir))
            print("   ❌ {}/".format(dir))
    
    return issues

def test_training_data():
    """Test training data availability"""
    print("\n📊 Testing training data...")
    issues = []
    
    if os.path.exists('model/X.txt.npy') and os.path.exists('model/Y.txt.npy'):
        try:
            X = np.load('model/X.txt.npy')
            Y = np.load('model/Y.txt.npy')
            print("   ✅ Training data loaded: {}, {Y.shape}".format(X.shape))
            
            if len(X) == 0:
                issues.append("Training data is empty")
            elif X.shape[1:] != (64, 64, 3):
                issues.append("Incorrect image shape: {}, expected (64, 64, 3)".format(X.shape[1:]))
            
        except Exception as e:
            issues.append("Error loading training data: {}".format(e))
    else:
        print("   ⚠️ No training data found, will create sample dataset")
        try:
            result = subprocess.run(['python', 'create_sample_dataset.py'], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print("   ✅ Sample dataset created")
            else:
                issues.append("Failed to create sample dataset: {}".format(result.stderr))
        except Exception as e:
            issues.append("Error creating sample dataset: {}".format(e))
    
    return issues

def test_model_functions():
    """Test model training and loading functions"""
    print("\n🧠 Testing model functions...")
    issues = []
    
    try:
        # Test model creation
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
        
        # Load training data
        if not os.path.exists('model/X.txt.npy'):
            issues.append("No training data for model testing")
            return issues
            
        X_train = np.load('model/X.txt.npy')
        Y_train = np.load('model/Y.txt.npy')
        
        # Create simple model
        model = Sequential([
            Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(Y_train.shape[1], activation='softmax')
        ])
        
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print("   ✅ Model creation successful")
        
        # Test model saving
        model.save_weights('model/test_model.weights.h5')
        model_json = model.to_json()
        with open('model/test_model.json', 'w') as f:
            f.write(model_json)
        print("   ✅ Model saving successful")
        
        # Test model loading
        from tensorflow.keras.models import model_from_json
        with open('model/test_model.json', 'r') as f:
            loaded_model_json = f.read()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights('model/test_model.weights.h5')
        loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print("   ✅ Model loading successful")
        
    except Exception as e:
        issues.append("Model function error: {}".format(e))
        print("   ❌ Model function error: {}".format(e))
    
    return issues

def test_analytics_functions():
    """Test analytics and visualization functions"""
    print("\n📈 Testing analytics functions...")
    issues = []
    
    try:
        # Test history file creation
        dummy_history = {
            'accuracy': [0.1, 0.2, 0.3, 0.4, 0.5],
            'loss': [0.9, 0.8, 0.7, 0.6, 0.5],
            'val_accuracy': [0.15, 0.25, 0.35, 0.45, 0.55],
            'val_loss': [0.85, 0.75, 0.65, 0.55, 0.45]
        }
        
        with open('model/test_history.pckl', 'wb') as f:
            pickle.dump(dummy_history, f)
        print("   ✅ History file creation successful")
        
        # Test history loading
        with open('model/test_history.pckl', 'rb') as f:
            loaded_history = pickle.load(f)
        
        if 'accuracy' in loaded_history and len(loaded_history['accuracy']) > 0:
            print("   ✅ History loading successful")
        else:
            issues.append("History data is incomplete")
            
        # Test matplotlib functionality
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 6))
        plt.plot(loaded_history['accuracy'], label='Accuracy')
        plt.plot(loaded_history['loss'], label='Loss')
        plt.legend()
        plt.title('Test Plot')
        plt.savefig('test_plot.png')
        plt.close()
        print("   ✅ Matplotlib plotting successful")
        
        # Clean up test file
        if os.path.exists('test_plot.png'):
            os.remove('test_plot.png')
            
    except Exception as e:
        issues.append("Analytics function error: {}".format(e))
        print("   ❌ Analytics function error: {}".format(e))
    
    return issues

def test_image_processing():
    """Test image processing functions"""
    print("\n🖼️ Testing image processing...")
    issues = []
    
    try:
        # Create test image if it doesn't exist
        if not os.path.exists('testSamples/sample_iris.jpg'):
            if not os.path.exists('testSamples'):
                os.makedirs('testSamples')
            
            # Create a simple test image
            test_img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
            cv2.imwrite('testSamples/sample_iris.jpg', test_img)
            print("   ✅ Test image created")
        
        # Test image loading
        img = cv2.imread('testSamples/sample_iris.jpg')
        if img is not None:
            print("   ✅ Image loading successful: {}".format(img.shape))
        else:
            issues.append("Failed to load test image")
            return issues
        
        # Test image resizing
        resized = cv2.resize(img, (64, 64))
        if resized.shape == (64, 64, 3):
            print("   ✅ Image resizing successful")
        else:
            issues.append("Image resizing failed: {}".format(resized.shape))
        
        # Test image normalization
        normalized = resized.astype('float32') / 255.0
        if 0 <= normalized.min() and normalized.max() <= 1:
            print("   ✅ Image normalization successful")
        else:
            issues.append("Image normalization failed: range [{}, {normalized.max()}]".format(normalized.min()))
            
    except Exception as e:
        issues.append("Image processing error: {}".format(e))
        print("   ❌ Image processing error: {}".format(e))
    
    return issues

def test_enhanced_features():
    """Test enhanced features availability"""
    print("\n⚡ Testing enhanced features...")
    issues = []
    
    try:
        from advanced_models import create_advanced_iris_model
        print("   ✅ Advanced models available")
    except ImportError:
        issues.append("Advanced models not available")
        print("   ⚠️ Advanced models not available")
    
    try:
        from analytics_dashboard import AnalyticsDashboard
        print("   ✅ Analytics dashboard available")
    except ImportError:
        issues.append("Analytics dashboard not available")
        print("   ⚠️ Analytics dashboard not available")
    
    try:
        from live_recognition import LiveRecognition
        print("   ✅ Live recognition available")
    except ImportError:
        issues.append("Live recognition not available")
        print("   ⚠️ Live recognition not available")
    
    try:
        from performance_monitor import monitor
        print("   ✅ Performance monitor available")
    except ImportError:
        issues.append("Performance monitor not available")
        print("   ⚠️ Performance monitor not available")
    
    return issues

def test_main_gui_functions():
    """Test main GUI functions without actually opening GUI"""
    print("\n🖥️ Testing main GUI functions...")
    issues = []

    try:
        # Import main functions
        sys.path.append('.')

        # Test individual functions from Main.py
        import Main

        # Test if functions exist
        if hasattr(Main, 'loadModel'):
            print("   ✅ loadModel function exists")
        else:
            issues.append("loadModel function missing")

        if hasattr(Main, 'show_analytics_dashboard'):
            print("   ✅ show_analytics_dashboard function exists")
        else:
            issues.append("show_analytics_dashboard function missing")

        if hasattr(Main, 'predictChange'):
            print("   ✅ predictChange function exists")
        else:
            issues.append("predictChange function missing")

        if hasattr(Main, 'graph'):
            print("   ✅ graph function exists")
        else:
            issues.append("graph function missing")

    except Exception as e:
        issues.append("Main GUI function error: {}".format(e))
        print("   ❌ Main GUI function error: {}".format(e))

    return issues

def test_database_functionality():
    """Test database functionality"""
    print("\n🗄️ Testing database functionality...")
    issues = []

    try:
        from database_manager import db

        # Test database connection
        stats = db.get_system_statistics()
        print("   ✅ Database connection successful")

        # Test basic database operations
        if isinstance(stats, dict):
            print("   ✅ Database statistics retrieval successful")
        else:
            issues.append("Database statistics format incorrect")

    except Exception as e:
        issues.append("Database error: {}".format(e))
        print("   ❌ Database error: {}".format(e))

    return issues

def run_specific_function_tests():
    """Run specific tests for problematic functions"""
    print("\n🔧 Testing specific problematic functions...")
    issues = []

    # Test analytics dashboard specifically
    try:
        if os.path.exists('model/history.pckl'):
            with open('model/history.pckl', 'rb') as f:
                data = pickle.load(f)

            if 'accuracy' in data and len(data['accuracy']) > 0:
                print("   ✅ Training history data is valid")
            else:
                issues.append("Training history data is invalid or empty")
        else:
            print("   ⚠️ No training history found")

    except Exception as e:
        issues.append("Analytics test error: {}".format(e))

    # Test model loading specifically
    try:
        if os.path.exists('model/model.json'):
            with open('model/model.json', 'r') as f:
                model_json = f.read()

            from tensorflow.keras.models import model_from_json
            model = model_from_json(model_json)

            # Check for weights file
            if os.path.exists('model/model.weights.h5'):
                model.load_weights('model/model.weights.h5')
                print("   ✅ Model loading from saved files successful")
            else:
                issues.append("Model weights file not found")

        else:
            print("   ⚠️ No saved model found")

    except Exception as e:
        issues.append("Model loading test error: {}".format(e))

    return issues

def main():
    """Run comprehensive test suite"""
    print("🔬 COMPREHENSIVE IRIS RECOGNITION SYSTEM TEST")
    print("=" * 60)
    print("Test started: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print()

    all_issues = []

    # Run all tests
    all_issues.extend(test_imports())
    all_issues.extend(test_file_structure())
    all_issues.extend(test_training_data())
    all_issues.extend(test_model_functions())
    all_issues.extend(test_analytics_functions())
    all_issues.extend(test_image_processing())
    all_issues.extend(test_enhanced_features())
    all_issues.extend(test_main_gui_functions())
    all_issues.extend(test_database_functionality())
    all_issues.extend(run_specific_function_tests())

    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)

    if not all_issues:
        print("🎉 ALL TESTS PASSED!")
        print("The iris recognition system is working correctly.")
    else:
        print("⚠️ FOUND {} ISSUES:".format(len(all_issues)))
        for i, issue in enumerate(all_issues, 1):
            print("   {}. {issue}".format(i))

        print("\n🔧 RECOMMENDED ACTIONS:")
        if any("import" in issue.lower() for issue in all_issues):
            print("   • Install missing packages: pip install -r requirements.txt")
        if any("file" in issue.lower() or "directory" in issue.lower() for issue in all_issues):
            print("   • Check file structure and create missing files")
        if any("model" in issue.lower() for issue in all_issues):
            print("   • Run model training: python Main.py -> Train Model")
        if any("data" in issue.lower() for issue in all_issues):
            print("   • Create sample dataset: python create_sample_dataset.py")

    print("\nTest completed: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    return len(all_issues) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
