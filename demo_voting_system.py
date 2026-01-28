#!/usr/bin/env python3
"""
Voting System Demo
Demonstrates the iris-based voting system functionality
"""

import tkinter as tk
from tkinter import messagebox
import time
from voting_system import voting_system, show_voting_interface
from voting_results import show_voting_results, show_individual_vote_lookup

def demo_voting_system():
    """Demonstrate the voting system with sample data"""
    
    print("🗳️ IRIS-BASED VOTING SYSTEM DEMO")
    print("=" * 50)
    
    # Create demo window
    demo_window = tk.Tk()
    demo_window.title("🗳️ Voting System Demo")
    demo_window.geometry("800x600")
    demo_window.configure(bg='#1a1a2e')
    
    # Header
    header_label = tk.Label(demo_window,
                           text="🗳️ IRIS-BASED VOTING SYSTEM DEMO",
                           font=('Segoe UI', 18, 'bold'),
                           fg='white', bg='#1a1a2e')
    header_label.pack(pady=20)
    
    # Description
    desc_label = tk.Label(demo_window,
                         text="This demo shows how the voting system works with iris authentication",
                         font=('Segoe UI', 12),
                         fg='#CCCCCC', bg='#1a1a2e')
    desc_label.pack(pady=(0, 20))
    
    # Demo buttons frame
    buttons_frame = tk.Frame(demo_window, bg='#1a1a2e')
    buttons_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
    
    # Demo 1: Show voting interface
    def demo_voting_interface():
        """Demo the voting interface"""
        messagebox.showinfo("Demo 1", 
                           "Demo 1: Voting Interface\n\n"
                           "This simulates a person (ID: 999) with 95% confidence\n"
                           "authenticating and voting.")
        show_voting_interface(person_id=999, confidence_score=0.95)
    
    demo1_btn = tk.Button(buttons_frame,
                         text="🗳️ Demo 1: Voting Interface",
                         command=demo_voting_interface,
                         font=('Segoe UI', 14, 'bold'),
                         fg='white', bg='#4CAF50',
                         relief='flat', padx=30, pady=15)
    demo1_btn.pack(fill=tk.X, pady=10)
    
    demo1_desc = tk.Label(buttons_frame,
                         text="Simulate a person authenticating and casting a vote",
                         font=('Segoe UI', 10),
                         fg='#CCCCCC', bg='#1a1a2e')
    demo1_desc.pack(pady=(0, 20))
    
    # Demo 2: Show results dashboard
    def demo_results_dashboard():
        """Demo the results dashboard"""
        messagebox.showinfo("Demo 2", 
                           "Demo 2: Results Dashboard\n\n"
                           "This shows the real-time voting results\n"
                           "with charts and statistics.")
        show_voting_results()
    
    demo2_btn = tk.Button(buttons_frame,
                         text="📊 Demo 2: Results Dashboard",
                         command=demo_results_dashboard,
                         font=('Segoe UI', 14, 'bold'),
                         fg='white', bg='#2196F3',
                         relief='flat', padx=30, pady=15)
    demo2_btn.pack(fill=tk.X, pady=10)
    
    demo2_desc = tk.Label(buttons_frame,
                         text="View comprehensive voting results and analytics",
                         font=('Segoe UI', 10),
                         fg='#CCCCCC', bg='#1a1a2e')
    demo2_desc.pack(pady=(0, 20))
    
    # Demo 3: Individual vote lookup
    def demo_vote_lookup():
        """Demo the vote lookup"""
        messagebox.showinfo("Demo 3", 
                           "Demo 3: Individual Vote Lookup\n\n"
                           "This allows checking if a specific person\n"
                           "has voted and what they voted for.")
        show_individual_vote_lookup()
    
    demo3_btn = tk.Button(buttons_frame,
                         text="🔍 Demo 3: Vote Lookup",
                         command=demo_vote_lookup,
                         font=('Segoe UI', 14, 'bold'),
                         fg='white', bg='#FF9800',
                         relief='flat', padx=30, pady=15)
    demo3_btn.pack(fill=tk.X, pady=10)
    
    demo3_desc = tk.Label(buttons_frame,
                         text="Look up individual voting records by person ID",
                         font=('Segoe UI', 10),
                         fg='#CCCCCC', bg='#1a1a2e')
    demo3_desc.pack(pady=(0, 20))
    
    # Demo 4: Create sample data
    def demo_create_sample_data():
        """Create sample voting data"""
        try:
            # Sample votes
            sample_votes = [
                (101, 1, 0.95), (102, 2, 0.88), (103, 1, 0.92), (104, 3, 0.85),
                (105, 2, 0.91), (106, 4, 0.87), (107, 1, 0.94), (108, 5, 0.89)
            ]
            
            parties = voting_system.get_parties()
            party_names = {p['id']: p['name'] for p in parties}
            
            votes_created = 0
            for person_id, party_id, confidence in sample_votes:
                if not voting_system.has_voted(person_id):
                    success = voting_system.cast_vote(person_id, party_id, confidence)
                    if success:
                        votes_created += 1
            
            messagebox.showinfo("Sample Data Created", 
                               "✅ Created {} sample votes!\n\n".format(votes_created)
                               f"You can now view results in Demo 2\n"
                               f"or lookup individual votes in Demo 3.")
        except Exception as e:
            messagebox.showerror("Error", "Failed to create sample data: {}".format(str(e)))
    
    demo4_btn = tk.Button(buttons_frame,
                         text="📝 Demo 4: Create Sample Data",
                         command=demo_create_sample_data,
                         font=('Segoe UI', 14, 'bold'),
                         fg='white', bg='#9C27B0',
                         relief='flat', padx=30, pady=15)
    demo4_btn.pack(fill=tk.X, pady=10)
    
    demo4_desc = tk.Label(buttons_frame,
                         text="Generate sample voting data for demonstration",
                         font=('Segoe UI', 10),
                         fg='#CCCCCC', bg='#1a1a2e')
    demo4_desc.pack(pady=(0, 20))
    
    # Current statistics
    def show_current_stats():
        """Show current voting statistics"""
        try:
            results = voting_system.get_voting_results()
            
            stats_text = f"📊 CURRENT STATISTICS:\n\n"
            stats_text += "Total Votes: {}\n".format(results['total_votes'])
            stats_text += "Total Voters: {}\n".format(results['total_voters'])
            stats_text += "Turnout: {}%\n\n".format((results['total_voters'] / 108) * 100:.1f)
            
            if results['total_votes'] > 0:
                stats_text += "🏆 TOP PARTIES:\n"
                for result in sorted(results['results'], key=lambda x: x['votes'], reverse=True)[:3]:
                    if result['votes'] > 0:
                        stats_text += "{} {result['party']}: {result['votes']} votes\n".format(result['symbol'])
            else:
                stats_text += "No votes cast yet. Use Demo 4 to create sample data."
            
            messagebox.showinfo("Current Statistics", stats_text)
        except Exception as e:
            messagebox.showerror("Error", "Failed to get statistics: {}".format(str(e)))
    
    stats_btn = tk.Button(buttons_frame,
                         text="📈 Current Statistics",
                         command=show_current_stats,
                         font=('Segoe UI', 12, 'bold'),
                         fg='white', bg='#607D8B',
                         relief='flat', padx=20, pady=10)
    stats_btn.pack(fill=tk.X, pady=10)
    
    # Instructions
    instructions_frame = tk.Frame(demo_window, bg='#2d2d44', relief='solid', bd=1)
    instructions_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
    
    instructions_label = tk.Label(instructions_frame,
                                 text="💡 DEMO INSTRUCTIONS:\n"
                                      "1. Start with Demo 4 to create sample voting data\n"
                                      "2. Try Demo 1 to see the voting interface\n"
                                      "3. Use Demo 2 to view comprehensive results\n"
                                      "4. Test Demo 3 to lookup individual votes",
                                 font=('Segoe UI', 10),
                                 fg='white', bg='#2d2d44',
                                 justify=tk.LEFT)
    instructions_label.pack(pady=15)
    
    # Close button
    close_btn = tk.Button(demo_window,
                         text="❌ Close Demo",
                         command=demo_window.destroy,
                         font=('Segoe UI', 12, 'bold'),
                         fg='white', bg='#f44336',
                         relief='flat', padx=20, pady=10)
    close_btn.pack(pady=20)
    
    # Show current stats on startup
    demo_window.after(1000, show_current_stats)
    
    demo_window.mainloop()

