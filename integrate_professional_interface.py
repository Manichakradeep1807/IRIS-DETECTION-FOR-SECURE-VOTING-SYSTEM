#!/usr/bin/env python3
"""
Integration script to connect the professional interface with existing iris recognition system
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def integrate_professional_interface():
    """Integrate professional interface with existing system"""
    
    print("🔗 Integrating Professional Interface with Existing System")
    print("=" * 60)
    
    try:
        # Import existing system components
        print("1️⃣ Checking existing system components...")
        
        # Check for main system file
        if os.path.exists('Main_final_cleaned.py'):
            print("✅ Found Main_final_cleaned.py")
        else:
            print("❌ Main_final_cleaned.py not found")
            return False
        
        # Check for voting system
        if os.path.exists('voting_results.py'):
            print("✅ Found voting_results.py")
        else:
            print("❌ voting_results.py not found")
            return False
        
        # Check for professional interface
        if os.path.exists('professional_interface.py'):
            print("✅ Found professional_interface.py")
        else:
            print("❌ professional_interface.py not found")
            return False
        
        print("\n2️⃣ Creating integrated interface...")
        
        # Create integrated interface class
        create_integrated_interface()
        
        print("✅ Integration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration error: {e}")
        return False

def create_integrated_interface():
    """Create integrated interface that connects professional UI with existing functions"""
    
    integrated_code = '''#!/usr/bin/env python3
"""
Integrated Professional Iris Recognition Interface
Connects professional UI with existing system functionality
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Import professional interface
from professional_interface import ProfessionalIrisInterface

# Import existing system functions
try:
    from Main_final_cleaned import (
        show_iris_recognition, show_live_recognition, 
        show_voting_menu, show_iris_gallery, 
        toggle_voice_commands, show_settings_menu
    )
    MAIN_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Warning: Could not import main system functions: {e}")
    MAIN_SYSTEM_AVAILABLE = False

try:
    from voting_results import show_voting_results, show_individual_vote_lookup
    VOTING_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Warning: Could not import voting functions: {e}")
    VOTING_SYSTEM_AVAILABLE = False

class IntegratedProfessionalInterface(ProfessionalIrisInterface):
    """Professional interface integrated with existing system"""
    
    def __init__(self):
        super().__init__()
        self.setup_integration()
        
    def setup_integration(self):
        """Setup integration with existing system"""
        print("🔗 Setting up system integration...")
        
        # Update window title
        self.root.title("🔍 Integrated Iris Recognition System - Professional Edition")
        
        # Show integration status
        self.show_integration_status()
        
    def show_integration_status(self):
        """Show integration status in the interface"""
        # This could be added to the status area
        pass
        
    # Override button methods to connect with existing functions
    def start_recognition(self):
        """Start iris recognition using existing system"""
        try:
            if MAIN_SYSTEM_AVAILABLE:
                print("🔍 Starting integrated iris recognition...")
                show_iris_recognition()
            else:
                messagebox.showinfo(
                    "Recognition", 
                    "🔍 Iris Recognition\\n\\n"
                    "Professional interface ready!\\n"
                    "Connect to your existing recognition system here."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Recognition error: {e}")
            
    def start_live_recognition(self):
        """Start live recognition using existing system"""
        try:
            if MAIN_SYSTEM_AVAILABLE:
                print("📹 Starting integrated live recognition...")
                show_live_recognition()
            else:
                messagebox.showinfo(
                    "Live Recognition", 
                    "📹 Live Recognition\\n\\n"
                    "Professional interface ready!\\n"
                    "Connect to your existing live recognition system here."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Live recognition error: {e}")
            
    def open_voting_system(self):
        """Open voting system using existing system"""
        try:
            if MAIN_SYSTEM_AVAILABLE:
                print("🗳️ Opening integrated voting system...")
                show_voting_menu()
            else:
                messagebox.showinfo(
                    "Voting System", 
                    "🗳️ Voting System\\n\\n"
                    "Professional interface ready!\\n"
                    "Your secure voting system with password protection is available."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Voting system error: {e}")
            
    def open_gallery(self):
        """Open iris gallery using existing system"""
        try:
            if MAIN_SYSTEM_AVAILABLE:
                print("🖼️ Opening integrated iris gallery...")
                show_iris_gallery()
            else:
                messagebox.showinfo(
                    "Iris Gallery", 
                    "🖼️ Iris Gallery\\n\\n"
                    "Professional interface ready!\\n"
                    "Connect to your existing iris gallery system here."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Gallery error: {e}")
            
    def show_analytics(self):
        """Show analytics dashboard"""
        try:
            if VOTING_SYSTEM_AVAILABLE:
                print("📊 Opening integrated analytics...")
                show_voting_results()
            else:
                messagebox.showinfo(
                    "Analytics", 
                    "📊 Analytics Dashboard\\n\\n"
                    "Professional interface ready!\\n"
                    "System analytics and voting results available here."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Analytics error: {e}")
            
    def toggle_voice(self):
        """Toggle voice commands using existing system"""
        try:
            if MAIN_SYSTEM_AVAILABLE:
                print("🎤 Toggling integrated voice commands...")
                toggle_voice_commands()
            else:
                messagebox.showinfo(
                    "Voice Commands", 
                    "🎤 Voice Commands\\n\\n"
                    "Professional interface ready!\\n"
                    "Voice command system integration available."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Voice commands error: {e}")
            
    def open_settings(self):
        """Open settings using existing system"""
        try:
            if MAIN_SYSTEM_AVAILABLE:
                print("⚙️ Opening integrated settings...")
                show_settings_menu()
            else:
                messagebox.showinfo(
                    "Settings", 
                    "⚙️ System Settings\\n\\n"
                    "Professional interface ready!\\n"
                    "System configuration and preferences available."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Settings error: {e}")

def main():
    """Main function to run the integrated professional interface"""
    print("🚀 Starting Integrated Professional Iris Recognition Interface...")
    print(f"📋 Main system available: {MAIN_SYSTEM_AVAILABLE}")
    print(f"📋 Voting system available: {VOTING_SYSTEM_AVAILABLE}")
    
    try:
        app = IntegratedProfessionalInterface()
        app.run()
    except Exception as e:
        print(f"❌ Error starting integrated interface: {e}")
        messagebox.showerror("Error", f"Failed to start integrated interface: {e}")

if __name__ == "__main__":
    main()
'''
    
    # Write the integrated interface file
    with open('integrated_professional_interface.py', 'w', encoding='utf-8') as f:
        f.write(integrated_code)
    
    print("✅ Created integrated_professional_interface.py")

def main():
    """Main function"""
    print("🔗 Starting Professional Interface Integration...")
    
    success = integrate_professional_interface()
    
    if success:
        print("\n✅ Integration completed successfully!")
        print("\n🚀 You can now run:")
        print("   python integrated_professional_interface.py")
        print("\nThis will launch the professional interface connected to your existing system!")
        
        # Ask if user wants to launch the integrated interface
        try:
            choice = input("\nDo you want to launch the integrated interface now? (y/N): ").lower().strip()
            if choice == 'y' or choice == 'yes':
                print("\n🚀 Launching integrated professional interface...")
                import subprocess
                subprocess.run([sys.executable, 'integrated_professional_interface.py'])
        except KeyboardInterrupt:
            print("\n👋 Integration complete!")
    else:
        print("\n❌ Integration failed!")
        print("Please ensure all required files are present and try again.")

if __name__ == "__main__":
    main()
