#!/usr/bin/env python3
"""
VOICE COMMANDS DIAGNOSIS AND FIX
================================
This script will diagnose and fix voice command issues step by step.
"""

import os
import sys
import subprocess
import importlib.util

def print_header(title):
    print("\n" + "="*50)
    print(f"🔍 {title}")
    print("="*50)

def print_status(message, status="INFO"):
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    icon = icons.get(status, "ℹ️")
    print(f"{icon} {message}")

def check_dependency(module_name, package_name=None):
    """Check if a dependency is installed"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print_status(f"{package_name}: Available", "SUCCESS")
        return True
    except ImportError:
        print_status(f"{package_name}: Missing", "ERROR")
        return False

def install_dependency(package_name):
    """Install a dependency using pip"""
    try:
        print_status(f"Installing {package_name}...", "INFO")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print_status(f"Successfully installed {package_name}", "SUCCESS")
            return True
        else:
            print_status(f"Failed to install {package_name}", "ERROR")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print_status(f"Error installing {package_name}: {e}", "ERROR")
        return False

def test_voice_dependencies():
    """Test and install voice command dependencies"""
    print_header("CHECKING VOICE COMMAND DEPENDENCIES")
    
    dependencies = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "pyaudio"),
        ("pyttsx3", "pyttsx3")
    ]
    
    missing_deps = []
    
    for module_name, package_name in dependencies:
        if not check_dependency(module_name, package_name):
            missing_deps.append(package_name)
    
    if missing_deps:
        print_status(f"Missing dependencies: {missing_deps}", "WARNING")
        print_status("Attempting to install missing dependencies...", "INFO")
        
        for package in missing_deps:
            install_dependency(package)
        
        # Re-check after installation
        print_status("Re-checking dependencies after installation...", "INFO")
        for module_name, package_name in dependencies:
            check_dependency(module_name, package_name)
    else:
        print_status("All voice command dependencies are available!", "SUCCESS")

def test_voice_commands_import():
    """Test importing voice commands module"""
    print_header("TESTING VOICE COMMANDS MODULE")
    
    try:
        from voice_commands import VoiceCommandSystem, initialize_voice_commands
        print_status("voice_commands module imported successfully", "SUCCESS")
        return True
    except ImportError as e:
        print_status(f"voice_commands import failed: {e}", "ERROR")
        print_status("Trying alternative voice_commands_fixed.py...", "INFO")
        
        try:
            spec = importlib.util.spec_from_file_location("voice_commands_fixed", "voice_commands_fixed.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print_status("voice_commands_fixed.py imported successfully", "SUCCESS")
                return True
        except Exception as e2:
            print_status(f"voice_commands_fixed.py import failed: {e2}", "ERROR")
        
        return False

def test_voice_system_functionality():
    """Test voice system functionality"""
    print_header("TESTING VOICE SYSTEM FUNCTIONALITY")
    
    try:
        # Try to import and create voice system
        from voice_commands import VoiceCommandSystem
        
        print_status("Creating voice command system...", "INFO")
        voice_system = VoiceCommandSystem()
        
        print_status("Voice command system created successfully", "SUCCESS")
        
        # Test command patterns
        if hasattr(voice_system, 'command_patterns'):
            patterns = voice_system.command_patterns
            print_status(f"Found {len(patterns)} command patterns", "SUCCESS")
            
            # Show some example commands
            print_status("Example voice commands:", "INFO")
            for cmd, patterns_list in list(patterns.items())[:5]:
                print(f"   - {patterns_list[0]}")
        
        # Test callback registration
        def test_callback():
            print_status("Test callback executed successfully!", "SUCCESS")
            return True
        
        voice_system.register_callback('test_command', test_callback)
        
        if 'test_command' in voice_system.command_callbacks:
            print_status("Callback registration: OK", "SUCCESS")
            
            # Execute test callback
            result = voice_system.command_callbacks['test_command']()
            if result:
                print_status("Callback execution: OK", "SUCCESS")
        
        return True
        
    except Exception as e:
        print_status(f"Voice system test failed: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return False

def test_hardware_components():
    """Test hardware components (microphone and speakers)"""
    print_header("TESTING HARDWARE COMPONENTS")
    
    # Test microphone
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        print_status("Microphone object created", "SUCCESS")
        
        # Quick microphone test (non-blocking)
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print_status("Microphone access: OK", "SUCCESS")
        except Exception as mic_error:
            print_status(f"Microphone access issue: {mic_error}", "WARNING")
            print_status("Voice commands will work in fallback mode", "INFO")
    
    except Exception as e:
        print_status(f"Microphone test failed: {e}", "ERROR")
    
    # Test text-to-speech
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        print_status("TTS engine created", "SUCCESS")
        
        # Test TTS properties
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        voices = engine.getProperty('voices')
        
        print_status(f"TTS rate: {rate}, volume: {volume}", "INFO")
        print_status(f"Available voices: {len(voices) if voices else 0}", "INFO")
        
        engine.stop()
        print_status("Text-to-speech: OK", "SUCCESS")
        
    except Exception as e:
        print_status(f"TTS test failed: {e}", "ERROR")

def create_voice_test_demo():
    """Create a simple voice test demo"""
    print_header("CREATING VOICE TEST DEMO")
    
    demo_script = '''#!/usr/bin/env python3
"""
Voice Commands Test Demo
"""

def main():
    print("🎤 VOICE COMMANDS TEST DEMO")
    print("=" * 40)
    
    try:
        from voice_commands import VoiceCommandSystem
        
        # Create voice system
        voice_system = VoiceCommandSystem()
        print("✅ Voice system created successfully")
        
        # Register test callbacks
        def test_start_recognition():
            print("🎯 START RECOGNITION command executed!")
        
        def test_take_photo():
            print("📸 TAKE PHOTO command executed!")
        
        def test_show_gallery():
            print("🖼️ SHOW GALLERY command executed!")
        
        # Register callbacks
        voice_system.register_callback('start_recognition', test_start_recognition)
        voice_system.register_callback('take_photo', test_take_photo)
        voice_system.register_callback('show_gallery', test_show_gallery)
        
        print("✅ Callbacks registered successfully")
        
        # Test command execution
        print("\\n🧪 Testing command execution:")
        voice_system._execute_command('start_recognition')
        voice_system._execute_command('take_photo')
        voice_system._execute_command('show_gallery')
        
        # Show available commands
        print("\\n📋 Available voice commands:")
        patterns = voice_system.command_patterns
        for cmd, patterns_list in patterns.items():
            print(f"   {cmd}: '{patterns_list[0]}'")
        
        print("\\n🎉 Voice commands test completed successfully!")
        print("\\nTo use voice commands:")
        print("1. Say 'start recognition' to begin iris recognition")
        print("2. Say 'take photo' to capture an image")
        print("3. Say 'show gallery' to view captured images")
        print("4. Say 'help' to see all available commands")
        
    except Exception as e:
        print(f"❌ Voice commands test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
'''
    
    try:
        with open('voice_test_demo.py', 'w') as f:
            f.write(demo_script)
        print_status("Created voice_test_demo.py", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Failed to create demo: {e}", "ERROR")
        return False

def main():
    """Main diagnosis function"""
    print("🎤 VOICE COMMANDS DIAGNOSIS TOOL")
    print("=" * 50)
    print("This tool will diagnose and fix voice command issues.")
    
    # Step 1: Check dependencies
    test_voice_dependencies()
    
    # Step 2: Test voice commands import
    import_ok = test_voice_commands_import()
    
    # Step 3: Test voice system functionality
    if import_ok:
        functionality_ok = test_voice_system_functionality()
    else:
        functionality_ok = False
    
    # Step 4: Test hardware
    test_hardware_components()
    
    # Step 5: Create test demo
    create_voice_test_demo()
    
    # Summary
    print_header("DIAGNOSIS SUMMARY")
    
    if import_ok and functionality_ok:
        print_status("✅ Voice commands are working properly!", "SUCCESS")
        print_status("Run 'python voice_test_demo.py' to test", "INFO")
    else:
        print_status("⚠️ Some issues found with voice commands", "WARNING")
        print_status("Recommended fixes:", "INFO")
        print("1. Run: pip install SpeechRecognition pyttsx3 pyaudio")
        print("2. Check microphone permissions")
        print("3. Try using voice_commands_fixed.py instead")
    
    print("\n" + "="*50)
    print("Diagnosis complete!")

if __name__ == "__main__":
    main()
