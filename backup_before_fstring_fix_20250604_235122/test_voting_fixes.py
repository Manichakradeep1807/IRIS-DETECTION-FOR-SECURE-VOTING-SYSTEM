#!/usr/bin/env python3
"""
Test script to verify voting system fixes
Tests the CAST VOTE button visibility and party selection functionality
"""

import tkinter as tk
import sys
import os

def test_voting_system_fixes():
    """Test the voting system fixes"""
    print("🔍 Testing Voting System Fixes...")
    print("=" * 50)
    
    try:
        # Import voting system
        from voting_system import voting_system, show_voting_interface, show_enhanced_voting_interface
        print("✅ Voting system imported successfully")
        
        # Test database initialization
        parties = voting_system.get_parties()
        print(f"✅ Found {len(parties)} political parties")
        
        for party in parties:
            print(f"   - {party['symbol']} {party['name']}")
        
        # Create test window
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        print("\n🗳️ Testing Basic Voting Interface...")
        print("   - CAST VOTE button should be visible but disabled initially")
        print("   - Button should change when party is selected")
        print("   - Party selection should work properly")
        
        # Test basic voting interface
        def test_basic_interface():
            try:
                show_voting_interface(person_id=999, confidence_score=0.95)
                print("✅ Basic voting interface opened successfully")
                return True
            except Exception as e:
                print(f"❌ Basic voting interface failed: {e}")
                return False
        
        # Test enhanced voting interface
        def test_enhanced_interface():
            try:
                # Create a dummy iris image path
                dummy_image_path = "test_iris.jpg"
                show_enhanced_voting_interface(person_id=998, confidence_score=0.95, iris_image_path=dummy_image_path)
                print("✅ Enhanced voting interface opened successfully")
                return True
            except Exception as e:
                print(f"❌ Enhanced voting interface failed: {e}")
                return False
        
        print("\n🧪 Running Interface Tests...")
        
        # Test basic interface
        basic_result = test_basic_interface()
        
        # Wait a moment
        root.after(2000, lambda: test_enhanced_interface())
        
        # Start the GUI event loop
        print("\n📋 Manual Testing Instructions:")
        print("1. Check if CAST VOTE button is visible")
        print("2. Try selecting different parties")
        print("3. Verify button changes from disabled to enabled")
        print("4. Test clicking the CAST VOTE button")
        print("5. Close the voting windows when done")
        print("\n⚠️ Close all voting windows to complete the test")
        
        root.mainloop()
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure voting_system.py exists and is properly configured")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Voting System Fix Verification")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('voting_system.py'):
        print("❌ voting_system.py not found!")
        print("💡 Make sure you're running this from the mini project directory")
        return False
    
    # Run the test
    result = test_voting_system_fixes()
    
    if result:
        print("\n✅ Voting system test completed!")
        print("📋 Check the manual testing results above")
    else:
        print("\n❌ Voting system test failed!")
        print("💡 Check the error messages above for details")
    
    return result

if __name__ == "__main__":
    main()