def quick_demo():
    """Quick command-line demo"""
    print("🗳️ QUICK VOTING SYSTEM DEMO")
    print("=" * 40)
    
    # Show current statistics
    results = voting_system.get_voting_results()
    print("📊 Current Statistics:")
    print("   Total Votes: {}".format(results['total_votes']))
    print("   Total Voters: {}".format(results['total_voters']))
    print("   Turnout: {:.1f}%".format((results['total_voters'] / 108) * 100))
    
    if results['total_votes'] > 0:
        print("\n🏆 Current Results:")
        for result in sorted(results['results'], key=lambda x: x['votes'], reverse=True):
            if result['votes'] > 0:
                print("   {} {}: {} votes ({:.1f}%)".format(result['symbol'], result['party'], result['votes'], result['percentage']))
    else:
        print("\n📝 No votes cast yet.")
        print("   Run create_sample_votes.py to add sample data")
    
    print("\n🎯 Available Parties:")
    parties = voting_system.get_parties()
    for party in parties:
        print("   {} {}".format(party['symbol'], party['name']))

    print("\n🚀 To use the full system:")
    print("   1. Run: python Main.py")
    print("   2. Click: 🗳️ VOTING SYSTEM")
    print("   3. Choose: CAST VOTE or VIEW RESULTS")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_demo()
    else:
        demo_voting_system()
