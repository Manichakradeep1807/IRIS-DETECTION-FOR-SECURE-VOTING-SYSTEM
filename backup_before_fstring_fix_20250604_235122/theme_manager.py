#!/usr/bin/env python3
"""
Theme Manager for Iris Recognition System
Provides dark/light theme switching and customization
"""

import json
import os
from typing import Dict, Any

class ThemeManager:
    """Manages application themes and styling"""
    
    def __init__(self):
        self.current_theme = "dark"
        self.themes_file = "themes.json"
        self.user_preferences_file = "user_preferences.json"
        self.themes = self._load_default_themes()
        self.load_user_preferences()
    
    def _load_default_themes(self) -> Dict[str, Any]:
        """Load default theme configurations"""
        return {
            "dark": {
                "name": "Dark Professional",
                "colors": {
                    "primary": "#1a1a2e",
                    "secondary": "#16213e",
                    "accent_primary": "#0f3460",
                    "accent_secondary": "#533483",
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "danger": "#f44336",
                    "info": "#2196F3",
                    "text_primary": "#ffffff",
                    "text_secondary": "#cccccc",
                    "text_muted": "#888888",
                    "border": "#444444",
                    "hover": "#2d2d44",
                    "active": "#3d3d54"
                },
                "fonts": {
                    "primary": "Segoe UI",
                    "secondary": "Arial",
                    "monospace": "Consolas"
                },
                "sizes": {
                    "button_padding_x": 20,
                    "button_padding_y": 10,
                    "border_radius": 5,
                    "font_size_large": 16,
                    "font_size_medium": 12,
                    "font_size_small": 10
                }
            },
            "light": {
                "name": "Light Professional",
                "colors": {
                    "primary": "#ffffff",
                    "secondary": "#f5f5f5",
                    "accent_primary": "#2196F3",
                    "accent_secondary": "#9C27B0",
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "danger": "#f44336",
                    "info": "#00BCD4",
                    "text_primary": "#212121",
                    "text_secondary": "#424242",
                    "text_muted": "#757575",
                    "border": "#e0e0e0",
                    "hover": "#f0f0f0",
                    "active": "#e8e8e8"
                },
                "fonts": {
                    "primary": "Segoe UI",
                    "secondary": "Arial",
                    "monospace": "Consolas"
                },
                "sizes": {
                    "button_padding_x": 20,
                    "button_padding_y": 10,
                    "border_radius": 5,
                    "font_size_large": 16,
                    "font_size_medium": 12,
                    "font_size_small": 10
                }
            },
            "blue": {
                "name": "Ocean Blue",
                "colors": {
                    "primary": "#0d1421",
                    "secondary": "#1e2a3a",
                    "accent_primary": "#2980b9",
                    "accent_secondary": "#3498db",
                    "success": "#27ae60",
                    "warning": "#f39c12",
                    "danger": "#e74c3c",
                    "info": "#17a2b8",
                    "text_primary": "#ecf0f1",
                    "text_secondary": "#bdc3c7",
                    "text_muted": "#7f8c8d",
                    "border": "#34495e",
                    "hover": "#2c3e50",
                    "active": "#34495e"
                },
                "fonts": {
                    "primary": "Segoe UI",
                    "secondary": "Arial",
                    "monospace": "Consolas"
                },
                "sizes": {
                    "button_padding_x": 20,
                    "button_padding_y": 10,
                    "border_radius": 8,
                    "font_size_large": 16,
                    "font_size_medium": 12,
                    "font_size_small": 10
                }
            },
            "green": {
                "name": "Forest Green",
                "colors": {
                    "primary": "#1b2631",
                    "secondary": "#273746",
                    "accent_primary": "#27ae60",
                    "accent_secondary": "#2ecc71",
                    "success": "#58d68d",
                    "warning": "#f4d03f",
                    "danger": "#ec7063",
                    "info": "#5dade2",
                    "text_primary": "#f8f9fa",
                    "text_secondary": "#d5dbdb",
                    "text_muted": "#85929e",
                    "border": "#566573",
                    "hover": "#34495e",
                    "active": "#2c3e50"
                },
                "fonts": {
                    "primary": "Segoe UI",
                    "secondary": "Arial",
                    "monospace": "Consolas"
                },
                "sizes": {
                    "button_padding_x": 20,
                    "button_padding_y": 10,
                    "border_radius": 6,
                    "font_size_large": 16,
                    "font_size_medium": 12,
                    "font_size_small": 10
                }
            }
        }
    
    def get_current_theme(self) -> Dict[str, Any]:
        """Get the current active theme"""
        return self.themes.get(self.current_theme, self.themes["dark"])
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get colors for the current theme"""
        return self.get_current_theme()["colors"]
    
    def get_theme_fonts(self) -> Dict[str, str]:
        """Get fonts for the current theme"""
        return self.get_current_theme()["fonts"]
    
    def get_theme_sizes(self) -> Dict[str, int]:
        """Get sizes for the current theme"""
        return self.get_current_theme()["sizes"]
    
    def set_theme(self, theme_name: str) -> bool:
        """Set the active theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_user_preferences()
            return True
        return False
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes"""
        return {name: theme["name"] for name, theme in self.themes.items()}
    
    def save_user_preferences(self):
        """Save user preferences to file"""
        try:
            preferences = {
                "theme": self.current_theme,
                "custom_settings": {}
            }
            with open(self.user_preferences_file, 'w') as f:
                json.dump(preferences, f, indent=2)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def load_user_preferences(self):
        """Load user preferences from file"""
        try:
            if os.path.exists(self.user_preferences_file):
                with open(self.user_preferences_file, 'r') as f:
                    preferences = json.load(f)
                    self.current_theme = preferences.get("theme", "dark")
        except Exception as e:
            print(f"Error loading preferences: {e}")
            self.current_theme = "dark"
    
    def create_custom_theme(self, name: str, base_theme: str, modifications: Dict[str, Any]) -> bool:
        """Create a custom theme based on an existing theme"""
        if base_theme not in self.themes:
            return False
        
        # Copy base theme
        custom_theme = self.themes[base_theme].copy()
        custom_theme["name"] = name
        
        # Apply modifications
        for category, changes in modifications.items():
            if category in custom_theme:
                custom_theme[category].update(changes)
        
        self.themes[name] = custom_theme
        self.save_themes()
        return True
    
    def save_themes(self):
        """Save themes to file"""
        try:
            with open(self.themes_file, 'w') as f:
                json.dump(self.themes, f, indent=2)
        except Exception as e:
            print(f"Error saving themes: {e}")
    
    def load_themes(self):
        """Load themes from file"""
        try:
            if os.path.exists(self.themes_file):
                with open(self.themes_file, 'r') as f:
                    saved_themes = json.load(f)
                    self.themes.update(saved_themes)
        except Exception as e:
            print(f"Error loading themes: {e}")

# Global theme manager instance
theme_manager = ThemeManager()

def get_current_colors():
    """Convenience function to get current theme colors"""
    return theme_manager.get_theme_colors()

def get_current_fonts():
    """Convenience function to get current theme fonts"""
    return theme_manager.get_theme_fonts()

def get_current_sizes():
    """Convenience function to get current theme sizes"""
    return theme_manager.get_theme_sizes()

def switch_theme(theme_name: str):
    """Convenience function to switch themes"""
    return theme_manager.set_theme(theme_name)

def get_available_themes():
    """Convenience function to get available themes"""
    return theme_manager.get_available_themes()
