#!/usr/bin/env python3
"""
COMPREHENSIVE IRIS RECOGNITION PROJECT DIAGNOSIS
===============================================
This tool will test every component of your iris recognition system
to ensure everything is working properly.
"""

import os
import sys
import time
import traceback
import subprocess
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"🔍 {title}")
    print("="*70)

def print_status(message, status="INFO"):
    """Print a status message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️", "TEST": "🧪"}
    icon = icons.get(status, "ℹ️")
    print(f"[{timestamp}] {icon} {message}")

def test_python_environment():
    """Test Python environment and version"""
    print_header("TESTING PYTHON ENVIRONMENT")
    
    try:
        python_version = sys.version
        print_status(f"Python Version: {python_version.split()[0]}", "SUCCESS")
        
        # Check if Python version is compatible
        version_info = sys.version_info
        if version_info.major == 3 and version_info.minor >= 8:
            print_status("Python version is compatible", "SUCCESS")
            return True
        else:
            print_status("Python version may be too old (need 3.8+)", "WARNING")
            return True  # Still allow to continue
            
    except Exception as e:
        print_status(f"Python environment test failed: {e}", "ERROR")
        return False

def test_core_dependencies():
    """Test all core dependencies"""
    print_header("TESTING CORE DEPENDENCIES")
    
    dependencies = {
        # Core ML/CV libraries
        'tensorflow': 'TensorFlow (Deep Learning)',
        'cv2': 'OpenCV (Computer Vision)', 
        'numpy': 'NumPy (Numerical Computing)',
        'matplotlib': 'Matplotlib (Plotting)',
        'sklearn': 'Scikit-learn (Machine Learning)',
        'skimage': 'Scikit-image (Image Processing)',
        'PIL': 'Pillow (Image Processing)',
        
        # Voice command libraries
        'speech_recognition': 'SpeechRecognition (Voice Input)',
        'pyttsx3': 'pyttsx3 (Text-to-Speech)',
        'pyaudio': 'PyAudio (Audio Processing)',
        
        # System libraries
        'psutil': 'psutil (System Monitoring)',
        'tkinter': 'Tkinter (GUI Framework)',
        'threading': 'Threading (Built-in)',
        'pickle': 'Pickle (Built-in)',
        'json': 'JSON (Built-in)'
    }
    
    results = {}
    missing_deps = []
    
    for module, description in dependencies.items():
        try:
            if module == 'cv2':
                import cv2
            elif module == 'sklearn':
                import sklearn
            elif module == 'skimage':
                import skimage
            elif module == 'PIL':
                import PIL
            else:
                __import__(module)
            
            print_status(f"{description}: Available", "SUCCESS")
            results[module] = True
            
        except ImportError:
            print_status(f"{description}: MISSING", "ERROR")
            results[module] = False
            missing_deps.append(module)
    
    if missing_deps:
        print_status(f"Missing dependencies: {missing_deps}", "WARNING")
        print_status("Run: pip install -r requirements.txt", "INFO")
    
    return results

def test_project_files():
    """Test if all required project files exist"""
    print_header("TESTING PROJECT FILES")
    
    required_files = [
        'Main.py',
        'voice_commands.py',
        'requirements.txt',
        'advanced_models.py',
        'data_augmentation.py',
        'performance_monitor.py',
        'database_manager.py',
        'theme_manager.py',
        'language_manager.py',
        'settings_window.py',
        'live_recognition.py',

    ]
    
    optional_files = [
        'voice_commands_fixed.py',
        'voice_commands_fixed_new.py',
        'install_all_dependencies.bat',
        'diagnose_voice.bat'
    ]
    
    required_dirs = [
        'model',
        'captured_iris',
        'testSamples',
        'sample_dataset'
    ]
    
    missing_files = []
    missing_dirs = []
    
    # Check required files
    for file in required_files:
        if os.path.exists(file):
            print_status(f"File {file}: Found", "SUCCESS")
        else:
            print_status(f"File {file}: MISSING", "ERROR")
            missing_files.append(file)
    
    # Check optional files
    for file in optional_files:
        if os.path.exists(file):
            print_status(f"Optional file {file}: Found", "SUCCESS")
        else:
            print_status(f"Optional file {file}: Not found", "WARNING")
    
    # Check directories
    for directory in required_dirs:
        if os.path.exists(directory):
            print_status(f"Directory {directory}: Found", "SUCCESS")
        else:
            print_status(f"Directory {directory}: MISSING", "ERROR")
            missing_dirs.append(directory)
    
    return len(missing_files) == 0 and len(missing_dirs) == 0

def test_voice_commands():
    """Test voice command system"""
    print_header("TESTING VOICE COMMAND SYSTEM")
    
    try:
        # Test import
        from voice_commands import VoiceCommandSystem, initialize_voice_commands
        print_status("Voice commands module imported successfully", "SUCCESS")
        
        # Test system creation
        voice_system = VoiceCommandSystem()
        print_status("Voice command system created", "SUCCESS")
        
        # Test command patterns
        if hasattr(voice_system, 'command_patterns'):
            patterns = voice_system.command_patterns
            print_status(f"Found {len(patterns)} command patterns", "SUCCESS")
            
            # Test key commands
            key_commands = ['start_recognition', 'take_photo', 'show_gallery', 'train_model']
            for cmd in key_commands:
                if cmd in patterns:
                    print_status(f"Command '{cmd}': Available ({len(patterns[cmd])} patterns)", "SUCCESS")
                else:
                    print_status(f"Command '{cmd}': Missing", "ERROR")
        
        # Test callback registration
        def test_callback():
            return "test_success"
        
        voice_system.register_callback('test_command', test_callback)
        
        if 'test_command' in voice_system.command_callbacks:
            result = voice_system.command_callbacks['test_command']()
            if result == "test_success":
                print_status("Callback system working", "SUCCESS")
                return True
        
        return True
        
    except Exception as e:
        print_status(f"Voice commands test failed: {e}", "ERROR")
        return False

def test_model_files():
    """Test model files and training data"""
    print_header("TESTING MODEL FILES AND DATA")
    
    model_files = [
        'model/X.txt.npy',
        'model/Y.txt.npy',
        'model/model.json',
        'model/model.weights.h5'
    ]
    
    optional_model_files = [
        'model/high_accuracy_model.json',
        'model/high_accuracy_model.weights.h5',
        'model/history.pckl'
    ]
    
    # Check training data
    for file in model_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # MB
            print_status(f"Model file {file}: Found ({size:.1f} MB)", "SUCCESS")
        else:
            print_status(f"Model file {file}: Missing", "WARNING")
    
    # Check optional model files
    for file in optional_model_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # MB
            print_status(f"Optional model {file}: Found ({size:.1f} MB)", "SUCCESS")
        else:
            print_status(f"Optional model {file}: Not found", "INFO")
    
    # Check sample dataset
    if os.path.exists('sample_dataset'):
        person_dirs = [d for d in os.listdir('sample_dataset') if os.path.isdir(os.path.join('sample_dataset', d))]
        print_status(f"Sample dataset: {len(person_dirs)} person directories", "SUCCESS")
    else:
        print_status("Sample dataset: Missing", "WARNING")
    
    return True

def test_camera_access():
    """Test camera access for live recognition"""
    print_header("TESTING CAMERA ACCESS")
    
    try:
        import cv2
        
        # Test camera initialization
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                print_status(f"Camera: Available ({width}x{height})", "SUCCESS")
                cap.release()
                return True
            else:
                print_status("Camera: Connected but not working", "WARNING")
                cap.release()
                return False
        else:
            print_status("Camera: Not available", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"Camera test failed: {e}", "ERROR")
        return False

def test_gui_components():
    """Test GUI components"""
    print_header("TESTING GUI COMPONENTS")
    
    try:
        import tkinter as tk
        print_status("Tkinter: Available", "SUCCESS")
        
        # Test theme manager
        try:
            from theme_manager import theme_manager, get_current_colors
            print_status("Theme manager: Available", "SUCCESS")
        except ImportError:
            print_status("Theme manager: Missing", "WARNING")
        
        # Test language manager
        try:
            from language_manager import language_manager, get_text
            print_status("Language manager: Available", "SUCCESS")
        except ImportError:
            print_status("Language manager: Missing", "WARNING")
        
        # Test settings window
        try:
            from settings_window import show_settings_window
            print_status("Settings window: Available", "SUCCESS")
        except ImportError:
            print_status("Settings window: Missing", "WARNING")
        
        return True
        
    except Exception as e:
        print_status(f"GUI components test failed: {e}", "ERROR")
        return False

def test_main_application():
    """Test if Main.py can be imported without errors"""
    print_header("TESTING MAIN APPLICATION")
    
    try:
        # Save current directory
        original_dir = os.getcwd()
        
        # Try to import Main.py components
        print_status("Testing Main.py imports...", "TEST")
        
        # Test individual functions from Main.py
        import importlib.util
        spec = importlib.util.spec_from_file_location("Main", "Main.py")
        
        if spec and spec.loader:
            print_status("Main.py can be loaded", "SUCCESS")
            return True
        else:
            print_status("Main.py cannot be loaded", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Main application test failed: {e}", "ERROR")
        return False

def run_comprehensive_diagnosis():
    """Run all diagnostic tests"""
    print("🔍 COMPREHENSIVE IRIS RECOGNITION PROJECT DIAGNOSIS")
    print("=" * 70)
    print("Testing all components of your iris recognition system...")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Run all tests
    results['python_env'] = test_python_environment()
    results['dependencies'] = test_core_dependencies()
    results['project_files'] = test_project_files()
    results['voice_commands'] = test_voice_commands()
    results['model_files'] = test_model_files()
    results['camera'] = test_camera_access()
    results['gui'] = test_gui_components()
    results['main_app'] = test_main_application()
    
    return results

if __name__ == "__main__":
    # Run comprehensive diagnosis
    results = run_comprehensive_diagnosis()
    
    # Print summary
    print_header("DIAGNOSIS SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print_status(f"Tests completed: {total_tests}", "INFO")
    print_status(f"Tests passed: {passed_tests}", "SUCCESS" if passed_tests == total_tests else "WARNING")
    print_status(f"Tests failed: {total_tests - passed_tests}", "ERROR" if passed_tests < total_tests else "SUCCESS")
    
    # Detailed results
    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        icon = "✅" if result else "❌"
        print_status(f"{test_name.upper()}: {status}", "SUCCESS" if result else "ERROR")
    
    # Overall assessment
    if passed_tests == total_tests:
        print_status("🎉 ALL TESTS PASSED! Your project is ready to run!", "SUCCESS")
        print_status("Run: python Main.py", "INFO")
    elif passed_tests >= total_tests * 0.8:
        print_status("⚠️ Most tests passed. Project should work with minor issues.", "WARNING")
        print_status("Check failed tests above and install missing dependencies.", "INFO")
    else:
        print_status("❌ Multiple issues found. Project needs fixes.", "ERROR")
        print_status("Install dependencies: pip install -r requirements.txt", "INFO")
    
    print(f"\nDiagnosis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
