#!/usr/bin/env python3
"""
Debug script to check if the voting button is actually being created and displayed
"""

import tkinter as tk
from tkinter import messagebox
import sys

def debug_voting_button():
    """Create a simple voting interface to debug button visibility"""
    print("🔍 DEBUGGING VOTING BUTTON VISIBILITY")
    print("=" * 50)
    
    # Create main window
    root = tk.Tk()
    root.title("🗳️ Debug Voting Button")
    root.geometry("800x600")
    root.configure(bg='#1a1a2e')
    
    # Title
    title_label = tk.Label(root,
                          text="🗳️ VOTING BUTTON DEBUG TEST",
                          font=('Segoe UI', 18, 'bold'),
                          fg='white',
                          bg='#1a1a2e')
    title_label.pack(pady=20)
    
    # Instructions
    instructions = tk.Label(root,
                           text="This test creates a simplified voting interface\n"
                                "to check if the CAST VOTE button appears correctly.",
                           font=('Segoe UI', 12),
                           fg='#CCCCCC',
                           bg='#1a1a2e')
    instructions.pack(pady=10)
    
    # Create a simple party selection
    party_frame = tk.Frame(root, bg='#2d2d44', relief='solid', bd=2)
    party_frame.pack(fill=tk.X, padx=50, pady=20)
    
    party_label = tk.Label(party_frame,
                          text="📋 SELECT A PARTY:",
                          font=('Segoe UI', 14, 'bold'),
                          fg='white',
                          bg='#2d2d44')
    party_label.pack(pady=10)
    
    # Party selection variable
    selected_party = tk.IntVar(value=0)
    
    # Create some test parties
    parties = [
        {"id": 1, "name": "Democratic Party", "symbol": "🔵"},
        {"id": 2, "name": "Republican Party", "symbol": "🔴"},
        {"id": 3, "name": "Green Party", "symbol": "🟢"}
    ]
    
    # Create radio buttons
    for party in parties:
        radio_btn = tk.Radiobutton(party_frame,
                                  text=f"{party['symbol']} {party['name']}",
                                  variable=selected_party,
                                  value=party['id'],
                                  font=('Segoe UI', 12),
                                  fg='white',
                                  bg='#2d2d44',
                                  selectcolor='#4CAF50',
                                  activebackground='#2d2d44',
                                  command=lambda: update_button())
        radio_btn.pack(anchor='w', padx=20, pady=5)
    
    # Status label
    status_label = tk.Label(root,
                           text="❌ No party selected",
                           font=('Segoe UI', 12, 'bold'),
                           fg='#FF9800',
                           bg='#1a1a2e')
    status_label.pack(pady=10)
    
    # Button frame
    button_frame = tk.Frame(root, bg='#1a1a2e')
    button_frame.pack(fill=tk.X, padx=50, pady=20)
    
    # Create the CAST VOTE button with maximum visibility
    cast_vote_btn = tk.Button(button_frame,
                             text="🗳️ SELECT A PARTY TO VOTE",
                             font=('Segoe UI', 20, 'bold'),
                             fg='#CCCCCC',
                             bg='#666666',
                             relief='flat',
                             bd=5,
                             padx=60,
                             pady=30,
                             state='disabled')
    cast_vote_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Test button to verify layout
    test_btn = tk.Button(button_frame,
                        text="✅ TEST BUTTON",
                        font=('Segoe UI', 16, 'bold'),
                        fg='white',
                        bg='#2196F3',
                        relief='raised',
                        bd=3,
                        padx=30,
                        pady=15)
    test_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Cancel button
    cancel_btn = tk.Button(button_frame,
                          text="❌ CLOSE",
                          command=root.destroy,
                          font=('Segoe UI', 14, 'bold'),
                          fg='white',
                          bg='#f44336',
                          relief='flat',
                          padx=20,
                          pady=15)
    cancel_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def update_button():
        """Update button based on selection"""
        party_id = selected_party.get()
        print(f"DEBUG: Party selected: {party_id}")
        
        if party_id == 0:
            # No selection
            cast_vote_btn.config(
                text="🗳️ SELECT A PARTY TO VOTE",
                bg='#666666',
                fg='#CCCCCC',
                state='disabled',
                relief='flat'
            )
            status_label.config(text="❌ No party selected", fg='#FF9800')
            print("DEBUG: Button disabled")
        else:
            # Party selected
            selected_party_name = next(p['name'] for p in parties if p['id'] == party_id)
            cast_vote_btn.config(
                text="🗳️ CAST VOTE NOW",
                bg='#4CAF50',
                fg='white',
                state='normal',
                relief='raised'
            )
            status_label.config(text=f"✅ Selected: {selected_party_name}", fg='#4CAF50')
            print(f"DEBUG: Button enabled for {selected_party_name}")
            
            # Flash effect
            def flash():
                cast_vote_btn.config(bg='#FFD700')
                root.after(200, lambda: cast_vote_btn.config(bg='#4CAF50'))
            flash()
    
    # Add debug info
    debug_frame = tk.Frame(root, bg='#1a1a2e')
    debug_frame.pack(fill=tk.X, padx=50, pady=10)
    
    debug_label = tk.Label(debug_frame,
                          text="🔍 DEBUG INFO:\n"
                               "• The CAST VOTE button should appear above\n"
                               "• It should be gray when no party is selected\n"
                               "• It should turn green when you select a party\n"
                               "• Check the console for debug messages",
                          font=('Segoe UI', 10),
                          fg='#888888',
                          bg='#1a1a2e',
                          justify=tk.LEFT)
    debug_label.pack()
    
    # Initialize button state
    update_button()
    
    print("✅ Debug voting interface created")
    print("📋 Look for the CAST VOTE button in the window")
    print("🔍 Try selecting different parties to see if the button changes")
    
    root.mainloop()

if __name__ == "__main__":
    debug_voting_button()
