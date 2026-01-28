import sys
import subprocess

def check_python_versions():
    """Check available Python versions and compatibility"""
    print("🔍 Checking Python Compatibility for Iris Recognition System")
    print("=" * 60)
    
    current_version = sys.version_info
    print(f"Current Python version: {current_version.major}.{current_version.minor}.{current_version.micro}")
    
    # Check if current version supports TensorFlow
    if current_version.major == 3 and 7 <= current_version.minor <= 12:
        print("✅ Current Python version supports TensorFlow/Keras")
        tensorflow_compatible = True
    else:
        print("❌ Current Python version does NOT support TensorFlow/Keras")
        print("   TensorFlow requires Python 3.7-3.12")
        tensorflow_compatible = False
    
    print("\n🔍 Checking for other Python versions...")
    
    # Check for Python 3.11 and 3.12
    compatible_versions = []
    
    for version in ['3.11', '3.12', '3.10', '3.9']:
        try:
            result = subprocess.run([f'py', f'-{version}', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ Found Python {version}: {result.stdout.strip()}")
                compatible_versions.append(version)
            else:
                print(f"❌ Python {version} not found")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"❌ Python {version} not found")
    
    print("\n📋 Recommendations:")
    print("-" * 40)
    
    if tensorflow_compatible:
        print("🎉 You can use the full deep learning functionality!")
        print("   Run: python Main.py")
    elif compatible_versions:
        best_version = compatible_versions[0]
        print(f"🔧 Use Python {best_version} for full functionality:")
        print(f"   Run: py -{best_version} Main.py")
        print(f"   Or run: setup_python311.bat")
    else:
        print("⚠️  No compatible Python version found.")
        print("   Please install Python 3.11 or 3.12 from:")
        print("   https://www.python.org/downloads/")
    
    print(f"\n📦 Current functionality with Python {current_version.major}.{current_version.minor}:")
    if tensorflow_compatible:
        print("   ✅ Full CNN deep learning model")
        print("   ✅ Real iris recognition")
        print("   ✅ Model training and saving")
        print("   ✅ Accuracy graphs")
        print("   ✅ Voting system")
    else:
        print("   ✅ GUI interface")
        print("   ✅ Iris feature extraction")
        print("   ✅ Demo/simulated recognition")
        print("   ❌ Deep learning model (requires Python 3.7-3.12)")
    
    return tensorflow_compatible, compatible_versions

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking Dependencies...")
    print("-" * 30)
    
    required_packages = [
        'numpy', 'matplotlib', 'cv2', 'tkinter', 
        'pyttsx3', 'skimage', 'pickle'
    ]
    
    optional_packages = ['tensorflow', 'keras']
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'skimage':
                import skimage
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_required.append(package)
    
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"⚠️  {package} - Missing (needed for deep learning)")
            missing_optional.append(package)
    
    if missing_required:
        print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
        print("   Install with: pip install opencv-python matplotlib numpy pyttsx3 scikit-image")
    
    if missing_optional:
        print(f"\n⚠️  Missing optional packages: {', '.join(missing_optional)}")
        print("   For full functionality, install with compatible Python version")
    
    return len(missing_required) == 0, len(missing_optional) == 0

if __name__ == "__main__":
    try:
        tensorflow_compatible, compatible_versions = check_python_versions()
        required_ok, optional_ok = check_dependencies()
        
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        
        if tensorflow_compatible and required_ok and optional_ok:
            print("🎉 READY TO GO! Full functionality available.")
            print("   Run: python Main.py")
        elif required_ok and compatible_versions:
            print("🔧 SETUP NEEDED: Use compatible Python version.")
            print("   Run: setup_python311.bat")
        elif required_ok:
            print("⚠️  LIMITED FUNCTIONALITY: GUI only.")
            print("   Install Python 3.11/3.12 for deep learning.")
        else:
            print("❌ SETUP REQUIRED: Missing dependencies.")
            print("   Install required packages first.")
        
    except Exception as e:
        print(f"Error during compatibility check: {e}")
    
    input("\nPress Enter to exit...")
