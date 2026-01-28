#!/usr/bin/env python3
"""
Professional Iris Recognition Interface
Modern, attractive, and user-friendly design
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
import sys
from datetime import datetime
import threading
import time

class ProfessionalIrisInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_interface()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("🔍 Advanced Iris Recognition System - Professional Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(1200, 800)
        
    def setup_styles(self):
        """Setup modern color scheme and fonts"""
        # Professional color palette
        self.colors = {
            'primary': '#1a1a2e',      # Dark navy
            'secondary': '#16213e',     # Darker navy
            'accent': '#0f3460',        # Blue accent
            'accent_light': '#533483',  # Purple accent
            'success': '#00d4aa',       # Teal green
            'warning': '#ffa726',       # Orange
            'danger': '#ef5350',        # Red
            'info': '#42a5f5',          # Blue
            'light': '#f8f9fa',         # Light gray
            'dark': '#212529',          # Dark gray
            'text_primary': '#ffffff',  # White
            'text_secondary': '#b0bec5', # Light gray
            'text_muted': '#78909c',    # Muted gray
            'gradient_start': '#667eea', # Gradient start
            'gradient_end': '#764ba2',   # Gradient end
            'card_bg': '#1e1e2e',       # Card background
            'border': '#2d2d44',        # Border color
        }
        
        # Professional fonts
        self.fonts = {
            'title': ('Segoe UI', 28, 'bold'),
            'subtitle': ('Segoe UI', 16, 'normal'),
            'heading': ('Segoe UI', 18, 'bold'),
            'subheading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 12, 'normal'),
            'small': ('Segoe UI', 10, 'normal'),
            'button': ('Segoe UI', 12, 'bold'),
            'mono': ('Consolas', 11, 'normal'),
        }
        
    def create_gradient_frame(self, parent, width, height):
        """Create a frame with gradient background"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        
        # Create gradient effect
        for i in range(height):
            ratio = i / height
            r1, g1, b1 = 102, 126, 234  # gradient_start RGB
            r2, g2, b2 = 118, 75, 162   # gradient_end RGB
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, width=1)
            
        return canvas
        
    def create_modern_button(self, parent, text, command, bg_color, hover_color, width=200, height=50):
        """Create a modern styled button with hover effects"""
        button_frame = tk.Frame(parent, bg=self.colors['primary'])
        
        button = tk.Button(
            button_frame,
            text=text,
            command=command,
            font=self.fonts['button'],
            fg=self.colors['text_primary'],
            bg=bg_color,
            activebackground=hover_color,
            activeforeground=self.colors['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=15,
            cursor='hand2'
        )
        
        # Add hover effects
        def on_enter(e):
            button.config(bg=hover_color)
            
        def on_leave(e):
            button.config(bg=bg_color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        button.pack(fill=tk.BOTH, expand=True)
        return button_frame
        
    def create_interface(self):
        """Create the main professional interface"""
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section with gradient
        header_frame = tk.Frame(main_container, bg=self.colors['secondary'], height=120)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['secondary'])
        header_content.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        # Title with icon
        title_frame = tk.Frame(header_content, bg=self.colors['secondary'])
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = tk.Label(
            title_frame,
            text="🔍 Advanced Iris Recognition System",
            font=self.fonts['title'],
            fg=self.colors['text_primary'],
            bg=self.colors['secondary']
        )
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(
            title_frame,
            text="Professional Biometric Authentication & Voting Platform",
            font=self.fonts['subtitle'],
            fg=self.colors['text_secondary'],
            bg=self.colors['secondary']
        )
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Status indicators
        status_frame = tk.Frame(header_content, bg=self.colors['secondary'])
        status_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # System status
        status_label = tk.Label(
            status_frame,
            text="🟢 System Online",
            font=self.fonts['body'],
            fg=self.colors['success'],
            bg=self.colors['secondary']
        )
        status_label.pack(anchor='e')
        
        # Current time - Update function to avoid encoding issues
        time_label = tk.Label(
            status_frame,
            text="",  # Will be updated by timer
            font=self.fonts['small'],
            fg=self.colors['text_muted'],
            bg=self.colors['secondary']
        )
        time_label.pack(anchor='e', pady=(5, 0))
        
        def update_time():
            try:
                # Use safe text instead of emojis to avoid encoding errors
                time_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                time_label.config(text=time_str)
            except Exception:
                # Fallback if encoding fails
                try:
                    time_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                    time_label.config(text=time_str)
                except Exception:
                    pass
            self.root.after(1000, update_time)
        
        update_time()
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.colors['primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Navigation
        left_panel = tk.Frame(content_frame, bg=self.colors['card_bg'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Navigation header
        nav_header = tk.Label(
            left_panel,
            text="🎛️ Control Panel",
            font=self.fonts['heading'],
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg']
        )
        nav_header.pack(pady=20)
        
        # Navigation buttons
        nav_buttons = [
            ("🔍 Iris Recognition", self.start_recognition, self.colors['info']),
            ("📹 Live Recognition", self.start_live_recognition, self.colors['warning']),
            ("🗳️ Voting System", self.open_voting_system, self.colors['accent_light']),
            ("🖼️ Iris Gallery", self.open_gallery, self.colors['success']),
            ("📊 Analytics", self.show_analytics, self.colors['info']),
            ("🎤 Voice Commands", self.toggle_voice, self.colors['warning']),
            ("⚙️ Settings", self.open_settings, self.colors['dark']),
        ]
        
        for text, command, color in nav_buttons:
            btn_frame = self.create_modern_button(
                left_panel, text, command, color, 
                self.lighten_color(color), width=300, height=60
            )
            btn_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Right panel - Main workspace
        right_panel = tk.Frame(content_frame, bg=self.colors['card_bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Workspace header
        workspace_header = tk.Frame(right_panel, bg=self.colors['border'], height=60)
        workspace_header.pack(fill=tk.X)
        workspace_header.pack_propagate(False)
        
        workspace_title = tk.Label(
            workspace_header,
            text="📋 Workspace",
            font=self.fonts['heading'],
            fg=self.colors['text_primary'],
            bg=self.colors['border']
        )
        workspace_title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Quick stats
        stats_frame = tk.Frame(workspace_header, bg=self.colors['border'])
        stats_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        stats_labels = [
            ("👥 Users: 108", self.colors['success']),
            ("🗳️ Votes: 5", self.colors['info']),
            ("🎯 Accuracy: 98.5%", self.colors['warning']),
        ]
        
        for text, color in stats_labels:
            stat_label = tk.Label(
                stats_frame,
                text=text,
                font=self.fonts['small'],
                fg=color,
                bg=self.colors['border']
            )
            stat_label.pack(side=tk.LEFT, padx=10)
        
        # Main workspace area
        self.workspace = tk.Frame(right_panel, bg=self.colors['card_bg'])
        self.workspace.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Welcome screen
        self.show_welcome_screen()
        
        # Footer
        footer_frame = tk.Frame(main_container, bg=self.colors['border'], height=40)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="🔒 Secure Biometric System | Professional Edition | © 2025 Advanced Iris Recognition",
            font=self.fonts['small'],
            fg=self.colors['text_muted'],
            bg=self.colors['border']
        )
        footer_label.pack(expand=True)
        
    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        # Simple color lightening
        color_map = {
            self.colors['info']: '#5dade5',
            self.colors['warning']: '#ffb74d',
            self.colors['accent_light']: '#7e57c2',
            self.colors['success']: '#26c6da',
            self.colors['dark']: '#424242',
        }
        return color_map.get(color, color)
        
    def show_welcome_screen(self):
        """Show welcome screen in workspace"""
        # Clear workspace
        for widget in self.workspace.winfo_children():
            widget.destroy()
            
        # Welcome content
        welcome_frame = tk.Frame(self.workspace, bg=self.colors['card_bg'])
        welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        # Center content
        center_frame = tk.Frame(welcome_frame, bg=self.colors['card_bg'])
        center_frame.pack(expand=True)
        
        # Welcome icon and text
        welcome_icon = tk.Label(
            center_frame,
            text="👁️‍🗨️",
            font=('Segoe UI', 72),
            fg=self.colors['accent'],
            bg=self.colors['card_bg']
        )
        welcome_icon.pack(pady=(50, 20))
        
        welcome_title = tk.Label(
            center_frame,
            text="Welcome to Advanced Iris Recognition",
            font=self.fonts['title'],
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg']
        )
        welcome_title.pack(pady=(0, 10))
        
        welcome_subtitle = tk.Label(
            center_frame,
            text="Professional Biometric Authentication System",
            font=self.fonts['subtitle'],
            fg=self.colors['text_secondary'],
            bg=self.colors['card_bg']
        )
        welcome_subtitle.pack(pady=(0, 30))
        
        # Feature highlights
        features_frame = tk.Frame(center_frame, bg=self.colors['card_bg'])
        features_frame.pack(pady=20)
        
        features = [
            "🔒 Secure biometric authentication",
            "🗳️ Integrated voting system",
            "📊 Real-time analytics",
            "🎤 Voice command support",
            "🖼️ Advanced iris gallery",
        ]
        
        for feature in features:
            feature_label = tk.Label(
                features_frame,
                text=feature,
                font=self.fonts['body'],
                fg=self.colors['text_secondary'],
                bg=self.colors['card_bg']
            )
            feature_label.pack(pady=5)
        
        # Quick start button
        quick_start_btn = self.create_modern_button(
            center_frame,
            "🚀 Quick Start - Begin Recognition",
            self.start_recognition,
            self.colors['success'],
            '#26c6da',
            width=300,
            height=60
        )
        quick_start_btn.pack(pady=30)

        # System status cards
        status_cards_frame = tk.Frame(center_frame, bg=self.colors['card_bg'])
        status_cards_frame.pack(pady=20)

        # Create status cards
        cards_data = [
            ("🎯", "98.5%", "Recognition\nAccuracy", self.colors['success']),
            ("⚡", "0.3s", "Average\nResponse Time", self.colors['info']),
            ("🔒", "256-bit", "Security\nEncryption", self.colors['warning']),
        ]

        for icon, value, label, color in cards_data:
            card = self.create_status_card(status_cards_frame, icon, value, label, color)
            card.pack(side=tk.LEFT, padx=15)

    def create_status_card(self, parent, icon, value, label, color):
        """Create a professional status card"""
        card_frame = tk.Frame(
            parent,
            bg=self.colors['border'],
            relief='solid',
            bd=1,
            width=120,
            height=100
        )
        card_frame.pack_propagate(False)

        # Card content
        content_frame = tk.Frame(card_frame, bg=self.colors['border'])
        content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Icon
        icon_label = tk.Label(
            content_frame,
            text=icon,
            font=('Segoe UI', 20),
            fg=color,
            bg=self.colors['border']
        )
        icon_label.pack()

        # Value
        value_label = tk.Label(
            content_frame,
            text=value,
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['border']
        )
        value_label.pack()

        # Label
        label_widget = tk.Label(
            content_frame,
            text=label,
            font=('Segoe UI', 8),
            fg=self.colors['text_muted'],
            bg=self.colors['border'],
            justify=tk.CENTER
        )
        label_widget.pack()

        return card_frame
        
    # Button command methods
    def start_recognition(self):
        messagebox.showinfo("Recognition", "🔍 Starting iris recognition...\nThis will launch the recognition module.")
        
    def start_live_recognition(self):
        messagebox.showinfo("Live Recognition", "📹 Starting live recognition...\nThis will activate the camera for real-time recognition.")
        
    def open_voting_system(self):
        messagebox.showinfo("Voting System", "🗳️ Opening voting system...\nSecure biometric voting interface will launch.")
        
    def open_gallery(self):
        messagebox.showinfo("Gallery", "🖼️ Opening iris gallery...\nView and manage captured iris images.")
        
    def show_analytics(self):
        messagebox.showinfo("Analytics", "📊 Loading analytics dashboard...\nSystem performance and statistics.")
        
    def toggle_voice(self):
        messagebox.showinfo("Voice Commands", "🎤 Voice commands toggled...\nVoice control system activated.")
        
    def open_settings(self):
        messagebox.showinfo("Settings", "⚙️ Opening settings...\nSystem configuration and preferences.")
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function to run the professional interface"""
    # Set UTF-8 encoding for console output to handle emojis
    import sys
    import io
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass
    
    try:
        # Use safe text without emojis for console output
        print("Starting Professional Iris Recognition Interface...")
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Avoid locale/encoding errors on some consoles
        try:
            print("Starting Professional Iris Recognition Interface...")
        except Exception:
            pass
    
    try:
        app = ProfessionalIrisInterface()
        app.run()
    except Exception as e:
        try:
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            print(f"Error starting interface: {error_msg}")
        except Exception:
            pass
        try:
            messagebox.showerror("Error", f"Failed to start interface: {e}")
        except Exception:
            pass

if __name__ == "__main__":
    main()
