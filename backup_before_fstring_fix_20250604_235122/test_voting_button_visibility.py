#!/usr/bin/env python3
"""
Test script to verify that the voting button visibility issue is fixed
This script tests both the regular and enhanced voting interfaces
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import traceback

def test_voting_button_visibility():
    """Test the voting button visibility and functionality"""
    print("🔍 TESTING VOTING BUTTON VISIBILITY")
    print("=" * 50)
    
    try:
        # Import voting system
        from voting_system import voting_system, show_voting_interface, show_enhanced_voting_interface
        
        print("✅ Voting system imported successfully")
        
        # Test 1: Check if voting system has parties
        parties = voting_system.get_parties()
        print(f"✅ Found {len(parties)} political parties:")
        for i, party in enumerate(parties[:3], 1):
            print(f"   {i}. {party['symbol']} {party['name']}")
        
        if len(parties) == 0:
            print("❌ ERROR: No parties found in voting system!")
            return False
        
        # Test 2: Test regular voting interface
        print("\n🔍 Testing regular voting interface...")
        
        def test_regular_interface():
            try:
                show_voting_interface(person_id=999, confidence_score=0.95)
                print("✅ Regular voting interface opened successfully")
                return True
            except Exception as e:
                print(f"❌ Regular voting interface failed: {e}")
                traceback.print_exc()
                return False
        
        # Test 3: Test enhanced voting interface
        print("\n🔍 Testing enhanced voting interface...")
        
        def test_enhanced_interface():
            try:
                # Create a dummy iris image path
                dummy_iris_path = "test_iris.jpg"
                show_enhanced_voting_interface(person_id=998, confidence_score=0.92, iris_image_path=dummy_iris_path)
                print("✅ Enhanced voting interface opened successfully")
                return True
            except Exception as e:
                print(f"❌ Enhanced voting interface failed: {e}")
                traceback.print_exc()
                return False
        
        # Create test GUI
        root = tk.Tk()
        root.title("🗳️ Voting Button Visibility Test")
        root.geometry("600x400")
        root.configure(bg='#1a1a2e')
        
        # Test instructions
        instructions = tk.Label(root,
                               text="VOTING BUTTON VISIBILITY TEST\n\n"
                                    "This test will open voting interfaces to verify\n"
                                    "that the CAST VOTE button is visible and functional.\n\n"
                                    "Instructions:\n"
                                    "1. Click a test button below\n"
                                    "2. In the voting window, select a party\n"
                                    "3. Verify the CAST VOTE button becomes visible and green\n"
                                    "4. Close the voting window and try the other test",
                               font=('Segoe UI', 12),
                               fg='white',
                               bg='#1a1a2e',
                               justify=tk.LEFT)
        instructions.pack(pady=20, padx=20)
        
        # Test buttons
        button_frame = tk.Frame(root, bg='#1a1a2e')
        button_frame.pack(pady=20)
        
        regular_btn = tk.Button(button_frame,
                               text="🗳️ Test Regular Voting Interface",
                               command=test_regular_interface,
                               font=('Segoe UI', 14, 'bold'),
                               fg='white',
                               bg='#4CAF50',
                               activebackground='#45a049',
                               padx=20,
                               pady=10)
        regular_btn.pack(pady=10)
        
        enhanced_btn = tk.Button(button_frame,
                                text="🗳️ Test Enhanced Voting Interface",
                                command=test_enhanced_interface,
                                font=('Segoe UI', 14, 'bold'),
                                fg='white',
                                bg='#FF9800',
                                activebackground='#F57C00',
                                padx=20,
                                pady=10)
        enhanced_btn.pack(pady=10)
        
        # Status label
        status_label = tk.Label(root,
                               text="✅ Voting system loaded successfully!\n"
                                    "Click the test buttons above to verify button visibility.",
                               font=('Segoe UI', 11),
                               fg='#4CAF50',
                               bg='#1a1a2e')
        status_label.pack(pady=20)
        
        # Close button
        close_btn = tk.Button(root,
                             text="❌ Close Test",
                             command=root.destroy,
                             font=('Segoe UI', 12),
                             fg='white',
                             bg='#f44336',
                             activebackground='#da190b',
                             padx=20,
                             pady=5)
        close_btn.pack(pady=10)
        
        print("\n✅ Test GUI created successfully")
        print("📋 Instructions:")
        print("   1. Click 'Test Regular Voting Interface'")
        print("   2. Select a party and verify the CAST VOTE button becomes visible")
        print("   3. Close the voting window")
        print("   4. Click 'Test Enhanced Voting Interface'")
        print("   5. Repeat the verification process")
        print("\n🎯 Expected behavior:")
        print("   - Button should start as gray and disabled")
        print("   - When you select a party, button should turn green and say 'CAST VOTE NOW'")
        print("   - Button should flash gold briefly when enabled")
        print("   - Debug messages should appear in console")
        
        root.mainloop()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure voting_system.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🗳️ VOTING BUTTON VISIBILITY TEST")
    print("=" * 70)
    print("This test verifies that the voting button visibility issue is fixed.")
    print()
    
    success = test_voting_button_visibility()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("📋 If you saw the voting interfaces and the buttons worked correctly,")
        print("   then the voting button visibility issue has been fixed!")
    else:
        print("\n❌ Test failed!")
        print("💡 Check the error messages above for troubleshooting information.")

if __name__ == "__main__":
    main()
