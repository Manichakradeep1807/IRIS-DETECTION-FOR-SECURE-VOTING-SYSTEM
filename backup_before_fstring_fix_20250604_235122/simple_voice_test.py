#!/usr/bin/env python3
"""
Simple Voice Commands Test
"""

import sys
import os

def test_imports():
    """Test basic imports"""
    print("Testing imports...")
    
    try:
        import speech_recognition as sr
        print("✅ speech_recognition imported")
    except ImportError as e:
        print(f"❌ speech_recognition failed: {e}")
        return False
    
    try:
        import pyaudio
        print("✅ pyaudio imported")
    except ImportError as e:
        print(f"❌ pyaudio failed: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported")
    except ImportError as e:
        print(f"❌ pyttsx3 failed: {e}")
        return False
    
    return True

def test_voice_commands_import():
    """Test voice commands module import"""
    print("\nTesting voice_commands.py import...")
    
    try:
        from voice_commands import VoiceCommandSystem, initialize_voice_commands
        print("✅ voice_commands imported successfully")
        return True
    except ImportError as e:
        print(f"❌ voice_commands import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ voice_commands error: {e}")
        return False

def test_voice_system_creation():
    """Test voice system creation"""
    print("\nTesting voice system creation...")
    
    try:
        from voice_commands import VoiceCommandSystem
        voice_system = VoiceCommandSystem()
        print("✅ VoiceCommandSystem created successfully")
        
        # Test command patterns
        if hasattr(voice_system, 'command_patterns'):
            patterns = voice_system.command_patterns
            print(f"✅ Found {len(patterns)} command patterns")
            
            # Check for key commands
            key_commands = ['start_recognition', 'take_photo', 'show_gallery']
            for cmd in key_commands:
                if cmd in patterns:
                    print(f"✅ Command '{cmd}' found")
                else:
                    print(f"❌ Command '{cmd}' missing")
        else:
            print("❌ No command patterns found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Voice system creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_callback_registration():
    """Test callback registration"""
    print("\nTesting callback registration...")
    
    try:
        from voice_commands import VoiceCommandSystem
        voice_system = VoiceCommandSystem()
        
        def test_callback():
            return "test_success"
        
        voice_system.register_callback('test_command', test_callback)
        
        if 'test_command' in voice_system.command_callbacks:
            result = voice_system.command_callbacks['test_command']()
            if result == "test_success":
                print("✅ Callback registration and execution works")
                return True
            else:
                print("❌ Callback execution failed")
                return False
        else:
            print("❌ Callback registration failed")
            return False
    except Exception as e:
        print(f"❌ Callback test failed: {e}")
        return False

def test_microphone_basic():
    """Test basic microphone access"""
    print("\nTesting microphone access...")
    
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        print("✅ Microphone object created")
        return True
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

def test_tts_basic():
    """Test basic TTS"""
    print("\nTesting text-to-speech...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("✅ TTS engine created")
        engine.stop()
        return True
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def main():
    print("🎤 SIMPLE VOICE COMMANDS TEST")
    print("=" * 40)
    
    tests = [
        ("Basic Imports", test_imports),
        ("Voice Commands Import", test_voice_commands_import),
        ("Voice System Creation", test_voice_system_creation),
        ("Callback Registration", test_callback_registration),
        ("Microphone Basic", test_microphone_basic),
        ("TTS Basic", test_tts_basic)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("TEST SUMMARY:")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
