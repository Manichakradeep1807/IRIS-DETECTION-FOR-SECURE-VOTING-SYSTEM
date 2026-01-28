#!/usr/bin/env python3
"""
Settings Window for Iris Recognition System
Provides theme and language selection interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from theme_manager import theme_manager, get_current_colors
from language_manager import language_manager, get_text

class SettingsWindow:
    """Settings window for theme and language configuration"""
    
    def __init__(self, parent, on_settings_changed=None):
        self.parent = parent
        self.on_settings_changed = on_settings_changed
        self.window = None
        self.theme_var = tk.StringVar()
        self.language_var = tk.StringVar()
        
        # Set initial values
        self.theme_var.set(theme_manager.current_theme)
        self.language_var.set(language_manager.current_language)
    
    def show(self):
        """Show the settings window"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = tk.Toplevel(self.parent)
        self.window.title(get_text("settings_title", "System Settings"))
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # Get current theme colors
        colors = get_current_colors()
        self.window.configure(bg=colors['primary'])
        
        # Make window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the settings interface"""
        colors = get_current_colors()
        
        # Main container
        main_frame = tk.Frame(self.window, bg=colors['primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame,
                              text=f"⚙️ {get_text('settings_title', 'System Settings')}",
                              font=('Segoe UI', 18, 'bold'),
                              fg=colors['text_primary'],
                              bg=colors['primary'])
        title_label.pack(pady=(0, 30))
        
        # Theme Selection Section
        self._create_theme_section(main_frame, colors)
        
        # Language Selection Section
        self._create_language_section(main_frame, colors)
        
        # Preview Section
        self._create_preview_section(main_frame, colors)
        
        # Buttons Section
        self._create_buttons_section(main_frame, colors)
    
    def _create_theme_section(self, parent, colors):
        """Create theme selection section"""
        # Theme frame
        theme_frame = tk.LabelFrame(parent,
                                   text=f"🎨 {get_text('settings_theme', 'Theme Selection')}",
                                   font=('Segoe UI', 12, 'bold'),
                                   fg=colors['text_primary'],
                                   bg=colors['secondary'],
                                   relief='raised',
                                   bd=2)
        theme_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Theme options
        themes = theme_manager.get_available_themes()
        
        row = 0
        col = 0
        for theme_code, theme_name in themes.items():
            theme_radio = tk.Radiobutton(theme_frame,
                                        text=theme_name,
                                        variable=self.theme_var,
                                        value=theme_code,
                                        font=('Segoe UI', 10),
                                        fg=colors['text_primary'],
                                        bg=colors['secondary'],
                                        selectcolor=colors['accent_primary'],
                                        activebackground=colors['hover'],
                                        command=self._on_theme_preview)
            theme_radio.grid(row=row, column=col, sticky='w', padx=10, pady=5)
            
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
        
        # Configure grid weights
        theme_frame.grid_columnconfigure(0, weight=1)
        theme_frame.grid_columnconfigure(1, weight=1)
    
    def _create_language_section(self, parent, colors):
        """Create language selection section"""
        # Language frame
        language_frame = tk.LabelFrame(parent,
                                      text=f"🌐 {get_text('settings_language', 'Language Selection')}",
                                      font=('Segoe UI', 12, 'bold'),
                                      fg=colors['text_primary'],
                                      bg=colors['secondary'],
                                      relief='raised',
                                      bd=2)
        language_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Language options
        languages = language_manager.get_available_languages()
        
        row = 0
        for lang_code, lang_name in languages.items():
            lang_radio = tk.Radiobutton(language_frame,
                                       text=f"{lang_name} ({lang_code.upper()})",
                                       variable=self.language_var,
                                       value=lang_code,
                                       font=('Segoe UI', 10),
                                       fg=colors['text_primary'],
                                       bg=colors['secondary'],
                                       selectcolor=colors['accent_primary'],
                                       activebackground=colors['hover'],
                                       command=self._on_language_preview)
            lang_radio.grid(row=row, column=0, sticky='w', padx=10, pady=5)
            row += 1
        
        # Configure grid weights
        language_frame.grid_columnconfigure(0, weight=1)
    
    def _create_preview_section(self, parent, colors):
        """Create preview section"""
        # Preview frame
        preview_frame = tk.LabelFrame(parent,
                                     text="👁️ Preview",
                                     font=('Segoe UI', 12, 'bold'),
                                     fg=colors['text_primary'],
                                     bg=colors['secondary'],
                                     relief='raised',
                                     bd=2)
        preview_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Preview content
        self.preview_label = tk.Label(preview_frame,
                                     text=get_text('welcome_title', '🎯 WELCOME TO ADVANCED IRIS RECOGNITION'),
                                     font=('Segoe UI', 11),
                                     fg=colors['text_primary'],
                                     bg=colors['secondary'],
                                     wraplength=500)
        self.preview_label.pack(pady=10)
        
        # Sample buttons for theme preview
        button_frame = tk.Frame(preview_frame, bg=colors['secondary'])
        button_frame.pack(pady=10)
        
        self.preview_button1 = tk.Button(button_frame,
                                        text=get_text('live_recognition', '📹 LIVE RECOGNITION'),
                                        font=('Segoe UI', 9, 'bold'),
                                        fg='white',
                                        bg=colors['warning'],
                                        relief='flat',
                                        padx=15,
                                        pady=5)
        self.preview_button1.pack(side=tk.LEFT, padx=5)
        
        self.preview_button2 = tk.Button(button_frame,
                                        text=get_text('iris_gallery', '🖼️ IRIS GALLERY'),
                                        font=('Segoe UI', 9, 'bold'),
                                        fg='white',
                                        bg=colors['accent_secondary'],
                                        relief='flat',
                                        padx=15,
                                        pady=5)
        self.preview_button2.pack(side=tk.LEFT, padx=5)
    
    def _create_buttons_section(self, parent, colors):
        """Create action buttons section"""
        button_frame = tk.Frame(parent, bg=colors['primary'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Apply button
        apply_btn = tk.Button(button_frame,
                             text=f"✅ {get_text('settings_apply', 'Apply Changes')}",
                             font=('Segoe UI', 11, 'bold'),
                             fg='white',
                             bg=colors['success'],
                             relief='flat',
                             padx=20,
                             pady=10,
                             command=self._apply_settings)
        apply_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Reset button
        reset_btn = tk.Button(button_frame,
                             text=f"🔄 {get_text('settings_reset', 'Reset to Default')}",
                             font=('Segoe UI', 11, 'bold'),
                             fg='white',
                             bg=colors['warning'],
                             relief='flat',
                             padx=20,
                             pady=10,
                             command=self._reset_settings)
        reset_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = tk.Button(button_frame,
                              text=f"❌ {get_text('settings_cancel', 'Cancel')}",
                              font=('Segoe UI', 11, 'bold'),
                              fg='white',
                              bg=colors['danger'],
                              relief='flat',
                              padx=20,
                              pady=10,
                              command=self._cancel_settings)
        cancel_btn.pack(side=tk.RIGHT)
    
    def _on_theme_preview(self):
        """Preview theme changes"""
        # This would update the preview in real-time
        # For now, just update the preview section
        pass
    
    def _on_language_preview(self):
        """Preview language changes"""
        # This would update the preview text in real-time
        # For now, just update the preview section
        pass
    
    def _apply_settings(self):
        """Apply the selected settings"""
        try:
            # Apply theme
            old_theme = theme_manager.current_theme
            new_theme = self.theme_var.get()
            
            # Apply language
            old_language = language_manager.current_language
            new_language = self.language_var.get()
            
            # Set new settings
            theme_changed = theme_manager.set_theme(new_theme)
            language_changed = language_manager.set_language(new_language)
            
            if theme_changed or language_changed:
                messagebox.showinfo(
                    get_text('success', 'Success'),
                    f"{get_text('settings_apply', 'Settings applied successfully!')} "
                    f"Please restart the application to see all changes."
                )
                
                # Notify parent about changes
                if self.on_settings_changed:
                    self.on_settings_changed(theme_changed, language_changed)
                
                self.window.destroy()
            else:
                messagebox.showerror(
                    get_text('error', 'Error'),
                    "Failed to apply settings. Please try again."
                )
                
        except Exception as e:
            messagebox.showerror(
                get_text('error', 'Error'),
                f"Error applying settings: {str(e)}"
            )
    
    def _reset_settings(self):
        """Reset settings to default"""
        self.theme_var.set("dark")
        self.language_var.set("en")
        
        messagebox.showinfo(
            get_text('info', 'Information'),
            "Settings reset to default values. Click 'Apply Changes' to save."
        )
    
    def _cancel_settings(self):
        """Cancel settings changes"""
        self.window.destroy()

def show_settings_window(parent, on_settings_changed=None):
    """Convenience function to show settings window"""
    settings = SettingsWindow(parent, on_settings_changed)
    settings.show()
    return settings
