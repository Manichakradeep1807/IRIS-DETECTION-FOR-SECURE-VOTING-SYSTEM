#!/usr/bin/env python3
"""
QUICK PROJECT DIAGNOSIS TEST
===========================
Simple test to check if your iris recognition project is working.
"""

import os
import sys

def check_files():
    """Check if essential files exist"""
    print("📁 CHECKING PROJECT FILES...")
    
    essential_files = [
        'Main.py',
        'voice_commands.py', 
        'requirements.txt'
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"✅ {file}: Found")
        else:
            print(f"❌ {file}: Missing")
    
    # Check directories
    dirs = ['model', 'captured_iris', 'testSamples', 'sample_dataset']
    for directory in dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/: Found")
        else:
            print(f"❌ {directory}/: Missing")

def check_imports():
    """Check if key imports work"""
    print("\n📦 CHECKING IMPORTS...")
    
    imports_to_test = [
        ('tkinter', 'Tkinter (GUI)'),
        ('numpy', 'NumPy'),
        ('cv2', 'OpenCV'),
        ('matplotlib', 'Matplotlib'),
        ('tensorflow', 'TensorFlow'),
        ('speech_recognition', 'SpeechRecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('pyaudio', 'PyAudio')
    ]
    
    working_imports = 0
    total_imports = len(imports_to_test)
    
    for module, name in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {name}: Available")
            working_imports += 1
        except ImportError:
            print(f"❌ {name}: Missing")
    
    print(f"\n📊 Import Status: {working_imports}/{total_imports} working")
    return working_imports, total_imports

def check_voice_commands():
    """Check voice commands system"""
    print("\n🎤 CHECKING VOICE COMMANDS...")
    
    try:
        from voice_commands import VoiceCommandSystem
        print("✅ Voice commands module: Imported")
        
        voice_system = VoiceCommandSystem()
        print("✅ Voice system: Created")
        
        if hasattr(voice_system, 'command_patterns'):
            patterns = voice_system.command_patterns
            print(f"✅ Command patterns: {len(patterns)} found")
            
            # Show some commands
            key_commands = ['start_recognition', 'take_photo', 'show_gallery']
            for cmd in key_commands:
                if cmd in patterns:
                    print(f"✅ '{cmd}': Available")
                else:
                    print(f"❌ '{cmd}': Missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice commands failed: {e}")
        return False

def check_model_data():
    """Check if model and data files exist"""
    print("\n🧠 CHECKING MODEL AND DATA...")
    
    model_files = [
        'model/X.txt.npy',
        'model/Y.txt.npy', 
        'model/model.json'
    ]
    
    for file in model_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"✅ {file}: Found ({size:.1f} KB)")
        else:
            print(f"❌ {file}: Missing")
    
    # Check sample data
    if os.path.exists('sample_dataset'):
        try:
            person_dirs = [d for d in os.listdir('sample_dataset') if os.path.isdir(os.path.join('sample_dataset', d))]
            print(f"✅ Sample dataset: {len(person_dirs)} person directories")
        except:
            print("⚠️ Sample dataset: Cannot read")
    else:
        print("❌ Sample dataset: Missing")

def create_fix_instructions():
    """Create detailed fix instructions"""
    print("\n🔧 DETAILED FIX INSTRUCTIONS")
    print("=" * 50)

    print("\n📋 STEP-BY-STEP FIX:")
    print("1. Run the complete fix script:")
    print("   COMPLETE_PROJECT_FIX.bat")
    print("\n2. Or install manually:")
    print("   pip install tensorflow>=2.10.0")
    print("   pip install opencv-python>=4.5.0")
    print("   pip install numpy matplotlib scikit-learn")
    print("   pip install SpeechRecognition pyttsx3 pyaudio")
    print("\n3. Test the installation:")
    print("   python quick_project_test.py")
    print("\n4. Run your project:")
    print("   python Main.py")

    print("\n🎯 EXPECTED FEATURES AFTER FIX:")
    print("✅ High-accuracy iris recognition (98%+ target)")
    print("✅ Live camera recognition with real-time detection")
    print("✅ Voice command control (25+ commands)")
    print("✅ Iris image gallery with auto-save")
    print("✅ Analytics dashboard with training graphs")
    print("✅ Modern GUI with dark theme and scroll support")
    print("✅ Database integration for storing results")
    print("✅ Performance monitoring and system diagnostics")

def main():
    """Run quick diagnosis"""
    print("🔍 QUICK PROJECT DIAGNOSIS")
    print("=" * 50)
    print("Checking if your iris recognition project is ready to run...\n")

    # Run checks
    check_files()
    working_imports, total_imports = check_imports()

    # Try voice commands (may fail due to missing deps)
    voice_ok = False
    try:
        voice_ok = check_voice_commands()
    except:
        print("❌ Voice commands: Cannot test (missing dependencies)")

    check_model_data()

    # Summary
    print("\n" + "=" * 50)
    print("📋 DIAGNOSIS SUMMARY")
    print("=" * 50)

    success_rate = working_imports / total_imports * 100

    if working_imports >= total_imports * 0.8 and voice_ok:
        print("🎉 PROJECT STATUS: READY TO RUN!")
        print("\n✅ Your iris recognition project should work properly.")
        print("\n🚀 To run your project:")
        print("   python Main.py")
        print("\n🎤 Voice commands should work:")
        print("   - Say 'start recognition'")
        print("   - Say 'take photo'")
        print("   - Say 'show gallery'")

    elif working_imports >= total_imports * 0.6:
        print("⚠️ PROJECT STATUS: NEEDS MINOR FIXES")
        print(f"\n📊 {working_imports}/{total_imports} packages available ({success_rate:.1f}%)")
        print("\n🔧 Some dependencies are missing.")
        print("RECOMMENDED FIX:")
        print("   COMPLETE_PROJECT_FIX.bat")

    else:
        print("❌ PROJECT STATUS: NEEDS MAJOR FIXES")
        print(f"\n📊 {working_imports}/{total_imports} packages available ({success_rate:.1f}%)")
        print("\n🚨 Many dependencies are missing.")
        print("CRITICAL: TensorFlow and other ML packages not found!")
        print("\nRECOMMENDED FIX:")
        print("   COMPLETE_PROJECT_FIX.bat")

    # Always show fix instructions
    create_fix_instructions()

    print(f"\n📊 Final Status: {working_imports}/{total_imports} packages ({success_rate:.1f}%)")
    print("=" * 50)

if __name__ == "__main__":
    main()
