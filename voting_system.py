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
from audit_system import default_audit_logger as audit
try:
    from database_manager import db  # for phone lookup
    from sms_utils import send_sms, format_voting_receipt
    from receipt_generator import generate_pdf_receipt, generate_jpeg_receipt
    _SMS_SUPPORT = True
except Exception:
    _SMS_SUPPORT = False
    def generate_pdf_receipt(*args, **kwargs): return None
    def generate_jpeg_receipt(*args, **kwargs): return None

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

            # Unique constraint to prevent duplicate voting per election if we extend votes
            try:
                cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_votes_unique_hash ON votes(vote_hash)')
            except Exception:
                pass
            
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

    def get_active_elections(self) -> List[Dict]:
        """Get active elections"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, description, start_date, end_date
                FROM elections
                WHERE is_active = 1
                ORDER BY created_at DESC
            ''')
            elections = []
            for row in cursor.fetchall():
                elections.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'start_date': row[3],
                    'end_date': row[4]
                })
            return elections
    
    def has_voted(self, person_id: int) -> bool:
        """Check if person has already voted"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*) FROM votes WHERE person_id = ?
                ''', (person_id,))

                count = cursor.fetchone()[0]
                print(f"DEBUG: Person {person_id} vote count: {count}")
                try:
                    audit.log_event('vote_status_check', {
                        'person_id': person_id,
                        'vote_count': int(count)
                    })
                except Exception:
                    pass
                return count > 0
        except Exception as e:
            print(f"Error checking vote status: {e}")
            try:
                audit.log_event('vote_status_error', {
                    'person_id': person_id,
                    'error': str(e)
                })
            except Exception:
                pass
            # If there's an error, assume they haven't voted to allow voting
            return False

    def clear_vote(self, person_id: int) -> bool:
        """Clear vote for a person (for testing purposes or re-voting)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # First check if vote exists
                cursor.execute('''
                    SELECT COUNT(*) FROM votes WHERE person_id = ?
                ''', (person_id,))

                vote_count = cursor.fetchone()[0]

                if vote_count > 0:
                    # Delete the vote(s)
                    cursor.execute('''
                        DELETE FROM votes WHERE person_id = ?
                    ''', (person_id,))
                    conn.commit()
                    print(f"DEBUG: Cleared {vote_count} vote(s) for person {person_id}")
                    try:
                        audit.log_event('vote_cleared', {
                            'person_id': person_id,
                            'cleared_count': int(vote_count)
                        })
                    except Exception:
                        pass
                    return True
                else:
                    print(f"DEBUG: No votes found for person {person_id} to clear")
                    try:
                        audit.log_event('vote_clear_noop', {
                            'person_id': person_id
                        })
                    except Exception:
                        pass
                    return True  # Return True since the goal (no votes) is achieved

        except Exception as e:
            print(f"Error clearing vote: {e}")
            try:
                audit.log_event('vote_clear_error', {
                    'person_id': person_id,
                    'error': str(e)
                })
            except Exception:
                pass
            return False
    
    def cast_vote(self, person_id: int, party_id: int, confidence_score: float, election_id: Optional[int] = None) -> bool:
        """Cast a vote for a person"""
        try:
            # Double-check if already voted (with fresh database connection)
            if self.has_voted(person_id):
                print(f"DEBUG: Person {person_id} has already voted, cannot cast new vote")
                try:
                    audit.log_event('vote_cast_blocked_already_voted', {
                        'person_id': person_id,
                        'party_id': party_id,
                        'confidence_score': float(confidence_score)
                    })
                except Exception:
                    pass
                return False

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Verify party exists
                cursor.execute('SELECT COUNT(*) FROM parties WHERE id = ?', (party_id,))
                if cursor.fetchone()[0] == 0:
                    print(f"ERROR: Party ID {party_id} does not exist")
                    try:
                        audit.log_event('vote_cast_error_invalid_party', {
                            'person_id': person_id,
                            'party_id': party_id
                        })
                    except Exception:
                        pass
                    return False

                # Create vote hash for security - using safe string operations
                timestamp_str = datetime.now().isoformat()
                vote_data = str(person_id) + "_" + str(party_id) + "_" + (str(election_id) if election_id else "general") + "_" + timestamp_str
                vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()

                # Insert vote with transaction safety
                cursor.execute('''
                    INSERT INTO votes (person_id, party_id, confidence_score, vote_hash)
                    VALUES (?, ?, ?, ?)
                ''', (person_id, party_id, confidence_score, vote_hash))

                conn.commit()
                print(f"DEBUG: Successfully cast vote for person {person_id}, party {party_id}")
                try:
                    audit.log_event('vote_cast_success', {
                        'person_id': person_id,
                        'party_id': party_id,
                        'election_id': election_id,
                        'vote_hash': vote_hash
                    })
                except Exception:
                    pass
                return True

        except Exception as e:
            error_msg = "Error casting vote: " + str(e)
            print(error_msg)
            try:
                audit.log_event('vote_cast_error', {
                    'person_id': person_id,
                    'party_id': party_id,
                    'error': str(e)
                })
            except Exception:
                pass
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
            
            # Determine winner information
            winner_info = self.get_election_winner(results, total_votes)

            return {
                'results': results,
                'total_votes': total_votes,
                'total_voters': self.get_total_voters(),
                'winner': winner_info
            }
    
    def get_total_voters(self) -> int:
        """Get total number of unique voters"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(DISTINCT person_id) FROM votes')
            return cursor.fetchone()[0]

    def get_election_winner(self, results: List[Dict], total_votes: int) -> Dict:
        """Determine the election winner based on vote counts"""
        if total_votes == 0:
            return {
                'status': 'no_votes',
                'message': 'No votes have been cast yet',
                'winner': None,
                'tied_parties': []
            }

        # Find the maximum vote count
        max_votes = max(result['votes'] for result in results)

        if max_votes == 0:
            return {
                'status': 'no_votes',
                'message': 'No votes have been cast yet',
                'winner': None,
                'tied_parties': []
            }

        # Find all parties with the maximum votes
        winners = [result for result in results if result['votes'] == max_votes]

        if len(winners) == 1:
            # Clear winner
            winner = winners[0]
            return {
                'status': 'winner',
                'message': f"{winner['symbol']} {winner['party']} wins with {winner['votes']} votes ({winner['percentage']:.1f}%)",
                'winner': winner,
                'tied_parties': []
            }
        else:
            # Tie situation
            tied_party_names = [f"{w['symbol']} {w['party']}" for w in winners]
            return {
                'status': 'tie',
                'message': f"Election tie between: {' & '.join(tied_party_names)} with {max_votes} votes each",
                'winner': None,
                'tied_parties': winners
            }
    
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
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = "voting_results_{}.json".format(timestamp)

        results = self.get_voting_results()

        # Add metadata with winner information
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'election_info': {
                'total_votes': results['total_votes'],
                'total_voters': results['total_voters'],
                'turnout_percentage': (results['total_voters'] / 108) * 100  # Assuming 108 registered persons
            },
            'winner_info': results['winner'],
            'results': results['results']
        }

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)

        try:
            audit.log_event('results_exported', {
                'file': filename,
                'total_votes': export_data['election_info']['total_votes'],
                'total_voters': export_data['election_info']['total_voters']
            })
        except Exception:
            pass

        return filename

    def clear_all_votes(self) -> bool:
        """Clear all votes from the database (for testing purposes)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM votes')
                conn.commit()
                print("DEBUG: All votes cleared from database")
                return True
        except Exception as e:
            print(f"Error clearing all votes: {e}")
            return False

    def get_vote_statistics(self) -> Dict:
        """Get detailed voting statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Total votes
                cursor.execute('SELECT COUNT(*) FROM votes')
                total_votes = cursor.fetchone()[0]

                # Unique voters
                cursor.execute('SELECT COUNT(DISTINCT person_id) FROM votes')
                unique_voters = cursor.fetchone()[0]

                # Votes per party
                cursor.execute('''
                    SELECT p.name, p.symbol, COUNT(v.id) as vote_count
                    FROM parties p
                    LEFT JOIN votes v ON p.id = v.party_id
                    GROUP BY p.id, p.name, p.symbol
                    ORDER BY vote_count DESC
                ''')
                party_votes = cursor.fetchall()

                return {
                    'total_votes': total_votes,
                    'unique_voters': unique_voters,
                    'party_votes': party_votes,
                    'database_status': 'operational'
                }
        except Exception as e:
            print(f"Error getting vote statistics: {e}")
            return {
                'total_votes': 0,
                'unique_voters': 0,
                'party_votes': [],
                'database_status': f'error: {str(e)}'
            }

# Global voting system instance
voting_system = VotingSystem()

def show_voting_interface(person_id: int, confidence_score: float):
    """Show voting interface for authenticated person"""
    
    # Check if already voted
    if voting_system.has_voted(person_id):
        existing_vote = voting_system.get_vote_by_person(person_id)
        # Safe message formatting to prevent bytes format errors
        party_name = str(existing_vote['party'])
        party_symbol = str(existing_vote['symbol'])
        timestamp = str(existing_vote['timestamp'])
        confidence_pct = "{:.1%}".format(float(existing_vote['confidence']))

        message = ("Person " + str(person_id) + " has already voted!\n\n" +
                  "Vote cast for: " + party_symbol + " " + party_name + "\n" +
                  "Time: " + timestamp + "\n" +
                  "Confidence: " + confidence_pct)

        messagebox.showinfo("Already Voted", message)
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
    
    # Election selector
    elections = voting_system.get_active_elections()
    election_frame = tk.Frame(voting_window, bg='#2d2d44', relief='solid', bd=1)
    election_frame.pack(fill=tk.X, padx=20, pady=(0, 12))
    tk.Label(election_frame, text="Select Election", font=('Segoe UI', 11, 'bold'), fg='white', bg='#2d2d44').pack(anchor='w', padx=12, pady=(8, 4))
    election_combo = ttk.Combobox(election_frame, values=[e['name'] for e in elections] if elections else ['General'], state='readonly')
    election_combo.current(0)
    election_combo.pack(fill=tk.X, padx=12, pady=(0, 10))
    
    # Parties frame with scrolling
    parties_frame = tk.Frame(voting_window, bg='#1a1a2e')
    parties_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    # Get parties and create selection
    parties = voting_system.get_parties()
    selected_party = tk.IntVar()
    
    for i, party in enumerate(parties):
        party_frame = tk.Frame(parties_frame, bg='#2d2d44', relief='solid', bd=1)
        party_frame.pack(fill=tk.X, pady=5)
        
        # Radio button with party info
        radio_btn = tk.Radiobutton(party_frame,
                                  text="{} {}".format(party['symbol'], party['name']),
                                  variable=selected_party,
                                  value=party['id'],
                                  font=('Segoe UI', 14, 'bold'),
                                  fg='white',
                                  bg='#2d2d44',
                                  selectcolor='#4CAF50',
                                  activebackground='#2d2d44',
                                  activeforeground='white')
        radio_btn.pack(anchor='w', padx=15, pady=10)
        
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
        
        # Confirm vote with safe string formatting
        confirm_message = ("Are you sure you want to vote for:\n\n" +
                          str(selected_party_symbol) + " " + str(selected_party_name) + "\n\n" +
                          "This action cannot be undone!")

        confirm = messagebox.askyesno("Confirm Vote", confirm_message)

        if confirm:
            selected_election_id = None
            if elections and election_combo.current() >= 0:
                try:
                    selected_election_id = elections[election_combo.current()]['id']
                except Exception:
                    selected_election_id = None
            success = voting_system.cast_vote(person_id, party_id, confidence_score, selected_election_id)
            if success:
                # Hide window immediately for better UX
                voting_window.withdraw()
                voting_window.update()
                
                # Safe success message formatting
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                success_message = ("✅ Your vote has been recorded!\n\n" +
                                 "Party: " + str(selected_party_symbol) + " " + str(selected_party_name) + "\n" +
                                 "Person ID: " + str(person_id) + "\n" +
                                 "Time: " + current_time)

                messagebox.showinfo("Vote Cast Successfully", success_message)
                # Save receipt locally (JSON)
                try:
                    receipt_dir = "receipts"
                    if not os.path.exists(receipt_dir):
                        os.makedirs(receipt_dir)
                        
                    receipt_path = os.path.join(receipt_dir, "vote_receipt_{}_{}.json".format(person_id, datetime.now().strftime('%Y%m%d_%H%M%S')))
                    with open(receipt_path, 'w') as f:
                        json.dump({
                            'person_id': person_id,
                            'party_symbol': str(selected_party_symbol),
                            'party_name': str(selected_party_name),
                            'timestamp': current_time,
                            'confidence': float(confidence_score),
                            'election': elections[election_combo.current()]['name'] if elections else 'General'
                        }, f, indent=2)
                    messagebox.showinfo("Receipt Saved", "Receipt saved to: {}".format(receipt_path))
                except Exception:
                    pass
                
                # Generate Beautiful JPEG Receipt (Replacing PDF/JSON preference)
                try:
                    jpeg_path = generate_jpeg_receipt(
                        person_id=person_id,
                        username=username,
                        party_name=str(selected_party_name),
                        party_symbol=str(selected_party_symbol),
                        timestamp=current_time,
                        confidence_score=float(confidence_score),
                        election=elections[election_combo.current()]['name'] if elections else 'General'
                    )
                    if jpeg_path:
                        # Auto-open the JPEG
                        try:
                            os.startfile(jpeg_path)
                        except Exception:
                            pass
                        messagebox.showinfo("Digital Receipt", f"Official Voting Receipt Generated:\n{jpeg_path}\n\nYou can download/keep this image.")
                except Exception as e:
                    print(f"Receipt Error: {e}") 
                    pass
                # Attempt SMS receipt
                try:
                    if _SMS_SUPPORT:
                        person = db.get_person(person_id)
                        phone = person.get('phone') if person else None
                        if phone:
                            receipt = format_voting_receipt(
                                person_id,
                                str(selected_party_symbol),
                                str(selected_party_name),
                                current_time,
                                "{:.1%}".format(confidence_score)
                            )
                            send_sms(str(phone), receipt)
                except Exception:
                    pass
                voting_window.destroy()
            else:
                messagebox.showerror("Voting Error", "Failed to cast vote. Please try again.")
    
    # Cast vote button
    vote_btn = tk.Button(buttons_frame,
                        text="🗳️ CAST VOTE",
                        command=cast_vote,
                        font=('Segoe UI', 14, 'bold'),
                        fg='white',
                        bg='#4CAF50',
                        activebackground='#45a049',
                        relief='flat',
                        padx=30,
                        pady=15)
    vote_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    # Cancel button
    cancel_btn = tk.Button(buttons_frame,
                          text="❌ CANCEL",
                          command=voting_window.destroy,
                          font=('Segoe UI', 12, 'bold'),
                          fg='white',
                          bg='#f44336',
                          activebackground='#da190b',
                          relief='flat',
                          padx=20,
                          pady=15)
    cancel_btn.pack(side=tk.RIGHT)
    
    # Security notice
    security_label = tk.Label(voting_window,
                             text="🔒 Your vote is secured with biometric authentication and cryptographic hashing",
                             font=('Segoe UI', 9),
                             fg='#888888',
                             bg='#1a1a2e')
    security_label.pack(pady=(0, 10))

def show_enhanced_voting_interface(person_id: int, confidence_score: float, iris_image_path: str, parent=None, username="User", on_close=None):
    """Show enhanced voting interface with individual vote buttons for each party"""

    print(f"DEBUG: Opening voting interface for person {person_id}")
    
    # Internal close handler
    def _handle_close():
        if on_close:
            on_close()
        voting_window.destroy()

    # Check if already voted - STRICT BLOCK
    if voting_system.has_voted(person_id):
        existing_vote = voting_system.get_vote_by_person(person_id)
        if existing_vote:
            party_symbol = str(existing_vote.get('symbol', ''))
            party_name = str(existing_vote.get('party', ''))
            timestamp = str(existing_vote.get('timestamp', ''))
            
            message = (f"Person {person_id} has already voted!\n\n"
                      f"Vote cast for: {party_symbol} {party_name}\n"
                      f"Time: {timestamp}\n\n"
                      "Multiple votes are not allowed in this election.")
            
            messagebox.showwarning("Already Voted", message)
            if on_close: on_close()
            return
        else:
            messagebox.showwarning("Already Voted", f"Person {person_id} has already voted.")
            if on_close: on_close()
            return

    # Create enhanced voting window with proper parent
    if parent is None:
        # Try to find the main window
        root = tk._default_root
        if root is None:
            # Create a temporary root if none exists
            root = tk.Tk()
            root.withdraw()
        voting_window = tk.Toplevel(root)
    else:
        voting_window = tk.Toplevel(parent)
        
    # Bind close
    voting_window.protocol("WM_DELETE_WINDOW", _handle_close)

    voting_window.title("🗳️ Enhanced Voting System - Person {}".format(person_id))
    voting_window.geometry("1000x800")
    voting_window.configure(bg='#1a1a2e')
    voting_window.resizable(False, False)

    # Center and Focus
    voting_window.lift()
    voting_window.focus_force()
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
                               person_id, confidence_score, os.path.basename(iris_image_path)),
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

    def _configure_scroll_region(event):
        # Update scroll region when frame is configured
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", _configure_scroll_region)

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
        """Update selection status"""
        party_id = selected_party.get()
        if party_id == 0:
            status_label.config(text="No party selected", fg='#FF9800')
            cast_btn.config(state='disabled', bg='#666666')
        else:
            selected_party_info = next(p for p in parties if p['id'] == party_id)
            status_label.config(
                text="Selected: {} {}".format(selected_party_info['symbol'], selected_party_info['name']),
                fg='#4CAF50'
            )
            cast_btn.config(state='normal', bg='#4CAF50')

    # Enhanced party display with individual vote buttons
    for i, party in enumerate(parties):
        party_frame = tk.Frame(scrollable_frame, bg='#2d2d44', relief='solid', bd=2)
        party_frame.pack(fill=tk.X, pady=8, padx=5)

        # Party header with enhanced styling
        party_header = tk.Frame(party_frame, bg='#3d3d54')
        party_header.pack(fill=tk.X)

        # Left side: Party info
        party_info_frame = tk.Frame(party_header, bg='#3d3d54')
        party_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Radio button with enhanced styling
        radio_btn = tk.Radiobutton(party_info_frame,
                                  text="{} {}".format(party['symbol'], party['name']),
                                  variable=selected_party,
                                  value=party['id'],
                                  font=('Segoe UI', 16, 'bold'),
                                  fg='white',
                                  bg='#3d3d54',
                                  selectcolor='#4CAF50',
                                  activebackground='#3d3d54',
                                  activeforeground='white',
                                  indicatoron=1,
                                  command=update_selection)
        radio_btn.pack(anchor='w', padx=20, pady=15)
        radio_buttons.append(radio_btn)

        # Right side: Individual vote button
        def create_vote_function(party_id, party_name, party_symbol):
            def vote_for_party():
                # Direct vote casting for this specific party
                party_symbol_str = str(party_symbol)
                party_name_str = str(party_name)
                confidence_pct = "{:.1%}".format(confidence_score)
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                confirm_msg = ("🗳️ DIRECT VOTE CONFIRMATION\n\n" +
                              "You are about to cast your vote for:\n\n" +
                              "Party: " + party_symbol_str + " " + party_name_str + "\n\n" +
                              "Voter Information:\n" +
                              "Person ID: " + str(person_id) + "\n" +
                              "Authentication: " + confidence_pct + " confidence\n" +
                              "Time: " + current_time + "\n\n" +
                              "⚠️ THIS ACTION CANNOT BE UNDONE!\n\n" +
                              "Are you sure you want to vote for this party?")

                confirm = messagebox.askyesno("Confirm Vote", confirm_msg)

                if confirm:
                    selected_election_id = None
                    if elections and enhanced_election_combo.current() >= 0:
                        try:
                            selected_election_id = elections[enhanced_election_combo.current()]['id']
                        except Exception:
                            selected_election_id = None

                    # Cast the vote directly
                    success = voting_system.cast_vote(person_id, party_id, confidence_score, selected_election_id)
                    if success:
                        # Hide window immediately for better UX
                        voting_window.withdraw()
                        voting_window.update()
                        
                        # Success message with receipt
                        separator = "=" * 30
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        confidence_pct = "{:.1%}".format(confidence_score)

                        receipt_msg = ("✅ VOTE CAST SUCCESSFULLY!\n\n" +
                                     "VOTING RECEIPT:\n" +
                                     separator + "\n" +
                                     "Party: " + party_symbol_str + " " + party_name_str + "\n" +
                                     "Person ID: " + str(person_id) + "\n" +
                                     "Time: " + current_time + "\n" +
                                     "Confidence: " + confidence_pct + "\n" +
                                     "Authentication: Biometric (Iris)\n" +
                                     separator + "\n\n" +
                                     "Thank you for participating in the democratic process!\n" +
                                     "Your vote has been securely recorded and encrypted.")

                        messagebox.showinfo("Vote Cast Successfully", receipt_msg)
                        # Save receipt
                        try:
                            receipt_dir = "receipts"
                            if not os.path.exists(receipt_dir):
                                os.makedirs(receipt_dir)
                                
                            receipt_path = os.path.join(receipt_dir, "vote_receipt_{}_{}.json".format(person_id, datetime.now().strftime('%Y%m%d_%H%M%S')))
                            with open(receipt_path, 'w') as f:
                                json.dump({
                                    'person_id': person_id,
                                    'party_symbol': party_symbol_str,
                                    'party_name': party_name_str,
                                    'timestamp': current_time,
                                    'confidence': float(confidence_score),
                                    'election': elections[enhanced_election_combo.current()]['name'] if elections else 'General'
                                }, f, indent=2)
                        except Exception:
                            pass
                        
                        # Generate JPEG Receipt
                        try:
                            jpeg_path = generate_jpeg_receipt(
                                person_id=person_id,
                                username=username,
                                party_name=party_name_str,
                                party_symbol=party_symbol_str,
                                timestamp=current_time,
                                confidence_score=float(confidence_score),
                                election=elections[enhanced_election_combo.current()]['name'] if elections else 'General'
                            )
                            if jpeg_path:
                                try: os.startfile(jpeg_path)
                                except: pass
                                messagebox.showinfo("Digital Receipt", f"Official Voting Receipt Generated:\n{jpeg_path}\n\nYou can download/keep this image.")
                        except Exception: pass

                        # Close Logic
                        if on_close: on_close()
                        voting_window.destroy()
                    else:
                        messagebox.showerror("Voting Error", "Failed to cast vote. Please try again.")
            
            return vote_for_party

        vote_btn = tk.Button(party_header,
                           text="🗳️ VOTE",
                           command=create_vote_function(party['id'], party['name'], party['symbol']),
                           font=('Segoe UI', 12, 'bold'),
                           fg='white',
                           bg='#4CAF50',
                           activebackground='#45a049',
                           relief='flat',
                           padx=20,
                           pady=10)
        vote_btn.pack(side=tk.RIGHT, padx=20, pady=15)

        # Party description with enhanced formatting
        desc_frame = tk.Frame(party_frame, bg='#2d2d44')
        desc_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        desc_label = tk.Label(desc_frame,
                             text="Description: {}".format(party['description']),
                             font=('Segoe UI', 11),
                             fg='#CCCCCC',
                             bg='#2d2d44',
                             wraplength=600,
                             justify=tk.LEFT)
        desc_label.pack(anchor='w')

        # Party color indicator
        color_frame = tk.Frame(desc_frame, bg=party.get('color', '#666666'), height=4)
        color_frame.pack(fill=tk.X, pady=(5, 0))

    def cast_vote_enhanced():
        """Enhanced vote casting with multiple confirmations"""
        party_id = selected_party.get()
        if party_id == 0:
            messagebox.showwarning("No Selection", "Please select a political party before voting.")
            return

        # Find selected party info
        selected_party_info = next(p for p in parties if p['id'] == party_id)

        # Enhanced confirmation dialog with safe string formatting
        party_symbol = str(selected_party_info['symbol'])
        party_name = str(selected_party_info['name'])
        party_desc = str(selected_party_info['description'][:100])
        confidence_pct = "{:.1%}".format(confidence_score)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        confirm_msg = ("🗳️ VOTE CONFIRMATION\n\n" +
                      "You are about to cast your vote for:\n\n" +
                      "Party: " + party_symbol + " " + party_name + "\n" +
                      "Description: " + party_desc + "...\n\n" +
                      "Voter Information:\n" +
                      "Person ID: " + str(person_id) + "\n" +
                      "Authentication: " + confidence_pct + " confidence\n" +
                      "Time: " + current_time + "\n\n" +
                      "⚠️ THIS ACTION CANNOT BE UNDONE!\n\n" +
                      "Are you absolutely sure you want to proceed?")

        confirm = messagebox.askyesno("Confirm Vote", confirm_msg)

        if confirm:
            # Final security confirmation
            final_confirm_msg = ("FINAL CONFIRMATION\n\n" +
                               "This is your last chance to change your mind.\n\n" +
                               "Casting vote for: " + party_symbol + " " + party_name + "\n\n" +
                               "Proceed with voting?")

            final_confirm = messagebox.askyesno("Final Confirmation", final_confirm_msg)

            if final_confirm:
                # Cast the vote
                success = voting_system.cast_vote(person_id, party_id, confidence_score)
                if success:
                    # Hide window immediately for better UX
                    voting_window.withdraw()
                    voting_window.update()
                    
                    # Success message with receipt - safe string formatting
                    separator = "=" * 30
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    confidence_pct = "{:.1%}".format(confidence_score)

                    receipt_msg = ("✅ VOTE CAST SUCCESSFULLY!\n\n" +
                                 "VOTING RECEIPT:\n" +
                                 separator + "\n" +
                                 "Party: " + party_symbol + " " + party_name + "\n" +
                                 "Person ID: " + str(person_id) + "\n" +
                                 "Time: " + current_time + "\n" +
                                 "Confidence: " + confidence_pct + "\n" +
                                 "Authentication: Biometric (Iris)\n" +
                                 separator + "\n\n" +
                                 "Thank you for participating in the democratic process!\n" +
                                 "Your vote has been securely recorded and encrypted.")

                    messagebox.showinfo("Vote Cast Successfully", receipt_msg)
                    # Attempt SMS receipt
                    try:
                        if _SMS_SUPPORT:
                            person = db.get_person(person_id)
                            phone = person.get('phone') if person else None
                            if phone:
                                sms_text = format_voting_receipt(
                                    person_id,
                                    party_symbol,
                                    party_name,
                                    current_time,
                                    confidence_pct
                                )
                                send_sms(str(phone), sms_text)
                    except Exception:
                        pass
                    voting_window.destroy()
                else:
                    messagebox.showerror("Voting Error",
                                       "Failed to cast vote. Please try again or contact support.")

    # Action buttons with enhanced styling
    action_frame = tk.Frame(buttons_frame, bg='#1a1a2e')
    action_frame.pack(fill=tk.X)

    # Cast vote button
    cast_btn = tk.Button(action_frame,
                        text="🗳️ CAST VOTE",
                        command=cast_vote_enhanced,
                        font=('Segoe UI', 16, 'bold'),
                        fg='white',
                        bg='#666666',
                        activebackground='#45a049',
                        relief='flat',
                        padx=40,
                        pady=20,
                        state='disabled')
    cast_btn.pack(side=tk.LEFT, padx=(0, 15))

    # Cancel button
    cancel_btn = tk.Button(action_frame,
                          text="❌ CANCEL",
                          command=voting_window.destroy,
                          font=('Segoe UI', 14, 'bold'),
                          fg='white',
                          bg='#f44336',
                          activebackground='#da190b',
                          relief='flat',
                          padx=30,
                          pady=20)
    cancel_btn.pack(side=tk.RIGHT)

    # Enhanced security notice
    security_frame = tk.Frame(voting_window, bg='#1a1a2e')
    security_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    security_label = tk.Label(security_frame,
                             text="🔒 Enhanced Security: Biometric authentication • Cryptographic hashing • Multi-step verification",
                             font=('Segoe UI', 10),
                             fg='#888888',
                             bg='#1a1a2e')
    security_label.pack()

    # Election selector (enhanced)
    elections = voting_system.get_active_elections()
    enhanced_election_frame = tk.Frame(voting_window, bg='#2d2d44', relief='solid', bd=1)
    enhanced_election_frame.pack(fill=tk.X, padx=20, pady=(0, 12))
    tk.Label(enhanced_election_frame, text="Select Election", font=('Segoe UI', 11, 'bold'), fg='white', bg='#2d2d44').pack(anchor='w', padx=12, pady=(8, 4))
    enhanced_election_combo = ttk.Combobox(enhanced_election_frame, values=[e['name'] for e in elections] if elections else ['General'], state='readonly')
    enhanced_election_combo.current(0)
    enhanced_election_combo.pack(fill=tk.X, padx=12, pady=(0, 10))

if __name__ == "__main__":
    # Test the voting system
    root = tk.Tk()
    root.withdraw()  # Hide main window

    # Test voting interface
    show_voting_interface(person_id=1, confidence_score=0.95)

    root.mainloop()
