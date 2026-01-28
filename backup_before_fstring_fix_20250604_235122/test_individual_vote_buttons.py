#!/usr/bin/env python3
"""
Test script to verify individual VOTE buttons for each party
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_individual_vote_buttons():
    """Test the individual vote buttons for each party"""
    print("🗳️ TESTING INDIVIDUAL VOTE BUTTONS")
    print("=" * 50)
    
    try:
        # Import voting system
        from voting_system import voting_system, show_enhanced_voting_interface, show_voting_interface
        
        print("✅ Voting system imported successfully")
        
        # Test database
        parties = voting_system.get_parties()
        print(f"✅ Found {len(parties)} political parties")
        
        # Show party list
        print("\n📋 Available parties:")
        for i, party in enumerate(parties, 1):
            print(f"   {i}. {party['symbol']} {party['name']}")
        
        # Create test GUI
        root = tk.Tk()
        root.title("🗳️ Individual Vote Buttons Test")
        root.geometry("800x600")
        root.configure(bg='#1a1a2e')
        
        # Title
        title_label = tk.Label(root,
                              text="🗳️ INDIVIDUAL VOTE BUTTONS TEST",
                              font=('Segoe UI', 20, 'bold'),
                              fg='white',
                              bg='#1a1a2e')
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(root,
                               text="This test verifies that each party has its own VOTE button.\n\n"
                                    "NEW FEATURES TO LOOK FOR:\n"
                                    "✅ Each party has a green 'VOTE' button on the right side\n"
                                    "✅ You can vote directly without selecting first\n"
                                    "✅ Buttons are clearly visible and clickable\n"
                                    "✅ Voting works immediately when button is clicked\n"
                                    "✅ Both regular and enhanced interfaces have vote buttons",
                               font=('Segoe UI', 12),
                               fg='#CCCCCC',
                               bg='#1a1a2e',
                               justify=tk.LEFT)
        instructions.pack(pady=20, padx=20)
        
        # Test buttons frame
        test_frame = tk.Frame(root, bg='#2d2d44', relief='solid', bd=2)
        test_frame.pack(fill=tk.X, padx=30, pady=20)
        
        test_header = tk.Label(test_frame,
                              text="🧪 TEST INTERFACES",
                              font=('Segoe UI', 16, 'bold'),
                              fg='white',
                              bg='#2d2d44')
        test_header.pack(pady=(15, 10))
        
        # Test buttons
        def open_regular_voting():
            print("\n🗳️ Opening REGULAR voting interface with individual vote buttons...")
            print("📋 Look for:")
            print("   • Green 'VOTE' button next to each party name")
            print("   • Buttons on the right side of each party")
            print("   • Direct voting without radio button selection")
            
            show_voting_interface(person_id=998, confidence_score=0.93)
        
        def open_enhanced_voting():
            print("\n🗳️ Opening ENHANCED voting interface with individual vote buttons...")
            print("📋 Look for:")
            print("   • Green 'VOTE' button next to each party name")
            print("   • Buttons positioned on the right side")
            print("   • Direct voting capability")
            print("   • Enhanced confirmation dialogs")
            
            show_enhanced_voting_interface(
                person_id=999, 
                confidence_score=0.95, 
                iris_image_path="test_image.jpg"
            )
        
        regular_btn = tk.Button(test_frame,
                               text="🗳️ Test Regular Interface",
                               command=open_regular_voting,
                               font=('Segoe UI', 14, 'bold'),
                               fg='white',
                               bg='#2196F3',
                               activebackground='#1976D2',
                               relief='raised',
                               bd=3,
                               padx=30,
                               pady=15)
        regular_btn.pack(pady=10)
        
        enhanced_btn = tk.Button(test_frame,
                                text="🗳️ Test Enhanced Interface",
                                command=open_enhanced_voting,
                                font=('Segoe UI', 14, 'bold'),
                                fg='white',
                                bg='#FF9800',
                                activebackground='#F57C00',
                                relief='raised',
                                bd=3,
                                padx=30,
                                pady=15)
        enhanced_btn.pack(pady=10)
        
        # Expected behavior
        behavior_frame = tk.Frame(root, bg='#2d2d44', relief='solid', bd=2)
        behavior_frame.pack(fill=tk.X, padx=30, pady=20)
        
        behavior_label = tk.Label(behavior_frame,
                                 text="🎯 EXPECTED BEHAVIOR:\n\n"
                                      "1. Each party shows: [Radio Button] Party Name [VOTE Button]\n"
                                      "2. VOTE buttons are green and clearly visible\n"
                                      "3. Click any VOTE button to vote directly for that party\n"
                                      "4. Confirmation dialog appears when voting\n"
                                      "5. Vote is recorded and window closes\n"
                                      "6. No need to select radio button first\n"
                                      "7. Both interfaces have individual vote buttons",
                                 font=('Segoe UI', 11),
                                 fg='white',
                                 bg='#2d2d44',
                                 justify=tk.LEFT)
        behavior_label.pack(pady=15, padx=15)
        
        # Status
        status_label = tk.Label(root,
                               text="✅ Ready to test individual vote buttons!",
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
        print("📋 Click the test buttons above to verify individual vote buttons")
        
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🗳️ INDIVIDUAL VOTE BUTTONS TEST")
    print("=" * 70)
    print("This test verifies that each party has its own VOTE button.")
    print()
    
    success = test_individual_vote_buttons()
    
    if success:
        print("\n✅ Test interface completed!")
        print("💡 If you saw green VOTE buttons next to each party")
        print("   and could vote directly by clicking them, then")
        print("   the individual vote buttons feature is working!")
    else:
        print("\n❌ Test failed!")
        print("💡 Check the error messages above.")

if __name__ == "__main__":
    main()
