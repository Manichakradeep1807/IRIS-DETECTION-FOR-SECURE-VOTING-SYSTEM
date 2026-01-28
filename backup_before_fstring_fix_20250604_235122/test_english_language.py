#!/usr/bin/env python3
"""
Test script to verify that the iris recognition system is completely in English
"""

def test_english_language():
    """Test that all language settings are in English"""
    print("🌐 TESTING ENGLISH LANGUAGE CONFIGURATION")
    print("=" * 60)
    
    try:
        # Test language manager
        from language_manager import language_manager, get_text
        
        print("✅ Language manager imported successfully")
        print(f"📋 Current language: {language_manager.current_language}")
        
        if language_manager.current_language == "en":
            print("✅ Language is set to English (en)")
        else:
            print(f"❌ Language is set to {language_manager.current_language}, not English")
            return False
        
        # Test key UI elements
        print("\n📝 Testing key UI elements:")
        ui_elements = {
            "app_title": "Application Title",
            "upload_dataset": "Upload Dataset Button",
            "train_model": "Train Model Button", 
            "live_recognition": "Live Recognition Button",
            "iris_gallery": "Iris Gallery Button",
            "settings": "Settings Button",
            "welcome_title": "Welcome Message",
            "loading": "Loading Message",
            "success": "Success Message",
            "error": "Error Message"
        }
        
        all_english = True
        for key, description in ui_elements.items():
            text = get_text(key)
            print(f"   • {description:20} → {text}")
            
            # Check if text contains non-English indicators
            if any(word in text.lower() for word in ['español', 'français', 'sistema', 'reconocimiento', 'système', 'reconnaissance']):
                print(f"     ❌ Contains non-English text!")
                all_english = False
            else:
                print(f"     ✅ English text")
        
        if all_english:
            print("\n🎉 ALL UI ELEMENTS ARE IN ENGLISH!")
        else:
            print("\n❌ Some UI elements contain non-English text")
            return False
        
        # Test user preferences
        print("\n📁 Testing user preferences file:")
        import json
        import os
        
        if os.path.exists("user_preferences.json"):
            with open("user_preferences.json", "r") as f:
                prefs = json.load(f)
                lang_setting = prefs.get("language", "unknown")
                print(f"   Language setting in file: {lang_setting}")
                
                if lang_setting == "en":
                    print("   ✅ User preferences set to English")
                else:
                    print(f"   ❌ User preferences set to {lang_setting}")
                    return False
        else:
            print("   ⚠️  User preferences file not found")
        
        print("\n✅ LANGUAGE TEST COMPLETED SUCCESSFULLY")
        print("🌐 The iris recognition system is completely configured for English")
        return True
        
    except Exception as e:
        print(f"❌ Error during language test: {e}")
        return False

def test_main_application_title():
    """Test that the main application will start with English title"""
    print("\n🖥️  TESTING MAIN APPLICATION TITLE")
    print("=" * 60)
    
    try:
        # Simulate what happens when Main.py starts
        from language_manager import language_manager, get_text
        
        # This is what Main.py does to set the title
        title = get_text("app_title", "👁️ Iris Recognition System - Advanced Biometric Platform")
        print(f"Application title will be: {title}")
        
        if "Iris Recognition System" in title and "Advanced Biometric Platform" in title:
            print("✅ Main application title is in English")
            return True
        else:
            print("❌ Main application title is not in English")
            return False
            
    except Exception as e:
        print(f"❌ Error testing main application title: {e}")
        return False

def main():
    """Run all language tests"""
    print("🔍 ENGLISH LANGUAGE VERIFICATION TEST")
    print("=" * 60)
    print("This test verifies that the iris recognition system")
    print("is completely configured to use English language.")
    print("=" * 60)
    
    # Run tests
    test1_result = test_english_language()
    test2_result = test_main_application_title()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Language Configuration: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Main Application Title: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The iris recognition system is completely in English")
        print("🚀 You can now run the main application with: python Main.py")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("The system may not be completely in English")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
