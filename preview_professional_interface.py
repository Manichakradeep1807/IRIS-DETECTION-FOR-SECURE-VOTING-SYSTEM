#!/usr/bin/env python3
"""
Preview launcher for the professional iris recognition interface
Shows the interface with demo functionality
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import subprocess

def show_interface_preview():
    """Show a preview of the professional interface"""
    
    print("🎨 Professional Iris Recognition Interface Preview")
    print("=" * 50)
    
    # Create preview window
    preview_window = tk.Tk()
    preview_window.title("🎨 Interface Preview - Professional Iris Recognition")
    preview_window.geometry("800x600")
    preview_window.configure(bg='#1a1a2e')
    
    # Center window
    preview_window.update_idletasks()
    x = (preview_window.winfo_screenwidth() // 2) - (800 // 2)
    y = (preview_window.winfo_screenheight() // 2) - (600 // 2)
    preview_window.geometry(f"800x600+{x}+{y}")
    
    # Header
    header_frame = tk.Frame(preview_window, bg='#16213e', height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text="🎨 Professional Interface Preview",
        font=('Segoe UI', 20, 'bold'),
        fg='white',
        bg='#16213e'
    )
    title_label.pack(expand=True)
    
    # Main content
    content_frame = tk.Frame(preview_window, bg='#1a1a2e')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Interface features
    features_label = tk.Label(
        content_frame,
        text="✨ Professional Interface Features",
        font=('Segoe UI', 16, 'bold'),
        fg='white',
        bg='#1a1a2e'
    )
    features_label.pack(pady=(0, 20))
    
    # Features list
    features_text = """
🎨 Modern Dark Theme Design
   • Professional navy blue color scheme
   • Gradient backgrounds and smooth transitions
   • Modern typography with Segoe UI fonts

🖱️ Interactive Elements
   • Hover effects on all buttons
   • Smooth color transitions
   • Professional button styling with rounded corners

📊 Dashboard Layout
   • Left navigation panel with control buttons
   • Main workspace area for content
   • Real-time status indicators
   • System statistics display

🔍 Advanced Features
   • Welcome screen with feature highlights
   • Status cards showing system metrics
   • Professional header with branding
   • Footer with system information

🎯 User Experience
   • Intuitive navigation structure
   • Clear visual hierarchy
   • Responsive design elements
   • Professional appearance
    """
    
    features_display = tk.Label(
        content_frame,
        text=features_text.strip(),
        font=('Segoe UI', 11),
        fg='#b0bec5',
        bg='#1a1a2e',
        justify=tk.LEFT
    )
    features_display.pack(pady=10)
    
    # Buttons frame
    buttons_frame = tk.Frame(content_frame, bg='#1a1a2e')
    buttons_frame.pack(pady=30)
    
    # Launch interface button
    def launch_interface():
        try:
            print("🚀 Launching professional interface...")
            preview_window.destroy()
            
            # Import and run the professional interface
            from professional_interface import ProfessionalIrisInterface
            app = ProfessionalIrisInterface()
            app.run()
            
        except ImportError as e:
            messagebox.showerror("Error", f"Could not import interface: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error launching interface: {e}")
    
    launch_btn = tk.Button(
        buttons_frame,
        text="🚀 Launch Professional Interface",
        command=launch_interface,
        font=('Segoe UI', 14, 'bold'),
        fg='white',
        bg='#00d4aa',
        activebackground='#26c6da',
        relief='flat',
        padx=30,
        pady=15,
        cursor='hand2'
    )
    launch_btn.pack(side=tk.LEFT, padx=10)
    
    # View code button
    def view_code():
        try:
            if os.path.exists('professional_interface.py'):
                if sys.platform.startswith('win'):
                    os.startfile('professional_interface.py')
                else:
                    subprocess.call(['open', 'professional_interface.py'])
            else:
                messagebox.showwarning("File Not Found", "professional_interface.py not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    
    code_btn = tk.Button(
        buttons_frame,
        text="📝 View Source Code",
        command=view_code,
        font=('Segoe UI', 14, 'bold'),
        fg='white',
        bg='#42a5f5',
        activebackground='#5dade5',
        relief='flat',
        padx=30,
        pady=15,
        cursor='hand2'
    )
    code_btn.pack(side=tk.LEFT, padx=10)
    
    # Close button
    close_btn = tk.Button(
        buttons_frame,
        text="❌ Close Preview",
        command=preview_window.destroy,
        font=('Segoe UI', 14, 'bold'),
        fg='white',
        bg='#ef5350',
        activebackground='#f44336',
        relief='flat',
        padx=30,
        pady=15,
        cursor='hand2'
    )
    close_btn.pack(side=tk.LEFT, padx=10)
    
    # Technical specs
    specs_frame = tk.Frame(content_frame, bg='#2d2d44', relief='solid', bd=1)
    specs_frame.pack(fill=tk.X, pady=20)
    
    specs_title = tk.Label(
        specs_frame,
        text="🔧 Technical Specifications",
        font=('Segoe UI', 12, 'bold'),
        fg='white',
        bg='#2d2d44'
    )
    specs_title.pack(pady=(10, 5))
    
    specs_text = """
• Window Size: 1400x900 (resizable, minimum 1200x800)
• Color Scheme: Professional dark theme with navy blue accents
• Typography: Segoe UI font family with multiple weights
• Layout: Responsive design with left navigation and main workspace
• Compatibility: Cross-platform (Windows, macOS, Linux)
• Dependencies: tkinter, PIL (Pillow) for enhanced graphics
    """
    
    specs_display = tk.Label(
        specs_frame,
        text=specs_text.strip(),
        font=('Segoe UI', 10),
        fg='#b0bec5',
        bg='#2d2d44',
        justify=tk.LEFT
    )
    specs_display.pack(pady=(5, 10))
    
    print("✅ Preview window created successfully")
    print("Click 'Launch Professional Interface' to see the full interface")
    
    # Start preview window
    preview_window.mainloop()

def main():
    """Main function"""
    print("🎨 Starting Interface Preview...")
    
    try:
        show_interface_preview()
    except Exception as e:
        print(f"❌ Error: {e}")
        messagebox.showerror("Error", f"Preview error: {e}")

if __name__ == "__main__":
    main()
