"""
Test script to verify that analytics feature has been completely removed
"""

import os
import sys

def test_analytics_removal():
    """Test that analytics feature has been completely removed"""
    print("🧪 Testing Analytics Feature Removal")
    print("=" * 50)
    
    # Test 1: Check if analytics files are removed
    print("\n📁 Testing file removal...")
    analytics_files = [
        'analytics_dashboard.py',
        'test_analytics.py', 
        'verify_analytics.py',
        'test_train_and_analytics.py'
    ]
    
    removed_files = []
    for file in analytics_files:
        if not os.path.exists(file):
            removed_files.append(file)
            print(f"   ✅ {file} - REMOVED")
        else:
            print(f"   ❌ {file} - STILL EXISTS")
    
    # Test 2: Check Main.py for analytics references
    print("\n📄 Testing Main.py for analytics references...")
    try:
        with open('Main.py', 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        analytics_keywords = [
            'show_analytics_dashboard',
            'VIEW ANALYTICS',
            'view_analytics',
            'Analytics Dashboard',
            'analytics_dashboard'
        ]
        
        found_references = []
        for keyword in analytics_keywords:
            if keyword in main_content:
                found_references.append(keyword)
        
        if found_references:
            print(f"   ❌ Found analytics references: {found_references}")
        else:
            print("   ✅ No analytics references found in Main.py")
            
    except Exception as e:
        print(f"   ❌ Error reading Main.py: {e}")
    
    # Test 3: Test import of Main.py
    print("\n🔧 Testing Main.py import...")
    try:
        import Main
        print("   ✅ Main.py imports successfully")
        
        # Check if analytics function exists
        if hasattr(Main, 'show_analytics_dashboard'):
            print("   ❌ show_analytics_dashboard function still exists")
        else:
            print("   ✅ show_analytics_dashboard function removed")
            
    except Exception as e:
        print(f"   ❌ Error importing Main.py: {e}")
    
    # Test 4: Check voice commands
    print("\n🎤 Testing voice commands...")
    try:
        from voice_commands import VoiceCommandSystem
        voice_system = VoiceCommandSystem()
        
        # Check if analytics command is removed
        if hasattr(voice_system, '_handle_view_analytics'):
            print("   ❌ _handle_view_analytics method still exists")
        else:
            print("   ✅ _handle_view_analytics method removed")
            
    except Exception as e:
        print(f"   ❌ Error testing voice commands: {e}")
    
    # Test 5: Check README.md
    print("\n📖 Testing README.md...")
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        analytics_refs = [
            'analytics',
            'Analytics',
            'VIEW ANALYTICS'
        ]
        
        found_readme_refs = []
        for ref in analytics_refs:
            if ref in readme_content:
                found_readme_refs.append(ref)
        
        if found_readme_refs:
            print(f"   ⚠️ Found analytics references in README: {found_readme_refs}")
        else:
            print("   ✅ No analytics references found in README.md")
            
    except Exception as e:
        print(f"   ❌ Error reading README.md: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 ANALYTICS REMOVAL TEST SUMMARY")
    print("=" * 50)
    
    total_tests = 5
    passed_tests = 0
    
    if len(removed_files) == len(analytics_files):
        print("✅ File removal: PASS")
        passed_tests += 1
    else:
        print("❌ File removal: FAIL")
    
    if not found_references:
        print("✅ Main.py cleanup: PASS")
        passed_tests += 1
    else:
        print("❌ Main.py cleanup: FAIL")
    
    try:
        import Main
        if not hasattr(Main, 'show_analytics_dashboard'):
            print("✅ Function removal: PASS")
            passed_tests += 1
        else:
            print("❌ Function removal: FAIL")
    except:
        print("❌ Function removal: FAIL")
    
    try:
        from voice_commands import VoiceCommandSystem
        voice_system = VoiceCommandSystem()
        if not hasattr(voice_system, '_handle_view_analytics'):
            print("✅ Voice commands cleanup: PASS")
            passed_tests += 1
        else:
            print("❌ Voice commands cleanup: FAIL")
    except:
        print("❌ Voice commands cleanup: FAIL")
    
    if not found_readme_refs:
        print("✅ README cleanup: PASS")
        passed_tests += 1
    else:
        print("⚠️ README cleanup: PARTIAL")
        passed_tests += 0.5
    
    success_rate = (passed_tests / total_tests) * 100
    print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 Analytics feature successfully removed!")
        return True
    else:
        print("⚠️ Some analytics references may still exist")
        return False

if __name__ == "__main__":
    success = test_analytics_removal()
    sys.exit(0 if success else 1)
