#!/usr/bin/env python3
"""
Test script to verify that the voice command model issue is fixed
"""

def test_model_initialization():
    """Test that model variable is properly initialized"""
    print("🧪 TESTING MODEL INITIALIZATION FIX")
    print("=" * 50)
    
    try:
        # Import Main.py to check model initialization
        import sys
        import os
        
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Test model variable existence
        print("📋 Checking model variable initialization...")
        
        # This should not raise a NameError anymore
        from Main import model
        print(f"✅ Model variable exists: {model}")
        
        if model is None:
            print("✅ Model is properly initialized to None")
        else:
            print(f"✅ Model is loaded: {type(model)}")
        
        return True
        
    except NameError as e:
        print(f"❌ NameError: {e}")
        print("   Model variable is not defined")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_voice_command_functions():
    """Test that voice command functions can be called"""
    print("\n🎤 TESTING VOICE COMMAND FUNCTIONS")
    print("=" * 50)
    
    try:
        # Import voice command functions
        from Main import voice_start_recognition, take_screenshot, stop_live_recognition
        
        print("✅ Voice command functions imported successfully:")
        print("   • voice_start_recognition")
        print("   • take_screenshot") 
        print("   • stop_live_recognition")
        
        # Test if functions are callable
        if callable(voice_start_recognition):
            print("✅ voice_start_recognition is callable")
        else:
            print("❌ voice_start_recognition is not callable")
            return False
        
        if callable(take_screenshot):
            print("✅ take_screenshot is callable")
        else:
            print("❌ take_screenshot is not callable")
            return False
        
        if callable(stop_live_recognition):
            print("✅ stop_live_recognition is callable")
        else:
            print("❌ stop_live_recognition is not callable")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_voice_system_integration():
    """Test voice system integration"""
    print("\n🔗 TESTING VOICE SYSTEM INTEGRATION")
    print("=" * 50)
    
    try:
        # Test voice commands module
        from voice_commands import VoiceCommandSystem
        print("✅ Voice command system can be imported")
        
        # Test if voice system can be created
        voice_system = VoiceCommandSystem()
        print("✅ Voice command system can be instantiated")
        
        # Test callback registration
        def test_callback():
            return "test"
        
        voice_system.register_callback('test', test_callback)
        print("✅ Callback registration works")
        
        # Test command patterns
        patterns = voice_system.command_patterns
        if 'start_recognition' in patterns:
            print("✅ Start recognition patterns found")
        else:
            print("❌ Start recognition patterns missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Voice system integration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 VOICE COMMAND MODEL FIX VERIFICATION")
    print("=" * 60)
    print("This test verifies that the 'model not defined' error is fixed")
    print("and voice commands can work properly.")
    print("=" * 60)
    
    # Run tests
    test1_result = test_model_initialization()
    test2_result = test_voice_command_functions()
    test3_result = test_voice_system_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Model Initialization:     {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Voice Command Functions:  {'✅ PASS' if test2_result else '❌ FAIL'}")
    print(f"Voice System Integration: {'✅ PASS' if test3_result else '❌ FAIL'}")
    
    if all([test1_result, test2_result, test3_result]):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The 'model not defined' error has been fixed")
        print("✅ Voice commands should work properly now")
        print("\n🚀 VOICE COMMANDS ARE READY:")
        print("   1. The main application is running")
        print("   2. Click '🎤 VOICE COMMANDS' button")
        print("   3. Say 'Start recognition' to test")
        print("   4. The system will handle model loading automatically")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("There may still be issues with the voice command system")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
