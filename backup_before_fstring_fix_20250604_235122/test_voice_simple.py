#!/usr/bin/env python3
"""
Simple Voice Commands Test
"""

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    try:
        import speech_recognition as sr
        print("✅ speech_recognition imported")
    except Exception as e:
        print(f"❌ speech_recognition failed: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported")
    except Exception as e:
        print(f"❌ pyttsx3 failed: {e}")
        return False
    
    try:
        import pyaudio
        print("✅ pyaudio imported")
    except Exception as e:
        print(f"❌ pyaudio failed: {e}")
        return False
    
    return True

def test_voice_commands_module():
    """Test voice_commands module"""
    print("\n🔍 Testing voice_commands module...")
    
    try:
        import voice_commands
        print("✅ voice_commands module imported")
        
        # Test VoiceCommandSystem creation
        voice_system = voice_commands.VoiceCommandSystem()
        print("✅ VoiceCommandSystem created")
        
        # Test command patterns
        patterns = voice_system.command_patterns
        print(f"✅ Command patterns: {len(patterns)} categories")
        
        # Test specific new commands
        new_commands = ['clear_console', 'save_data', 'check_memory', 'current_time']
        print("\n🆕 New commands:")
        for cmd in new_commands:
            if cmd in patterns:
                print(f"   ✅ {cmd}: {len(patterns[cmd])} patterns")
            else:
                print(f"   ❌ {cmd}: MISSING")
        
        # Test voice availability
        available = voice_commands.is_voice_available()
        print(f"\n✅ Voice available: {available}")
        
        return True
        
    except Exception as e:
        print(f"❌ voice_commands module failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_integration():
    """Test Main.py integration"""
    print("\n🔍 Testing Main.py integration...")
    
    try:
        # Check if Main.py has the required functions
        with open('Main.py', 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        required_functions = [
            'voice_clear_console',
            'voice_save_data', 
            'voice_check_memory',
            'voice_current_time'
        ]
        
        print("🔍 Checking callback functions:")
        for func in required_functions:
            if f"def {func}(" in main_content:
                print(f"   ✅ {func}")
            else:
                print(f"   ❌ {func} - MISSING")
        
        return True
        
    except Exception as e:
        print(f"❌ Main.py check failed: {e}")
        return False

def main():
    """Run simple voice commands test"""
    print("🎤 SIMPLE VOICE COMMANDS TEST")
    print("=" * 50)
    
    # Run tests
    test1 = test_imports()
    test2 = test_voice_commands_module() if test1 else False
    test3 = test_main_integration()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"   Imports: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"   Voice Module: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"   Main Integration: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if test1 and test2 and test3:
        print("\n🎉 ALL TESTS PASSED!")
        print("Voice commands should work now.")
        print("\n💡 To test:")
        print("   1. Run: python Main.py")
        print("   2. Click '🎤 VOICE COMMANDS' button")
        print("   3. Try saying: 'Clear console', 'What time is it?'")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Voice commands may not work properly.")

if __name__ == "__main__":
    main()
