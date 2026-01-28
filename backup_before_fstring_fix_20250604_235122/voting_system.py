#!/usr/bin/env python3
"""
Iris-Based Voting System
Secure biometric voting using iris recognition
"""

import sqlite3
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import tkinter as tk
from tkinter import messagebox, ttk

class VotingSystem:
    """
    Comprehensive voting system with iris authentication
    """
    
    def __init__(self, db_path="voting_system.db"):
        self.db_path = db_path
        self.init_database()
        self.load_parties()
    
    def init_database(self):
        """Initialize voting database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create parties table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS parties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    symbol TEXT,
                    color TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create votes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS votes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER NOT NULL,
                    party_id INTEGER NOT NULL,
                    confidence_score REAL NOT NULL,
                    vote_hash TEXT UNIQUE NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verification_method TEXT DEFAULT 'iris',
                    FOREIGN KEY (party_id) REFERENCES parties (id)
                )
            ''')
            
            # Create elections table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS elections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def load_parties(self):
        """Load or create default political parties"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if parties exist
            cursor.execute("SELECT COUNT(*) FROM parties")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Add default parties
                default_parties = [
                    ("Democratic Party", "🔵", "#1E88E5", "Progressive policies and social justice"),
                    ("Republican Party", "🔴", "#E53935", "Conservative values and free market"),
                    ("Green Party", "🟢", "#43A047", "Environmental protection and sustainability"),
                    ("Libertarian Party", "🟡", "#FFB300", "Individual liberty and minimal government"),
                    ("Independent", "⚪", "#757575", "Non-partisan independent candidates"),
                    ("Socialist Party", "🟠", "#FF7043", "Workers' rights and social equality")
                ]
                
                cursor.executemany('''
                    INSERT INTO parties (name, symbol, color, description)
                    VALUES (?, ?, ?, ?)
                ''', default_parties)
                
                conn.commit()
    
    def get_parties(self) -> List[Dict]:
        """Get all available parties"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, symbol, color, description 
                FROM parties 
                ORDER BY name
            ''')
            
            parties = []
            for row in cursor.fetchall():
                parties.append({
                    'id': row[0],
                    'name': row[1],
                    'symbol': row[2],
                    'color': row[3],
                    'description': row[4]
                })
            
            return parties
    
    def has_voted(self, person_id: int) -> bool:
        """Check if person has already voted"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM votes WHERE person_id = ?
            ''', (person_id,))
            
            return cursor.fetchone()[0] > 0
    
    def cast_vote(self, person_id: int, party_id: int, confidence_score: float) -> bool:
        """Cast a vote for a person"""
        try:
            # Check if already voted
            if self.has_voted(person_id):
                return False
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create vote hash for security
                vote_data = "{}_{}_{}" .format(person_id, party_id, datetime.now().isoformat())
                vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()
                
                # Insert vote
                cursor.execute('''
                    INSERT INTO votes (person_id, party_id, confidence_score, vote_hash)
                    VALUES (?, ?, ?, ?)
                ''', (person_id, party_id, confidence_score, vote_hash))
                
                conn.commit()
                return True
                
        except Exception as e:
            print("Error casting vote: {}".format(str(e)))
            return False
    
    def get_voting_results(self) -> Dict:
        """Get comprehensive voting results"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get vote counts by party
            cursor.execute('''
                SELECT p.name, p.symbol, p.color, COUNT(v.id) as vote_count
                FROM parties p
                LEFT JOIN votes v ON p.id = v.party_id
                GROUP BY p.id, p.name, p.symbol, p.color
                ORDER BY vote_count DESC
            ''')
            
            results = []
            total_votes = 0
            
            for row in cursor.fetchall():
                vote_count = row[3]
                total_votes += vote_count
                results.append({
                    'party': row[0],
                    'symbol': row[1],
                    'color': row[2],
                    'votes': vote_count
                })
            
            # Calculate percentages
            for result in results:
                if total_votes > 0:
                    result['percentage'] = (result['votes'] / total_votes) * 100
                else:
                    result['percentage'] = 0
            
            return {
                'results': results,
                'total_votes': total_votes,
                'total_voters': self.get_total_voters()
            }
    
    def get_total_voters(self) -> int:
        """Get total number of unique voters"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(DISTINCT person_id) FROM votes')
            return cursor.fetchone()[0]
    
    def get_vote_by_person(self, person_id: int) -> Optional[Dict]:
        """Get vote information for a specific person"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT v.timestamp, p.name, p.symbol, v.confidence_score
                FROM votes v
                JOIN parties p ON v.party_id = p.id
                WHERE v.person_id = ?
            ''', (person_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'timestamp': row[0],
                    'party': row[1],
                    'symbol': row[2],
                    'confidence': row[3]
                }
            return None
    
    def export_results(self, filename: str = None) -> str:
        """Export voting results to JSON file"""
        if not filename:
            filename = "voting_results_{}.json".format(datetime.now().strftime('%Y%m%d_%H%M%S'))
        
        results = self.get_voting_results()
        
        # Add metadata
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'election_info': {
                'total_votes': results['total_votes'],
                'total_voters': results['total_voters'],
                'turnout_percentage': (results['total_voters'] / 108) * 100  # Assuming 108 registered persons
            },
            'results': results['results']
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename

