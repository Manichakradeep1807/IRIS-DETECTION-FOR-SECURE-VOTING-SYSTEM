"""
Easy Startup Script for Iris Recognition System
This script checks dependencies and starts the system
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print("✅ Python version: {}.{version.minor}.{version.micro}".format(version.major))
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'tensorflow',
        'cv2',
        'numpy',
        'matplotlib',
        'sklearn',
        'PIL',
        'tkinter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                importlib.import_module('cv2')
            elif package == 'sklearn':
                importlib.import_module('sklearn')
            elif package == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package)
            print("✅ {}".format(package))
        except ImportError:
            print("❌ {}".format(package))
            missing_packages.append(package)
    
    return missing_packages

def install_missing_packages(missing_packages):
    """Install missing packages"""
    if not missing_packages:
        return True
    
    print("\n📦 Installing missing packages: {}".format(', '.join(missing_packages)))
    
    # Map package names to pip install names
    pip_names = {
        'cv2': 'opencv-python',
        'sklearn': 'scikit-learn',
        'PIL': 'Pillow'
    }
    
    for package in missing_packages:
        pip_name = pip_names.get(package, package)
        try:
            print("Installing {}...".format(pip_name))
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_name])
            print("✅ {} installed successfully".format(pip_name))
        except subprocess.CalledProcessError:
            print("❌ Failed to install {}".format(pip_name))
            return False
    
    return True

def check_project_files():
    """Check if required project files exist"""
    required_files = [
        'Main.py',
        'live_recognition.py',
        'create_realistic_iris_samples.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print("✅ {}".format(file))
        else:
            print("❌ {}".format(file))
            missing_files.append(file)
    
    return missing_files

def create_directories():
    """Create required directories"""
    directories = ['model', 'testSamples', 'sample_dataset']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("📁 Created directory: {}".format(directory))
        else:
            print("✅ Directory exists: {}".format(directory))

def start_application():
    """Start the iris recognition application"""
    try:
        print("\n🚀 Starting Iris Recognition System...")
        print("=" * 50)
        
        # Import and run the main application
        import Main
        
    except Exception as e:
        print("❌ Error starting application: {}".format(e))
        print("\n🔧 Troubleshooting:")
        print("1. Check if all dependencies are installed")
        print("2. Run: python test_iris_system.py")
        print("3. Check console for detailed error messages")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🔬 IRIS RECOGNITION SYSTEM STARTUP")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    print("\n📦 Checking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        response = input(f"\n❓ Install missing packages? (y/n): ").lower()
        if response == 'y':
            if not install_missing_packages(missing_packages):
                print("❌ Failed to install some packages. Please install manually.")
                input("Press Enter to exit...")
                return
        else:
            print("❌ Cannot start without required packages.")
            input("Press Enter to exit...")
            return
    
    print("\n📁 Checking project files...")
    missing_files = check_project_files()
    
    if missing_files:
        print("❌ Missing required files: {}".format(', '.join(missing_files)))
        print("Please ensure all project files are in the current directory.")
        input("Press Enter to exit...")
        return
    
    print("\n📂 Setting up directories...")
    create_directories()
    
    print("\n✅ All checks passed!")
    print("\n🎯 QUICK START GUIDE:")
    print("1. The GUI will open automatically")
    print("2. Click '🧠 TRAIN MODEL' to train the system")
    print("3. Click '🔍 TEST RECOGNITION' to test with sample images")
    print("4. Click '📹 LIVE RECOGNITION' for camera-based recognition")

    
    input("\nPress Enter to start the application...")
    
    # Start the application
    if start_application():
        print("✅ Application started successfully!")
    else:
        print("❌ Failed to start application.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
