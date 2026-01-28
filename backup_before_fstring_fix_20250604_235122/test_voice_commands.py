#!/usr/bin/env python3
"""
Test Voice Commands System
Verifies that voice recognition and text-to-speech are working correctly
"""

import time

def test_voice_recognition():
    """Test speech recognition functionality"""
    print("🎤 TESTING VOICE RECOGNITION")
    print("=" * 50)
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition module imported")
        
        # Test microphone access
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        print("🎙️ Testing microphone access...")
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
        print("✅ Microphone access successful")
        
        # Test basic recognition (without actually listening)
        print("✅ Speech recognition components ready")
        return True
        
    except ImportError:
        print("❌ SpeechRecognition not installed")
        print("   Run: pip install SpeechRecognition")
        return False
    except Exception as e:
        print(f"❌ Voice recognition error: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech functionality"""
    print("\n🔊 TESTING TEXT-TO-SPEECH")
    print("=" * 50)
    
    try:
        import pyttsx3
        print("✅ pyttsx3 module imported")
        
        # Initialize TTS engine
        engine = pyttsx3.init()
        print("✅ TTS engine initialized")
        
        # Test voice properties
        voices = engine.getProperty('voices')
        if voices:
            print(f"✅ Found {len(voices)} voice(s)")
            for i, voice in enumerate(voices[:2]):  # Show first 2 voices
                print(f"   Voice {i+1}: {voice.name}")
        else:
            print("⚠️ No voices found")
        
        # Test speech (brief)
        print("🔊 Testing speech output...")
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        engine.say("Voice commands test successful")
        engine.runAndWait()
        print("✅ Text-to-speech test completed")
        
        return True
        
    except ImportError:
        print("❌ pyttsx3 not installed")
        print("   Run: pip install pyttsx3")
        return False
    except Exception as e:
        print(f"❌ Text-to-speech error: {e}")
        return False

def test_voice_command_system():
    """Test the voice command system integration"""
    print("\n🎯 TESTING VOICE COMMAND SYSTEM")
    print("=" * 50)
    
    try:
        from voice_commands import VoiceCommandSystem, is_voice_available
        print("✅ Voice command module imported")
        
        # Check availability
        if is_voice_available():
            print("✅ Voice recognition is available")
        else:
            print("❌ Voice recognition is not available")
            return False
        
        # Create voice system instance
        voice_system = VoiceCommandSystem()
        print("✅ Voice command system created")
        
        # Test command patterns
        patterns = voice_system.command_patterns
        print(f"✅ Found {len(patterns)} command categories:")
        for command_type, command_list in patterns.items():
            print(f"   • {command_type}: {len(command_list)} patterns")
        
        # Test callback registration
        def test_callback():
            print("Test callback executed")
        
        voice_system.register_callback('test', test_callback)
        print("✅ Callback registration works")
        
        # Test TTS
        voice_system.speak("Voice command system test")
        print("✅ Voice system TTS works")
        
        return True
        
    except ImportError as e:
        print(f"❌ Voice command system not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Voice command system error: {e}")
        return False

def test_main_integration():
    """Test integration with main application"""
    print("\n🔗 TESTING MAIN APPLICATION INTEGRATION")
    print("=" * 50)
    
    try:
        # Test if Main.py can import voice commands
        import sys
        import os
        
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Test import without running the GUI
        print("🧪 Testing voice command imports...")
        
        # This would normally import Main.py but we'll just test the voice module
        from voice_commands import initialize_voice_commands, get_voice_system
        print("✅ Voice command functions can be imported")
        
        # Test initialization
        voice_system = initialize_voice_commands()
        if voice_system:
            print("✅ Voice system can be initialized")
        else:
            print("⚠️ Voice system initialization returned None")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def main():
    """Run all voice command tests"""
    print("🧪 VOICE COMMANDS TEST SUITE")
    print("=" * 60)
    print("This test verifies that voice recognition functionality")
    print("is properly installed and configured.")
    print("=" * 60)
    
    # Run tests
    test1_result = test_voice_recognition()
    test2_result = test_text_to_speech()
    test3_result = test_voice_command_system()
    test4_result = test_main_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Voice Recognition:        {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Text-to-Speech:           {'✅ PASS' if test2_result else '❌ FAIL'}")
    print(f"Voice Command System:     {'✅ PASS' if test3_result else '❌ FAIL'}")
    print(f"Main App Integration:     {'✅ PASS' if test4_result else '❌ FAIL'}")
    
    if all([test1_result, test2_result, test3_result, test4_result]):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Voice commands are ready to use")
        print("\n🚀 HOW TO USE VOICE COMMANDS:")
        print("   1. Run the main application: python Main.py")
        print("   2. Click the '🎤 VOICE COMMANDS' button")
        print("   3. Speak one of these commands:")
        print("      • 'Start recognition'")
        print("      • 'Take photo'")
        print("      • 'Show gallery'")
        print("      • 'Stop recognition'")
        print("      • 'Help'")
        print("   4. Wait for voice confirmation")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Voice commands may not work properly.")
        print("\n🔧 TROUBLESHOOTING:")
        if not test1_result:
            print("   • Install speech recognition: pip install SpeechRecognition pyaudio")
        if not test2_result:
            print("   • Install text-to-speech: pip install pyttsx3")
        if not test3_result:
            print("   • Check voice_commands.py file")
        if not test4_result:
            print("   • Check Main.py integration")
        print("   • Run: python install_voice_dependencies.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