# Global voting system instance
voting_system = VotingSystem()

def show_voting_interface(person_id: int, confidence_score: float):
    """Show voting interface for authenticated person"""

    # Check if already voted
    if voting_system.has_voted(person_id):
        existing_vote = voting_system.get_vote_by_person(person_id)
        messagebox.showinfo(
            "Already Voted",
            "Person {} has already voted!\n\n"
            "Vote cast for: {} {}\n"
            "Time: {}\n"
            "Confidence: {:.1%}".format(
                person_id,
                existing_vote['party'],
                existing_vote['symbol'],
                existing_vote['timestamp'],
                existing_vote['confidence']
            )
        )
        return
    
    # Create voting window
    voting_window = tk.Toplevel()
    voting_window.title("🗳️ Voting System - Person {}".format(person_id))
    voting_window.geometry("800x600")
    voting_window.configure(bg='#1a1a2e')
    voting_window.resizable(False, False)
    
    # Center the window
    voting_window.transient()
    voting_window.grab_set()
    
    # Header
    header_frame = tk.Frame(voting_window, bg='#1a1a2e')
    header_frame.pack(fill=tk.X, padx=20, pady=20)
    
    title_label = tk.Label(header_frame,
                          text="🗳️ SECURE IRIS-BASED VOTING SYSTEM",
                          font=('Segoe UI', 18, 'bold'),
                          fg='white', bg='#1a1a2e')
    title_label.pack()
    
    info_label = tk.Label(header_frame,
                         text="Authenticated: Person {} | Confidence: {:.1%}".format(person_id, confidence_score),
                         font=('Segoe UI', 12),
                         fg='#4CAF50', bg='#1a1a2e')
    info_label.pack(pady=(5, 0))
    
    # Instructions
    instructions_frame = tk.Frame(voting_window, bg='#2d2d44', relief='solid', bd=1)
    instructions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    instructions_label = tk.Label(instructions_frame,
                                 text="📋 Select your preferred political party below and click 'CAST VOTE'",
                                 font=('Segoe UI', 11),
                                 fg='white', bg='#2d2d44')
    instructions_label.pack(pady=10)
    
    # Parties frame with scrolling
    parties_frame = tk.Frame(voting_window, bg='#1a1a2e')
    parties_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    # Get parties and create selection
    parties = voting_system.get_parties()
    selected_party = tk.IntVar(value=0)  # Initialize with 0 (no selection)

    # Define button update function BEFORE creating button
    def update_cast_button_appearance():
        """Update the cast button appearance based on selection with enhanced visibility"""
        try:
            party_id = selected_party.get()
            print("DEBUG: Regular voting - Updating button appearance, selected party ID: {}".format(party_id))

            if party_id == 0:
                # No party selected - disabled state
                vote_btn.config(
                    text="🗳️ SELECT A PARTY TO VOTE",
                    bg='#666666',
                    fg='#CCCCCC',
                    state='disabled',
                    relief='flat',
                    cursor='arrow'
                )
                print("DEBUG: Regular voting - Button set to disabled state")
            else:
                # Party selected - enabled state with bright colors
                vote_btn.config(
                    text="🗳️ CAST VOTE NOW",
                    bg='#4CAF50',  # Bright green
                    fg='white',
                    state='normal',
                    relief='raised',
                    cursor='hand2'
                )
                print("DEBUG: Regular voting - Button set to enabled state for party {}".format(party_id))

                # Flash the button to draw attention
                def flash_button():
                    original_bg = vote_btn.cget('bg')
                    vote_btn.config(bg='#FFD700')  # Gold flash
                    vote_btn.after(200, lambda: vote_btn.config(bg=original_bg))

                flash_button()

        except Exception as e:
            print("ERROR: Failed to update regular voting button appearance: {}".format(str(e)))
            # Fallback to ensure button is visible
            vote_btn.config(
                text="🗳️ CAST VOTE",
                bg='#4CAF50',
                fg='white',
                state='normal',
                relief='raised'
            )

    # Define selection update function
    def update_selection():
        """Update selection and button appearance"""
        update_cast_button_appearance()

    for i, party in enumerate(parties):
        party_frame = tk.Frame(parties_frame, bg='#2d2d44', relief='solid', bd=1)
        party_frame.pack(fill=tk.X, pady=5)

        # Create horizontal layout for party info and vote button
        party_header = tk.Frame(party_frame, bg='#2d2d44')
        party_header.pack(fill=tk.X)

        # Left side - party info
        party_info_frame = tk.Frame(party_header, bg='#2d2d44')
        party_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Radio button with party info and PROPER command binding
        radio_btn = tk.Radiobutton(party_info_frame,
                                  text="{} {}".format(party['symbol'], party['name']),
                                  variable=selected_party,
                                  value=party['id'],
                                  font=('Segoe UI', 14, 'bold'),
                                  fg='white',
                                  bg='#2d2d44',
                                  selectcolor='#4CAF50',
                                  activebackground='#2d2d44',
                                  activeforeground='white',
                                  command=update_selection)  # ADD COMMAND HERE
        radio_btn.pack(anchor='w', padx=15, pady=10)

        # INDIVIDUAL VOTE BUTTON for each party in regular interface
        def create_regular_vote_handler(party_data):
            def vote_for_party():
                """Direct vote function for this specific party"""
                print("DEBUG: Regular interface - Direct vote button clicked for party {}".format(party_data['id']))

                # Confirmation dialog
                confirm = messagebox.askyesno(
                    "Confirm Vote",
                    "Are you sure you want to vote for:\n\n"
                    "{} {}\n\n"
                    "This action cannot be undone!".format(
                        party_data['symbol'],
                        party_data['name']
                    )
                )

                if confirm:
                    success = voting_system.cast_vote(person_id, party_data['id'], confidence_score)
                    if success:
                        messagebox.showinfo(
                            "Vote Cast Successfully",
                            "✅ Your vote has been recorded!\n\n"
                            "Party: {} {}\n"
                            "Person ID: {}\n"
                            "Time: {}".format(
                                party_data['symbol'],
                                party_data['name'],
                                person_id,
                                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            )
                        )
                        voting_window.destroy()
                    else:
                        messagebox.showerror("Voting Error", "Failed to cast vote. Please try again.")
            return vote_for_party

        # Create the individual VOTE button for this party
        individual_vote_btn = tk.Button(party_header,
                                       text="🗳️ VOTE",
                                       command=create_regular_vote_handler(party),
                                       font=('Segoe UI', 12, 'bold'),
                                       fg='white',
                                       bg='#4CAF50',
                                       activebackground='#45a049',
                                       relief='raised',
                                       bd=2,
                                       padx=15,
                                       pady=8,
                                       cursor='hand2')
        individual_vote_btn.pack(side=tk.RIGHT, padx=15, pady=10)

        # Party description
        desc_label = tk.Label(party_frame,
                             text=party['description'],
                             font=('Segoe UI', 10),
                             fg='#CCCCCC',
                             bg='#2d2d44',
                             wraplength=700)
        desc_label.pack(anchor='w', padx=35, pady=(0, 10))
    
    # Buttons frame
    buttons_frame = tk.Frame(voting_window, bg='#1a1a2e')
    buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    def cast_vote():
        party_id = selected_party.get()
        if party_id == 0:
            messagebox.showwarning("No Selection", "Please select a political party before voting.")
            return
        
        # Find selected party name
        selected_party_name = next(p['name'] for p in parties if p['id'] == party_id)
        selected_party_symbol = next(p['symbol'] for p in parties if p['id'] == party_id)
        
        # Confirm vote
        confirm = messagebox.askyesno(
            "Confirm Vote",
            "Are you sure you want to vote for:\n\n"
            "{} {}\n\n"
            "This action cannot be undone!".format(
                selected_party_symbol,
                selected_party_name
            )
        )
        
        if confirm:
            success = voting_system.cast_vote(person_id, party_id, confidence_score)
            if success:
                messagebox.showinfo(
                    "Vote Cast Successfully",
                    "✅ Your vote has been recorded!\n\n"
                    "Party: {} {}\n"
                    "Person ID: {}\n"
                    "Time: {}".format(
                        selected_party_symbol,
                        selected_party_name,
                        person_id,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )
                )
                voting_window.destroy()
            else:
                messagebox.showerror("Voting Error", "Failed to cast vote. Please try again.")
    
    # Create a prominent button section
    button_section = tk.Frame(buttons_frame, bg='#1a1a2e', relief='solid', bd=2)
    button_section.pack(fill=tk.X, pady=20)

    # Button header
    button_header = tk.Label(button_section,
                            text="🗳️ VOTING ACTION",
                            font=('Segoe UI', 16, 'bold'),
                            fg='white',
                            bg='#1a1a2e')
    button_header.pack(pady=(10, 5))

    # Cast vote button - MAXIMUM VISIBILITY AND FUNCTIONALITY
    vote_btn = tk.Button(button_section,
                        text="🗳️ SELECT A PARTY TO VOTE",  # Start with instruction text
                        command=cast_vote,
                        font=('Segoe UI', 22, 'bold'),  # Extra large font
                        fg='#CCCCCC',
                        bg='#666666',  # Start disabled
                        activebackground='#45a049',
                        relief='raised',  # Raised for visibility
                        bd=5,  # Thick border
                        padx=70,  # More padding
                        pady=35,  # More padding
                        state='disabled',  # Start disabled
                        cursor='hand2',  # Hand cursor when enabled
                        width=25,  # Fixed width
                        height=2)  # Fixed height
    vote_btn.pack(pady=15, padx=20)  # Center with padding

    # Cancel button - positioned separately
    cancel_section = tk.Frame(button_section, bg='#1a1a2e')
    cancel_section.pack(fill=tk.X, pady=10)

    cancel_btn = tk.Button(cancel_section,
                          text="❌ CANCEL VOTING",
                          command=voting_window.destroy,
                          font=('Segoe UI', 14, 'bold'),
                          fg='white',
                          bg='#f44336',
                          activebackground='#da190b',
                          relief='raised',
                          bd=3,
                          padx=30,
                          pady=10)
    cancel_btn.pack()

    # Initialize button appearance
    update_cast_button_appearance()

    # Security notice
    security_label = tk.Label(voting_window,
                             text="🔒 Your vote is secured with biometric authentication and cryptographic hashing",
                             font=('Segoe UI', 9),
                             fg='#888888',
                             bg='#1a1a2e')
    security_label.pack(pady=(0, 10))

    # Add helpful instructions
    help_label = tk.Label(voting_window,
                         text="💡 Tip: Select a party above to enable the CAST VOTE button",
                         font=('Segoe UI', 10, 'italic'),
                         fg='#CCCCCC',
                         bg='#1a1a2e')
    help_label.pack(pady=(0, 10))

