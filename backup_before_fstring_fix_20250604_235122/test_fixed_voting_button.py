#!/usr/bin/env python3
"""
Test script to verify the fixed voting button is now visible and functional
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_fixed_voting_button():
    """Test the fixed voting button visibility"""
    print("🔍 TESTING FIXED VOTING BUTTON")
    print("=" * 50)
    
    try:
        # Import voting system
        from voting_system import voting_system, show_enhanced_voting_interface
        
        print("✅ Voting system imported successfully")
        
        # Test database
        parties = voting_system.get_parties()
        print(f"✅ Found {len(parties)} political parties")
        
        # Create test GUI
        root = tk.Tk()
        root.title("🗳️ Fixed Voting Button Test")
        root.geometry("700x500")
        root.configure(bg='#1a1a2e')
        
        # Title
        title_label = tk.Label(root,
                              text="🗳️ FIXED VOTING BUTTON TEST",
                              font=('Segoe UI', 20, 'bold'),
                              fg='white',
                              bg='#1a1a2e')
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(root,
                               text="This test verifies that the CAST VOTE button is now visible.\n\n"
                                    "WHAT TO LOOK FOR:\n"
                                    "✅ Large, prominent CAST VOTE button\n"
                                    "✅ Button starts gray and disabled\n"
                                    "✅ Button turns green when party selected\n"
                                    "✅ Button flashes gold when enabled\n"
                                    "✅ Clear 'VOTING ACTION' header above button\n"
                                    "✅ Button is centered and easy to see",
                               font=('Segoe UI', 12),
                               fg='#CCCCCC',
                               bg='#1a1a2e',
                               justify=tk.LEFT)
        instructions.pack(pady=20, padx=20)
        
        # Test button
        def open_voting_test():
            print("\n🗳️ Opening enhanced voting interface...")
            print("📋 Look for these improvements:")
            print("   • 'VOTING ACTION' header")
            print("   • Large CAST VOTE button (24pt font)")
            print("   • Button with thick border and raised relief")
            print("   • Button centered in its own section")
            print("   • Fixed width and height for consistency")
            
            show_enhanced_voting_interface(
                person_id=999, 
                confidence_score=0.95, 
                iris_image_path="test_image.jpg"
            )
        
        test_btn = tk.Button(root,
                            text="🗳️ OPEN FIXED VOTING INTERFACE",
                            command=open_voting_test,
                            font=('Segoe UI', 16, 'bold'),
                            fg='white',
                            bg='#4CAF50',
                            activebackground='#45a049',
                            relief='raised',
                            bd=3,
                            padx=40,
                            pady=20)
        test_btn.pack(pady=30)
        
        # Expected behavior
        behavior_frame = tk.Frame(root, bg='#2d2d44', relief='solid', bd=2)
        behavior_frame.pack(fill=tk.X, padx=30, pady=20)
        
        behavior_label = tk.Label(behavior_frame,
                                 text="🎯 EXPECTED BEHAVIOR:\n\n"
                                      "1. Window opens with party selection\n"
                                      "2. You see 'VOTING ACTION' header\n"
                                      "3. Large gray button says 'SELECT A PARTY TO VOTE'\n"
                                      "4. Click any party to select it\n"
                                      "5. Button turns bright green\n"
                                      "6. Button text changes to 'CAST VOTE NOW'\n"
                                      "7. Button flashes gold briefly\n"
                                      "8. Button is clearly visible and clickable",
                                 font=('Segoe UI', 11),
                                 fg='white',
                                 bg='#2d2d44',
                                 justify=tk.LEFT)
        behavior_label.pack(pady=15, padx=15)
        
        # Status
        status_label = tk.Label(root,
                               text="✅ Ready to test! Click the button above.",
                               font=('Segoe UI', 12, 'bold'),
                               fg='#4CAF50',
                               bg='#1a1a2e')
        status_label.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(root,
                             text="❌ Close Test",
                             command=root.destroy,
                             font=('Segoe UI', 12),
                             fg='white',
                             bg='#f44336',
                             activebackground='#da190b',
                             padx=20,
                             pady=10)
        close_btn.pack(pady=20)
        
        print("\n✅ Test interface ready")
        print("📋 Click 'OPEN FIXED VOTING INTERFACE' to test")
        
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🗳️ FIXED VOTING BUTTON TEST")
    print("=" * 70)
    print("This test verifies that the voting button visibility issue is now fixed.")
    print()
    
    success = test_fixed_voting_button()
    
    if success:
        print("\n✅ Test interface completed!")
        print("💡 If you saw a large, prominent CAST VOTE button that became")
        print("   green when you selected a party, then the issue is FIXED!")
    else:
        print("\n❌ Test failed!")
        print("💡 Check the error messages above.")

if __name__ == "__main__":
    main()
