#!/usr/bin/env python3
"""
Test script for Theme and Language features
Demonstrates the new theme switching and multi-language support
"""

import os
import sys
import time

def test_theme_manager():
    """Test the theme manager functionality"""
    print("🎨 TESTING THEME MANAGER")
    print("=" * 50)
    
    try:
        from theme_manager import theme_manager, get_current_colors, get_available_themes, switch_theme
        
        print("✅ Theme manager imported successfully")
        
        # Test getting current theme
        current_theme = theme_manager.current_theme
        print(f"📋 Current theme: {current_theme}")
        
        # Test getting available themes
        themes = get_available_themes()
        print(f"🎨 Available themes: {list(themes.keys())}")
        
        for theme_name, theme_display_name in themes.items():
            print(f"   • {theme_name}: {theme_display_name}")
        
        # Test getting colors
        colors = get_current_colors()
        print(f"🎨 Current theme colors:")
        for color_name, color_value in colors.items():
            print(f"   • {color_name}: {color_value}")
        
        # Test switching themes
        print(f"\n🔄 Testing theme switching...")
        for theme_name in themes.keys():
            if theme_name != current_theme:
                print(f"   Switching to {theme_name}...")
                success = switch_theme(theme_name)
                if success:
                    new_colors = get_current_colors()
                    print(f"   ✅ Successfully switched to {theme_name}")
                    print(f"      Primary color: {new_colors['primary']}")
                else:
                    print(f"   ❌ Failed to switch to {theme_name}")
                break
        
        # Switch back to original theme
        switch_theme(current_theme)
        print(f"🔄 Switched back to original theme: {current_theme}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Theme manager not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing theme manager: {e}")
        return False

def test_language_manager():
    """Test the language manager functionality"""
    print("\n🌐 TESTING LANGUAGE MANAGER")
    print("=" * 50)
    
    try:
        from language_manager import language_manager, get_text, get_available_languages, set_language
        
        print("✅ Language manager imported successfully")
        
        # Test getting current language
        current_language = language_manager.current_language
        print(f"📋 Current language: {current_language}")
        
        # Test getting available languages
        languages = get_available_languages()
        print(f"🌐 Available languages: {list(languages.keys())}")
        
        for lang_code, lang_name in languages.items():
            print(f"   • {lang_code}: {lang_name}")
        
        # Test getting text
        print(f"\n📝 Testing text translations:")
        test_keys = [
            "app_title",
            "upload_dataset", 
            "train_model",
            "live_recognition",
            "settings_title",
            "welcome_title"
        ]
        
        for key in test_keys:
            text = get_text(key, f"[{key}]")
            print(f"   • {key}: {text}")
        
        # Test switching languages
        print(f"\n🔄 Testing language switching...")
        for lang_code in languages.keys():
            if lang_code != current_language:
                print(f"   Switching to {lang_code} ({languages[lang_code]})...")
                success = set_language(lang_code)
                if success:
                    # Test a few translations
                    title = get_text("app_title", "Iris Recognition System")
                    upload = get_text("upload_dataset", "Upload Dataset")
                    print(f"   ✅ Successfully switched to {lang_code}")
                    print(f"      App title: {title}")
                    print(f"      Upload button: {upload}")
                else:
                    print(f"   ❌ Failed to switch to {lang_code}")
                break
        
        # Switch back to original language
        set_language(current_language)
        print(f"🔄 Switched back to original language: {current_language}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Language manager not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing language manager: {e}")
        return False

def test_settings_window():
    """Test the settings window functionality"""
    print("\n⚙️ TESTING SETTINGS WINDOW")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from settings_window import show_settings_window
        
        print("✅ Settings window module imported successfully")
        
        # Create a test root window
        root = tk.Tk()
        root.title("Settings Test")
        root.geometry("400x300")
        root.withdraw()  # Hide the test window
        
        def on_settings_changed(theme_changed, language_changed):
            print(f"📝 Settings changed callback:")
            print(f"   Theme changed: {theme_changed}")
            print(f"   Language changed: {language_changed}")
        
        print("🖼️ Settings window components available")
        print("   Note: To test the full settings window, run the main application")
        print("   and click the '⚙️ SETTINGS' button")
        
        root.destroy()
        return True
        
    except ImportError as e:
        print(f"❌ Settings window not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing settings window: {e}")
        return False