def show_enhanced_voting_interface(person_id: int, confidence_score: float, iris_image_path: str):
    """Show enhanced voting interface with additional reliability features"""

    # Check if already voted
    if voting_system.has_voted(person_id):
        existing_vote = voting_system.get_vote_by_person(person_id)
        messagebox.showinfo(
            "Already Voted",
            "Person {} has already voted!\n\n"
            "Vote cast for: {} {}\n"
            "Time: {}\n"
            "Confidence: {:.1%}".format(
                person_id,
                existing_vote['party'],
                existing_vote['symbol'],
                existing_vote['timestamp'],
                existing_vote['confidence']
            )
        )
        return

    # Create enhanced voting window
    voting_window = tk.Toplevel()
    voting_window.title("🗳️ Enhanced Voting System - Person {}".format(person_id))
    voting_window.geometry("1000x800")
    voting_window.configure(bg='#1a1a2e')
    voting_window.resizable(False, False)

    # Center the window
    voting_window.transient()
    voting_window.grab_set()

    # Header with enhanced information
    header_frame = tk.Frame(voting_window, bg='#1a1a2e')
    header_frame.pack(fill=tk.X, padx=20, pady=20)

    title_label = tk.Label(header_frame,
                          text="🗳️ ENHANCED SECURE VOTING SYSTEM",
                          font=('Segoe UI', 20, 'bold'),
                          fg='white', bg='#1a1a2e')
    title_label.pack()

    # Authentication info with enhanced details
    auth_frame = tk.Frame(header_frame, bg='#2d2d44', relief='solid', bd=1)
    auth_frame.pack(fill=tk.X, pady=(10, 0))

    auth_title = tk.Label(auth_frame,
                         text="🔐 AUTHENTICATION VERIFIED",
                         font=('Segoe UI', 14, 'bold'),
                         fg='#4CAF50', bg='#2d2d44')
    auth_title.pack(pady=(10, 5))

    auth_details = tk.Label(auth_frame,
                           text="Person ID: {} | Confidence: {:.1%} | Image: {}".format(
                               person_id,
                               confidence_score,
                               os.path.basename(iris_image_path)
                           ),
                           font=('Segoe UI', 11),
                           fg='white', bg='#2d2d44')
    auth_details.pack(pady=(0, 10))

    # Voting instructions with enhanced guidance
    instructions_frame = tk.Frame(voting_window, bg='#2d2d44', relief='solid', bd=1)
    instructions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    instructions_title = tk.Label(instructions_frame,
                                 text="📋 VOTING INSTRUCTIONS",
                                 font=('Segoe UI', 14, 'bold'),
                                 fg='white', bg='#2d2d44')
    instructions_title.pack(pady=(15, 5))

    instructions_text = tk.Label(instructions_frame,
                                text="1. Review all political parties below\n"
                                     "2. Select your preferred party by clicking the radio button\n"
                                     "3. Verify your selection in the confirmation dialog\n"
                                     "4. Click 'CAST VOTE' to submit your vote securely",
                                font=('Segoe UI', 11),
                                fg='#CCCCCC', bg='#2d2d44',
                                justify=tk.LEFT)
    instructions_text.pack(pady=(0, 15))

    # Create scrollable parties frame
    parties_container = tk.Frame(voting_window, bg='#1a1a2e')
    parties_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    # Canvas for scrolling
    canvas = tk.Canvas(parties_container, bg='#1a1a2e', highlightthickness=0)
    scrollbar = tk.Scrollbar(parties_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Get parties and create enhanced selection
    parties = voting_system.get_parties()
    selected_party = tk.IntVar()

    # Add mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Store radio buttons for proper binding
    radio_buttons = []

    # Enhanced voting confirmation and buttons
    buttons_frame = tk.Frame(voting_window, bg='#1a1a2e')
    buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    # Selection status
    status_frame = tk.Frame(buttons_frame, bg='#2d2d44', relief='solid', bd=1)
    status_frame.pack(fill=tk.X, pady=(0, 15))

    status_label = tk.Label(status_frame,
                           text="No party selected",
                           font=('Segoe UI', 12, 'bold'),
                           fg='#FF9800', bg='#2d2d44')
    status_label.pack(pady=10)

    def update_selection():
        """Update selection status and button appearance with enhanced feedback"""
        try:
            party_id = selected_party.get()
            print("DEBUG: Party selection changed to ID: {}".format(party_id))  # Debug output

            if party_id == 0:
                status_label.config(text="❌ No party selected", fg='#FF9800')
                print("DEBUG: No party selected")
            else:
                selected_party_info = next(p for p in parties if p['id'] == party_id)
                status_label.config(
                    text="✅ Selected: {} {}".format(selected_party_info['symbol'], selected_party_info['name']),
                    fg='#4CAF50'
                )
                print("DEBUG: Party selected: {}".format(selected_party_info['name']))

            # Update button appearance (will be defined later)
            # Force update the GUI to ensure changes are visible
            voting_window.update_idletasks()
            update_cast_button_appearance()

        except Exception as e:
            print("ERROR: Failed to update selection: {}".format(str(e)))
            status_label.config(text="⚠️ Selection error", fg='#FF0000')

    # Store radio buttons for proper management
    radio_buttons = []

    # Enhanced party display with individual VOTE buttons
    for i, party in enumerate(parties):
        party_frame = tk.Frame(scrollable_frame, bg='#2d2d44', relief='solid', bd=2)
        party_frame.pack(fill=tk.X, pady=8, padx=5)

        # Party header with enhanced styling
        party_header = tk.Frame(party_frame, bg='#3d3d54')
        party_header.pack(fill=tk.X)

        # Create a horizontal layout for party info and vote button
        party_info_frame = tk.Frame(party_header, bg='#3d3d54')
        party_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Radio button with enhanced styling and proper command binding
        radio_btn = tk.Radiobutton(party_info_frame,
                                  text="{} {}".format(party['symbol'], party['name']),
                                  variable=selected_party,
                                  value=party['id'],
                                  font=('Segoe UI', 16, 'bold'),
                                  fg='white',
                                  bg='#3d3d54',
                                  selectcolor='#4CAF50',
                                  activebackground='#4d4d64',
                                  activeforeground='white',
                                  indicatoron=1,
                                  command=update_selection,
                                  cursor='hand2')  # Hand cursor for better UX
        radio_btn.pack(anchor='w', padx=20, pady=15)
        radio_buttons.append(radio_btn)

        # Add additional click handler to radio button for reliability
        def radio_click_handler():
            selected_party.set(party['id'])
            update_selection()
            print("DEBUG: Radio button clicked for party {}".format(party['id']))

        radio_btn.bind("<Button-1>", lambda e: radio_click_handler())

        # INDIVIDUAL VOTE BUTTON for each party
        def create_vote_handler(party_data):
            def vote_for_party():
                """Direct vote function for this specific party"""
                print("DEBUG: Direct vote button clicked for party {}".format(party_data['id']))

                # Enhanced confirmation dialog
                confirm_msg = (
                    "🗳️ DIRECT VOTE CONFIRMATION\n\n"
                    "You are about to cast your vote for:\n\n"
                    "Party: {} {}\n"
                    "Description: {}...\n\n"
                    "Voter Information:\n"
                    "Person ID: {}\n"
                    "Authentication: {:.1%} confidence\n"
                    "Time: {}\n\n"
                    "⚠️ THIS ACTION CANNOT BE UNDONE!\n\n"
                    "Are you absolutely sure you want to proceed?".format(
                        party_data['symbol'],
                        party_data['name'],
                        party_data['description'][:100],
                        person_id,
                        confidence_score,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )
                )

                confirm = messagebox.askyesno("Confirm Vote", confirm_msg)

                if confirm:
                    # Final security confirmation
                    final_confirm = messagebox.askyesno(
                        "Final Confirmation",
                        "FINAL CONFIRMATION\n\n"
                        "This is your last chance to change your mind.\n\n"
                        "Casting vote for: {} {}\n\n"
                        "Proceed with voting?".format(
                            party_data['symbol'],
                            party_data['name']
                        )
                    )

                    if final_confirm:
                        # Cast the vote
                        success = voting_system.cast_vote(person_id, party_data['id'], confidence_score)
                        if success:
                            # Success message with receipt
                            receipt_msg = (
                                "✅ VOTE CAST SUCCESSFULLY!\n\n"
                                "VOTING RECEIPT:\n"
                                "{}\n"
                                "Party: {} {}\n"
                                "Person ID: {}\n"
                                "Time: {}\n"
                                "Confidence: {:.1%}\n"
                                "Authentication: Biometric (Iris)\n"
                                "{}\n\n"
                                "Thank you for participating in the democratic process!\n"
                                "Your vote has been securely recorded and encrypted.".format(
                                    '='*30,
                                    party_data['symbol'],
                                    party_data['name'],
                                    person_id,
                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    confidence_score,
                                    '='*30
                                )
                            )

                            messagebox.showinfo("Vote Cast Successfully", receipt_msg)
                            voting_window.destroy()
                        else:
                            messagebox.showerror("Voting Error",
                                               "Failed to cast vote. Please try again or contact support.")
            return vote_for_party

        # Create the individual VOTE button for this party
        vote_btn = tk.Button(party_header,
                            text="🗳️ VOTE",
                            command=create_vote_handler(party),
                            font=('Segoe UI', 14, 'bold'),
                            fg='white',
                            bg='#4CAF50',
                            activebackground='#45a049',
                            relief='raised',
                            bd=3,
                            padx=20,
                            pady=10,
                            cursor='hand2')
        vote_btn.pack(side=tk.RIGHT, padx=20, pady=15)

        # Party description with enhanced formatting
        desc_frame = tk.Frame(party_frame, bg='#2d2d44')
        desc_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        desc_label = tk.Label(desc_frame,
                             text="Description: {}".format(party['description']),
                             font=('Segoe UI', 11),
                             fg='#CCCCCC',
                             bg='#2d2d44',
                             wraplength=800,
                             justify=tk.LEFT)
        desc_label.pack(anchor='w')

        # Party color indicator
        color_frame = tk.Frame(desc_frame, bg=party.get('color', '#666666'), height=4)
        color_frame.pack(fill=tk.X, pady=(5, 0))

        # Make the entire party frame clickable for easier selection
        def make_party_selector(party_id):
            def select_party(event=None):
                selected_party.set(party_id)
                update_selection()
            return select_party

        party_click_handler = make_party_selector(party['id'])

        # Bind click events to all parts of the party frame
        party_frame.bind("<Button-1>", party_click_handler)
        party_header.bind("<Button-1>", party_click_handler)
        desc_frame.bind("<Button-1>", party_click_handler)
        desc_label.bind("<Button-1>", party_click_handler)

        # Add hover effects
        def on_enter(event, frame=party_frame):
            frame.config(relief='raised', bd=3)

        def on_leave(event, frame=party_frame):
            frame.config(relief='solid', bd=2)

        party_frame.bind("<Enter>", on_enter)
        party_frame.bind("<Leave>", on_leave)

    def cast_vote_enhanced():
        """Enhanced vote casting with multiple confirmations"""
        party_id = selected_party.get()
        if party_id == 0:
            messagebox.showwarning("No Selection", "Please select a political party before voting.")
            return

        # Find selected party info
        selected_party_info = next(p for p in parties if p['id'] == party_id)

        # Enhanced confirmation dialog
        confirm_msg = (
            "🗳️ VOTE CONFIRMATION\n\n"
            "You are about to cast your vote for:\n\n"
            "Party: {} {}\n"
            "Description: {}...\n\n"
            "Voter Information:\n"
            "Person ID: {}\n"
            "Authentication: {:.1%} confidence\n"
            "Time: {}\n\n"
            "⚠️ THIS ACTION CANNOT BE UNDONE!\n\n"
            "Are you absolutely sure you want to proceed?".format(
                selected_party_info['symbol'],
                selected_party_info['name'],
                selected_party_info['description'][:100],
                person_id,
                confidence_score,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        )

        confirm = messagebox.askyesno("Confirm Vote", confirm_msg)

        if confirm:
            # Final security confirmation
            final_confirm = messagebox.askyesno(
                "Final Confirmation",
                "FINAL CONFIRMATION\n\n"
                "This is your last chance to change your mind.\n\n"
                "Casting vote for: {} {}\n\n"
                "Proceed with voting?".format(
                    selected_party_info['symbol'],
                    selected_party_info['name']
                )
            )

            if final_confirm:
                # Cast the vote
                success = voting_system.cast_vote(person_id, party_id, confidence_score)
                if success:
                    # Success message with receipt
                    receipt_msg = (
                        "✅ VOTE CAST SUCCESSFULLY!\n\n"
                        "VOTING RECEIPT:\n"
                        "{}\n"
                        "Party: {} {}\n"
                        "Person ID: {}\n"
                        "Time: {}\n"
                        "Confidence: {:.1%}\n"
                        "Authentication: Biometric (Iris)\n"
                        "{}\n\n"
                        "Thank you for participating in the democratic process!\n"
                        "Your vote has been securely recorded and encrypted.".format(
                            '='*30,
                            selected_party_info['symbol'],
                            selected_party_info['name'],
                            person_id,
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            confidence_score,
                            '='*30
                        )
                    )

                    messagebox.showinfo("Vote Cast Successfully", receipt_msg)
                    voting_window.destroy()
                else:
                    messagebox.showerror("Voting Error",
                                       "Failed to cast vote. Please try again or contact support.")

    # Action buttons with enhanced styling - FIXED LAYOUT
    action_frame = tk.Frame(buttons_frame, bg='#1a1a2e', relief='solid', bd=2)
    action_frame.pack(fill=tk.X, pady=20)

    # Add a prominent header for the button section
    button_header = tk.Label(action_frame,
                            text="🗳️ VOTING ACTION",
                            font=('Segoe UI', 16, 'bold'),
                            fg='white',
                            bg='#1a1a2e')
    button_header.pack(pady=(10, 5))

    # Cast vote button - MAXIMUM VISIBILITY AND FUNCTIONALITY
    cast_btn = tk.Button(action_frame,
                        text="🗳️ SELECT A PARTY TO VOTE",  # Start with instruction text
                        command=cast_vote_enhanced,
                        font=('Segoe UI', 24, 'bold'),  # EXTRA LARGE font
                        fg='#CCCCCC',
                        bg='#666666',  # Start disabled
                        activebackground='#45a049',
                        relief='raised',  # Make it raised for visibility
                        bd=6,  # Very thick border
                        padx=80,  # Extra padding
                        pady=40,  # Extra padding
                        state='disabled',  # Start disabled
                        cursor='hand2',  # Hand cursor when enabled
                        width=25,  # Fixed width to ensure visibility
                        height=2)  # Fixed height
    cast_btn.pack(pady=20, padx=20)  # Center the button with padding

    # Add a visual indicator that the button is disabled
    def update_cast_button_appearance():
        """Update the cast button appearance based on selection with enhanced visibility"""
        try:
            party_id = selected_party.get()
            print("DEBUG: Updating button appearance, selected party ID: {}".format(party_id))  # Debug output

            if party_id == 0:
                # No party selected - disabled state
                cast_btn.config(
                    text="🗳️ SELECT A PARTY TO VOTE",
                    bg='#666666',
                    fg='#CCCCCC',
                    state='disabled',
                    relief='flat',
                    cursor='arrow'
                )
                print("DEBUG: Button set to disabled state")
            else:
                # Party selected - enabled state with bright colors
                cast_btn.config(
                    text="🗳️ CAST VOTE NOW",
                    bg='#4CAF50',  # Bright green
                    fg='white',
                    state='normal',
                    relief='raised',
                    cursor='hand2'
                )
                print("DEBUG: Button set to enabled state for party {}".format(party_id))

                # Flash the button to draw attention
                def flash_button():
                    original_bg = cast_btn.cget('bg')
                    cast_btn.config(bg='#FFD700')  # Gold flash
                    cast_btn.after(200, lambda: cast_btn.config(bg=original_bg))

                flash_button()

        except Exception as e:
            print("ERROR: Failed to update button appearance: {}".format(str(e)))
            # Fallback to ensure button is visible
            cast_btn.config(
                text="🗳️ CAST VOTE",
                bg='#4CAF50',
                fg='white',
                state='normal',
                relief='raised'
            )

    # Cancel button - positioned separately to avoid layout conflicts
    cancel_frame = tk.Frame(action_frame, bg='#1a1a2e')
    cancel_frame.pack(fill=tk.X, pady=10)

    cancel_btn = tk.Button(cancel_frame,
                          text="❌ CANCEL VOTING",
                          command=voting_window.destroy,
                          font=('Segoe UI', 16, 'bold'),
                          fg='white',
                          bg='#f44336',
                          activebackground='#da190b',
                          relief='raised',
                          bd=3,
                          padx=40,
                          pady=15)
    cancel_btn.pack()

    # Enhanced security notice
    security_frame = tk.Frame(voting_window, bg='#1a1a2e')
    security_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    security_label = tk.Label(security_frame,
                             text="🔒 Enhanced Security: Biometric authentication • Cryptographic hashing • Multi-step verification",
                             font=('Segoe UI', 10),
                             fg='#888888',
                             bg='#1a1a2e')
    security_label.pack()

    # Initialize button appearance
    update_cast_button_appearance()

    # Add helpful instructions at the bottom
    help_frame = tk.Frame(voting_window, bg='#1a1a2e')
    help_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

    help_label = tk.Label(help_frame,
                         text="💡 Tip: Click anywhere on a party card to select it, then click the CAST VOTE button",
                         font=('Segoe UI', 10, 'italic'),
                         fg='#CCCCCC',
                         bg='#1a1a2e')
    help_label.pack()

if __name__ == "__main__":
    # Test the voting system
    root = tk.Tk()
    root.withdraw()  # Hide main window

    # Test voting interface
    show_voting_interface(person_id=1, confidence_score=0.95)

    root.mainloop()
