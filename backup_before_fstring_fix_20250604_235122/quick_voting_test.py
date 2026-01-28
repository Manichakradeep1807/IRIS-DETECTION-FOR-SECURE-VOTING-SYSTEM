#!/usr/bin/env python3
"""
Quick test to verify voting system functionality and button visibility
"""

import tkinter as tk
import sys
import os

def quick_test():
    """Quick test of voting system"""
    print("🚀 QUICK VOTING SYSTEM TEST")
    print("=" * 40)
    
    try:
        # Test import
        print("📦 Testing imports...")
        from voting_system import voting_system, show_enhanced_voting_interface
        print("✅ Voting system imported successfully")
        
        # Test database
        print("\n🗄️ Testing database...")
        parties = voting_system.get_parties()
        print(f"✅ Found {len(parties)} parties")
        
        # Show first few parties
        for i, party in enumerate(parties[:3], 1):
            print(f"   {i}. {party['symbol']} {party['name']}")
        
        # Test voting interface
        print("\n🗳️ Opening enhanced voting interface...")
        print("📋 Instructions:")
        print("   1. Select any party by clicking on it")
        print("   2. Watch for the CAST VOTE button to become green")
        print("   3. The button should flash gold when enabled")
        print("   4. Debug messages will appear in this console")
        print("   5. Close the voting window when done testing")
        
        # Create root window (hidden)
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Open voting interface
        show_enhanced_voting_interface(
            person_id=999, 
            confidence_score=0.95, 
            iris_image_path="test_image.jpg"
        )
        
        # Start the GUI event loop
        root.mainloop()
        
        print("\n✅ Test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Voting system test completed successfully!")
        print("💡 If the CAST VOTE button became visible and green when you selected a party,")
        print("   then the issue has been fixed!")
    else:
        print("\n❌ Test failed. Check the error messages above.")
