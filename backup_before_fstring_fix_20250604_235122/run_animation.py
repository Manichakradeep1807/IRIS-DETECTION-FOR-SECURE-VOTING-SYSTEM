#!/usr/bin/env python3
"""
🎬 Run Iris Recognition Animation Video Creator
Simple script to create the animation video with error handling
"""

import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {pip_name} - OK")
        except ImportError:
            print(f"❌ {pip_name} - MISSING")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    """Main function"""
    print("🎬 Iris Recognition Animation Video Creator")
    print("=" * 60)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return False
    
    print("\n✅ All dependencies available!")
    
    # Import and run animation
    try:
        print("\n🎬 Starting animation creation...")
        from create_animation_video import main as create_animation
        
        success = create_animation()
        
        if success:
            print("\n🎉 SUCCESS! Animation video created!")
            print("📁 Check for: iris_recognition_demo.mp4")
            
            # Check if file exists
            if os.path.exists("iris_recognition_demo.mp4"):
                file_size = os.path.getsize("iris_recognition_demo.mp4") / (1024 * 1024)  # MB
                print(f"📊 File size: {file_size:.1f} MB")
            
            return True
        else:
            print("\n❌ Animation creation failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Error creating animation: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Make sure you have enough disk space")
        print("   2. Check that OpenCV is properly installed")
        print("   3. Try running: pip install opencv-python numpy")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🚀 Animation ready to share!")
        input("\nPress Enter to exit...")
    else:
        print("\n💡 Need help? Check the error messages above")
        input("\nPress Enter to exit...")
