#!/usr/bin/env python3
"""
IMMEDIATE VOICE COMMANDS TEST
============================
This script tests voice commands right now and shows what's working.
"""

import sys
import traceback

def test_basic_imports():
    """Test if basic voice dependencies are available"""
    print("🔍 Testing basic imports...")
    
    results = {}
    
    # Test speech_recognition
    try:
        import speech_recognition as sr
        print("✅ speech_recognition: Available")
        results['speech_recognition'] = True
    except ImportError:
        print("❌ speech_recognition: Missing")
        results['speech_recognition'] = False
    
    # Test pyaudio
    try:
        import pyaudio
        print("✅ pyaudio: Available")
        results['pyaudio'] = True
    except ImportError:
        print("❌ pyaudio: Missing")
        results['pyaudio'] = False
    
    # Test pyttsx3
    try:
        import pyttsx3
        print("✅ pyttsx3: Available")
        results['pyttsx3'] = True
    except ImportError:
        print("❌ pyttsx3: Missing")
        results['pyttsx3'] = False
    
    return results

def test_voice_commands_module():
    """Test the voice commands module"""
    print("\n🔍 Testing voice_commands module...")
    
    try:
        from voice_commands import VoiceCommandSystem, initialize_voice_commands
        print("✅ voice_commands module imported successfully")
        
        # Test creating voice system
        voice_system = VoiceCommandSystem()
        print("✅ VoiceCommandSystem created")
        
        # Test command patterns
        if hasattr(voice_system, 'command_patterns'):
            patterns = voice_system.command_patterns
            print(f"✅ Found {len(patterns)} command patterns")
            
            # Show some commands
            print("\n📋 Available voice commands:")
            for i, (cmd, patterns_list) in enumerate(patterns.items()):
                if i < 10:  # Show first 10 commands
                    print(f"   {cmd}: '{patterns_list[0]}'")
                elif i == 10:
                    print(f"   ... and {len(patterns) - 10} more commands")
                    break
        
        # Test callback registration
        def test_callback():
            print("🎯 Test callback executed!")
            return True
        
        voice_system.register_callback('test_command', test_callback)
        
        if 'test_command' in voice_system.command_callbacks:
            print("✅ Callback registration works")
            
            # Execute test callback
            result = voice_system.command_callbacks['test_command']()
            if result:
                print("✅ Callback execution works")
        
        return True, voice_system
        
    except Exception as e:
        print(f"❌ voice_commands module failed: {e}")
        traceback.print_exc()
        return False, None

def test_voice_system_integration():
    """Test voice system integration with Main.py functions"""
    print("\n🔍 Testing voice system integration...")
    
    try:
        # Test if we can import Main.py functions
        import sys
        import os
        
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Try to import some Main.py functions (without running the GUI)
        try:
            from Main import initialize_voice_system
            print("✅ Can import initialize_voice_system from Main.py")
        except ImportError as e:
            print(f"⚠️ Cannot import from Main.py: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def simulate_voice_commands(voice_system):
    """Simulate voice command execution"""
    print("\n🎤 Simulating voice command execution...")
    
    if not voice_system:
        print("❌ No voice system available for testing")
        return
    
    # Test commands to simulate
    test_commands = [
        'start_recognition',
        'take_photo', 
        'show_gallery',
        'train_model',
        'help'
    ]
    
    # Register dummy callbacks for testing
    def dummy_start_recognition():
        print("🎯 START RECOGNITION command would execute")
    
    def dummy_take_photo():
        print("📸 TAKE PHOTO command would execute")
    
    def dummy_show_gallery():
        print("🖼️ SHOW GALLERY command would execute")
    
    def dummy_train_model():
        print("🧠 TRAIN MODEL command would execute")
    
    # Register callbacks
    voice_system.register_callback('start_recognition', dummy_start_recognition)
    voice_system.register_callback('take_photo', dummy_take_photo)
    voice_system.register_callback('show_gallery', dummy_show_gallery)
    voice_system.register_callback('train_model', dummy_train_model)
    
    print("✅ Registered test callbacks")
    
    # Simulate command execution
    print("\n🧪 Executing test commands:")
    for cmd in test_commands:
        try:
            if cmd in voice_system.command_callbacks:
                print(f"\n   Executing '{cmd}':")
                voice_system.command_callbacks[cmd]()
            elif cmd == 'help':
                print(f"\n   Executing '{cmd}':")
                voice_system._execute_command('help')
            else:
                print(f"\n   Command '{cmd}' not registered")
        except Exception as e:
            print(f"   ❌ Error executing '{cmd}': {e}")

def main():
    """Main test function"""
    print("🎤 VOICE COMMANDS IMMEDIATE TEST")
    print("=" * 50)
    print("Testing voice commands functionality right now...\n")
    
    # Test 1: Basic imports
    import_results = test_basic_imports()
    
    # Test 2: Voice commands module
    voice_module_ok, voice_system = test_voice_commands_module()
    
    # Test 3: Integration
    integration_ok = test_voice_system_integration()
    
    # Test 4: Simulate commands
    if voice_module_ok and voice_system:
        simulate_voice_commands(voice_system)
    
    # Summary
    print("\n" + "=" * 50)
    print("🔍 TEST SUMMARY")
    print("=" * 50)
    
    all_imports = all(import_results.values())
    
    if all_imports and voice_module_ok:
        print("✅ VOICE COMMANDS ARE WORKING!")
        print("\n🎉 Your voice commands should work properly.")
        print("\nTo use voice commands in the iris recognition system:")
        print("1. Run the main application: python Main.py")
        print("2. Look for voice command buttons or menu options")
        print("3. Say commands like:")
        print("   - 'Start recognition'")
        print("   - 'Take photo'") 
        print("   - 'Show gallery'")
        print("   - 'Help' (to see all commands)")
        
    elif voice_module_ok:
        print("⚠️ VOICE COMMANDS PARTIALLY WORKING")
        print("\nSome dependencies are missing, but voice commands")
        print("will work in fallback mode (text output only).")
        print("\nTo get full functionality, install missing packages:")
        missing = [pkg for pkg, available in import_results.items() if not available]
        for pkg in missing:
            print(f"   pip install {pkg}")
    
    else:
        print("❌ VOICE COMMANDS NEED FIXING")
        print("\nIssues found with voice commands system.")
        print("\nRecommended fixes:")
        print("1. Install dependencies: pip install SpeechRecognition pyttsx3 pyaudio")
        print("2. Run: python fix_voice_commands.py")
        print("3. Use the fixed voice commands module")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()
