#!/usr/bin/env python3
"""
Voting Results Dashboard
Real-time voting results and analytics
"""

import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
import json
from voting_system import voting_system

def show_voting_results():
    """Show comprehensive voting results dashboard"""
    
    # Create results window
    results_window = tk.Toplevel()
    results_window.title("🗳️ Voting Results Dashboard")
    results_window.geometry("1200x800")
    results_window.configure(bg='#1a1a2e')
    
    # Get voting results
    results_data = voting_system.get_voting_results()
    
    # Header
    header_frame = tk.Frame(results_window, bg='#1a1a2e')
    header_frame.pack(fill=tk.X, padx=20, pady=20)
    
    title_label = tk.Label(header_frame,
                          text="🗳️ VOTING RESULTS DASHBOARD",
                          font=('Segoe UI', 20, 'bold'),
                          fg='white', bg='#1a1a2e')
    title_label.pack()
    
    # Summary stats
    stats_frame = tk.Frame(results_window, bg='#2d2d44', relief='solid', bd=1)
    stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    stats_container = tk.Frame(stats_frame, bg='#2d2d44')
    stats_container.pack(pady=15)
    
    # Total votes
    total_votes_label = tk.Label(stats_container,
                                text="📊 Total Votes: {}".format(results_data['total_votes']),
                                font=('Segoe UI', 14, 'bold'),
                                fg='#4CAF50', bg='#2d2d44')
    total_votes_label.pack(side=tk.LEFT, padx=20)

    # Total voters
    total_voters_label = tk.Label(stats_container,
                                 text="👥 Total Voters: {}".format(results_data['total_voters']),
                                 font=('Segoe UI', 14, 'bold'),
                                 fg='#2196F3', bg='#2d2d44')
    total_voters_label.pack(side=tk.LEFT, padx=20)

    # Turnout percentage (assuming 108 registered voters)
    turnout = (results_data['total_voters'] / 108) * 100 if results_data['total_voters'] > 0 else 0
    turnout_label = tk.Label(stats_container,
                            text="📈 Turnout: {:.1f}%".format(turnout),
                            font=('Segoe UI', 14, 'bold'),
                            fg='#FF9800', bg='#2d2d44')
    turnout_label.pack(side=tk.LEFT, padx=20)

    # Last updated
    updated_label = tk.Label(stats_container,
                            text="🕒 Updated: {}".format(datetime.now().strftime('%H:%M:%S')),
                            font=('Segoe UI', 12),
                            fg='#CCCCCC', bg='#2d2d44')
    updated_label.pack(side=tk.RIGHT, padx=20)
    
    # Main content frame
    content_frame = tk.Frame(results_window, bg='#1a1a2e')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    # Left side - Results table
    left_frame = tk.Frame(content_frame, bg='#1a1a2e')
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    # Results table
    table_label = tk.Label(left_frame,
                          text="📋 DETAILED RESULTS",
                          font=('Segoe UI', 16, 'bold'),
                          fg='white', bg='#1a1a2e')
    table_label.pack(pady=(0, 10))
    
    # Create table frame
    table_frame = tk.Frame(left_frame, bg='#2d2d44', relief='solid', bd=1)
    table_frame.pack(fill=tk.BOTH, expand=True)
    
    # Table headers
    headers_frame = tk.Frame(table_frame, bg='#3d3d54')
    headers_frame.pack(fill=tk.X, padx=2, pady=2)
    
    tk.Label(headers_frame, text="Party", font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#3d3d54', width=20).pack(side=tk.LEFT, padx=5, pady=8)
    tk.Label(headers_frame, text="Votes", font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#3d3d54', width=10).pack(side=tk.LEFT, padx=5, pady=8)
    tk.Label(headers_frame, text="Percentage", font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#3d3d54', width=12).pack(side=tk.LEFT, padx=5, pady=8)
    tk.Label(headers_frame, text="Bar", font=('Segoe UI', 12, 'bold'),
             fg='white', bg='#3d3d54', width=20).pack(side=tk.LEFT, padx=5, pady=8)
    
    # Scrollable results
    results_canvas = tk.Canvas(table_frame, bg='#2d2d44', highlightthickness=0)
    results_scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=results_canvas.yview)
    results_scrollable = tk.Frame(results_canvas, bg='#2d2d44')
    
    results_scrollable.bind(
        "<Configure>",
        lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
    )
    
    results_canvas.create_window((0, 0), window=results_scrollable, anchor="nw")
    results_canvas.configure(yscrollcommand=results_scrollbar.set)
    
    results_canvas.pack(side="left", fill="both", expand=True)
    results_scrollbar.pack(side="right", fill="y")
    
    # Add results rows
    for i, result in enumerate(results_data['results']):
        row_bg = '#2d2d44' if i % 2 == 0 else '#3d3d54'
        
        row_frame = tk.Frame(results_scrollable, bg=row_bg)
        row_frame.pack(fill=tk.X, padx=2, pady=1)
        
        # Party name with symbol
        party_label = tk.Label(row_frame,
                              text="{} {}".format(result['symbol'], result['party']),
                              font=('Segoe UI', 11),
                              fg='white', bg=row_bg, width=20, anchor='w')
        party_label.pack(side=tk.LEFT, padx=5, pady=5)

        # Vote count
        votes_label = tk.Label(row_frame,
                              text=str(result['votes']),
                              font=('Segoe UI', 11, 'bold'),
                              fg='#4CAF50', bg=row_bg, width=10)
        votes_label.pack(side=tk.LEFT, padx=5, pady=5)

        # Percentage
        percentage_label = tk.Label(row_frame,
                                   text="{:.1f}%".format(result['percentage']),
                                   font=('Segoe UI', 11),
                                   fg='#2196F3', bg=row_bg, width=12)
        percentage_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Progress bar
        bar_frame = tk.Frame(row_frame, bg=row_bg, width=200, height=20)
        bar_frame.pack(side=tk.LEFT, padx=5, pady=5)
        bar_frame.pack_propagate(False)
        
        if results_data['total_votes'] > 0:
            bar_width = int((result['percentage'] / 100) * 180)
            if bar_width > 0:
                bar_canvas = tk.Canvas(bar_frame, bg=row_bg, highlightthickness=0, width=200, height=20)
                bar_canvas.pack()
                bar_canvas.create_rectangle(0, 2, bar_width, 18, fill=result['color'], outline="")
                bar_canvas.create_text(90, 10, text="{:.1f}%".format(result['percentage']),
                                     fill='white', font=('Segoe UI', 8, 'bold'))
    
    # Right side - Chart
    right_frame = tk.Frame(content_frame, bg='#1a1a2e')
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    chart_label = tk.Label(right_frame,
                          text="📊 VISUAL RESULTS",
                          font=('Segoe UI', 16, 'bold'),
                          fg='white', bg='#1a1a2e')
    chart_label.pack(pady=(0, 10))
    
    # Create chart
    if results_data['total_votes'] > 0:
        # Prepare data for chart
        parties = [r['party'] for r in results_data['results'] if r['votes'] > 0]
        votes = [r['votes'] for r in results_data['results'] if r['votes'] > 0]
        colors = [r['color'] for r in results_data['results'] if r['votes'] > 0]
        
        if parties:  # Only create chart if there are votes
            # Create matplotlib figure
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
            fig.patch.set_facecolor('#1a1a2e')
            
            # Pie chart
            ax1.pie(votes, labels=parties, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Vote Distribution', color='white', fontsize=14, fontweight='bold')
            ax1.set_facecolor('#1a1a2e')
            
            # Bar chart
            bars = ax2.bar(parties, votes, color=colors)
            ax2.set_title('Vote Counts', color='white', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Political Parties', color='white')
            ax2.set_ylabel('Number of Votes', color='white')
            ax2.set_facecolor('#1a1a2e')
            ax2.tick_params(colors='white')
            
            # Rotate x-axis labels for better readability
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', color='white')
            
            plt.tight_layout()
            
            # Embed chart in tkinter
            chart_canvas = FigureCanvasTkAgg(fig, right_frame)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            # No votes yet
            no_votes_label = tk.Label(right_frame,
                                     text="📊 No votes cast yet\n\nStart voting to see results!",
                                     font=('Segoe UI', 14),
                                     fg='#888888', bg='#1a1a2e',
                                     justify=tk.CENTER)
            no_votes_label.pack(expand=True)
    else:
        # No votes yet
        no_votes_label = tk.Label(right_frame,
                                 text="📊 No votes cast yet\n\nStart voting to see results!",
                                 font=('Segoe UI', 14),
                                 fg='#888888', bg='#1a1a2e',
                                 justify=tk.CENTER)
        no_votes_label.pack(expand=True)
    
    # Bottom buttons
    buttons_frame = tk.Frame(results_window, bg='#1a1a2e')
    buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    # Refresh button
    def refresh_results():
        results_window.destroy()
        show_voting_results()
    
    refresh_btn = tk.Button(buttons_frame,
                           text="🔄 Refresh Results",
                           command=refresh_results,
                           font=('Segoe UI', 12, 'bold'),
                           fg='white', bg='#4CAF50',
                           relief='flat', padx=20, pady=10)
    refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    # Export results button
    def export_results():
        try:
            filename = voting_system.export_results()
            messagebox.showinfo("Export Successful",
                              "Results exported to: {}".format(filename))
        except Exception as e:
            messagebox.showerror("Export Error", "Failed to export results: {}".format(str(e)))
    
    export_btn = tk.Button(buttons_frame,
                          text="📄 Export Results",
                          command=export_results,
                          font=('Segoe UI', 12, 'bold'),
                          fg='white', bg='#2196F3',
                          relief='flat', padx=20, pady=10)
    export_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    # Close button
    close_btn = tk.Button(buttons_frame,
                         text="❌ Close",
                         command=results_window.destroy,
                         font=('Segoe UI', 12, 'bold'),
                         fg='white', bg='#f44336',
                         relief='flat', padx=20, pady=10)
    close_btn.pack(side=tk.RIGHT)

def show_individual_vote_lookup():
    """Show interface to lookup individual votes"""
    
    lookup_window = tk.Toplevel()
    lookup_window.title("🔍 Individual Vote Lookup")
    lookup_window.geometry("500x400")
    lookup_window.configure(bg='#1a1a2e')
    
    # Header
    header_label = tk.Label(lookup_window,
                           text="🔍 INDIVIDUAL VOTE LOOKUP",
                           font=('Segoe UI', 16, 'bold'),
                           fg='white', bg='#1a1a2e')
    header_label.pack(pady=20)
    
    # Input frame
    input_frame = tk.Frame(lookup_window, bg='#2d2d44', relief='solid', bd=1)
    input_frame.pack(fill=tk.X, padx=20, pady=20)
    
    tk.Label(input_frame,
             text="Enter Person ID:",
             font=('Segoe UI', 12),
             fg='white', bg='#2d2d44').pack(pady=(15, 5))
    
    person_id_entry = tk.Entry(input_frame,
                              font=('Segoe UI', 12),
                              width=20,
                              justify='center')
    person_id_entry.pack(pady=(0, 15))
    
    # Results frame
    results_frame = tk.Frame(lookup_window, bg='#1a1a2e')
    results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    def lookup_vote():
        try:
            person_id = int(person_id_entry.get())
            vote_info = voting_system.get_vote_by_person(person_id)
            
            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            if vote_info:
                # Show vote information
                info_frame = tk.Frame(results_frame, bg='#2d2d44', relief='solid', bd=1)
                info_frame.pack(fill=tk.X, pady=10)
                
                tk.Label(info_frame,
                         text="✅ Vote Found for Person {}".format(person_id),
                         font=('Segoe UI', 14, 'bold'),
                         fg='#4CAF50', bg='#2d2d44').pack(pady=10)

                tk.Label(info_frame,
                         text="Party: {} {}".format(vote_info['symbol'], vote_info['party']),
                         font=('Segoe UI', 12),
                         fg='white', bg='#2d2d44').pack(pady=2)

                tk.Label(info_frame,
                         text="Time: {}".format(vote_info['timestamp']),
                         font=('Segoe UI', 12),
                         fg='white', bg='#2d2d44').pack(pady=2)

                tk.Label(info_frame,
                         text="Confidence: {:.1%}".format(vote_info['confidence']),
                         font=('Segoe UI', 12),
                         fg='white', bg='#2d2d44').pack(pady=(2, 10))
            else:
                # No vote found
                tk.Label(results_frame,
                         text="❌ No vote found for Person {}".format(person_id),
                         font=('Segoe UI', 14),
                         fg='#f44336', bg='#1a1a2e').pack(pady=20)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid Person ID (number)")
        except Exception as e:
            messagebox.showerror("Lookup Error", "Error looking up vote: {}".format(str(e)))
    
    # Lookup button
    lookup_btn = tk.Button(input_frame,
                          text="🔍 Lookup Vote",
                          command=lookup_vote,
                          font=('Segoe UI', 12, 'bold'),
                          fg='white', bg='#2196F3',
                          relief='flat', padx=20, pady=8)
    lookup_btn.pack(pady=(0, 15))
    
    # Close button
    close_btn = tk.Button(lookup_window,
                         text="❌ Close",
                         command=lookup_window.destroy,
                         font=('Segoe UI', 12, 'bold'),
                         fg='white', bg='#f44336',
                         relief='flat', padx=20, pady=10)
    close_btn.pack(pady=20)

if __name__ == "__main__":
    # Test the results dashboard
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    show_voting_results()
    
    root.mainloop()