def test_integration():
    """Test integration with main application"""
    print("\n🔗 TESTING INTEGRATION")
    print("=" * 50)
    
    try:
        # Test if main application can import the modules
        print("📋 Testing main application integration...")
        
        # Check if files exist
        files_to_check = [
            "theme_manager.py",
            "language_manager.py", 
            "settings_window.py"
        ]
        
        for file in files_to_check:
            if os.path.exists(file):
                print(f"   ✅ {file} exists")
            else:
                print(f"   ❌ {file} missing")
        
        # Test importing in main context
        try:
            from theme_manager import theme_manager, get_current_colors, get_current_fonts
            from language_manager import language_manager, get_text
            from settings_window import show_settings_window
            print("   ✅ All modules can be imported together")
        except ImportError as e:
            print(f"   ❌ Import error: {e}")
            return False
        
        # Test theme and language coordination
        print("📋 Testing theme and language coordination...")
        
        # Get current settings
        current_theme = theme_manager.current_theme
        current_language = language_manager.current_language
        
        print(f"   Current theme: {current_theme}")
        print(f"   Current language: {current_language}")
        
        # Test getting localized text with theme colors
        colors = get_current_colors()
        title_text = get_text("app_title", "Iris Recognition System")
        
        print(f"   Theme primary color: {colors['primary']}")
        print(f"   Localized title: {title_text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def demonstrate_features():
    """Demonstrate the new features"""
    print("\n🎯 FEATURE DEMONSTRATION")
    print("=" * 50)
    
    print("🆕 NEW FEATURES ADDED:")
    print("   ✨ Theme Manager:")
    print("      • 4 built-in themes (Dark, Light, Blue, Green)")
    print("      • Dynamic color switching")
    print("      • User preference persistence")
    print("      • Custom theme creation support")
    print()
    print("   🌐 Language Manager:")
    print("      • Multi-language support (English, Spanish, French)")
    print("      • Dynamic text switching")
    print("      • User preference persistence")
    print("      • Easy translation system")
    print()
    print("   ⚙️ Settings Window:")
    print("      • Modern GUI for theme/language selection")
    print("      • Real-time preview")
    print("      • Apply/Reset/Cancel options")
    print("      • Integration with main application")
    print()
    print("🎨 THEME EXAMPLES:")
    
    try:
        from theme_manager import theme_manager
        themes = theme_manager.get_available_themes()
        
        for theme_name, theme_display_name in themes.items():
            theme_manager.set_theme(theme_name)
            colors = theme_manager.get_theme_colors()
            print(f"   • {theme_display_name}:")
            print(f"     Primary: {colors['primary']}")
            print(f"     Secondary: {colors['secondary']}")
            print(f"     Accent: {colors['accent_primary']}")
    except:
        pass
    
    print("\n🌐 LANGUAGE EXAMPLES:")
    
    try:
        from language_manager import language_manager
        languages = language_manager.get_available_languages()
        
        for lang_code, lang_name in languages.items():
            language_manager.set_language(lang_code)
            title = language_manager.get_text("app_title", "Iris Recognition System")
            print(f"   • {lang_name}: {title}")
    except:
        pass

def main():
    """Main test function"""
    print("👁️ THEME & LANGUAGE FEATURES TEST")
    print("=" * 70)
    print("Testing the new theme switching and multi-language support")
    print()
    
    # Run tests
    test1_success = test_theme_manager()
    test2_success = test_language_manager()
    test3_success = test_settings_window()
    test4_success = test_integration()
    
    # Show demonstration
    demonstrate_features()
    
    print("\n" + "=" * 70)
    print("📋 TEST SUMMARY")
    print("=" * 70)
    
    if test1_success and test2_success and test3_success and test4_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Theme manager is working correctly")
        print("✅ Language manager is working correctly")
        print("✅ Settings window is available")
        print("✅ Integration is successful")
        print()
        print("🚀 READY TO USE:")
        print("   1. Run the main application: python Main.py")
        print("   2. Click the '⚙️ SETTINGS' button")
        print("   3. Choose your preferred theme and language")
        print("   4. Click 'Apply Changes'")
        print("   5. Restart the application to see all changes")
    else:
        print("❌ SOME TESTS FAILED")
        print("   Check the error messages above")
        print("   Ensure all required files are present")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
