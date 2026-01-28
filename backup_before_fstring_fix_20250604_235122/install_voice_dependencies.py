#!/usr/bin/env python3
"""
Install Voice Recognition Dependencies
Installs SpeechRecognition and pyaudio for voice commands
"""

import subprocess
import sys
import os

def install_package(package_name):
    """Install a Python package using pip"""
    try:
        print(f"📦 Installing {package_name}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package_name], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {package_name} installed successfully")
            return True
        else:
            print(f"❌ Failed to install {package_name}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing {package_name}: {e}")
        return False

def check_package(package_name):
    """Check if a package is already installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def main():
    """Install voice recognition dependencies"""
    print("🎤 VOICE RECOGNITION DEPENDENCIES INSTALLER")
    print("=" * 60)
    print("This script will install the required packages for voice commands:")
    print("• SpeechRecognition - For speech-to-text conversion")
    print("• pyaudio - For microphone access")
    print("=" * 60)
    
    # Check current status
    packages = {
        'speech_recognition': 'SpeechRecognition',
        'pyaudio': 'pyaudio'
    }
    
    print("\n🔍 Checking current installation status...")
    
    needs_installation = []
    for import_name, package_name in packages.items():
        if check_package(import_name):
            print(f"✅ {package_name} is already installed")
        else:
            print(f"❌ {package_name} is not installed")
            needs_installation.append(package_name)
    
    if not needs_installation:
        print("\n🎉 All voice recognition packages are already installed!")
        print("You can now use voice commands in the iris recognition system.")
        return True
    
    print(f"\n📋 Need to install: {', '.join(needs_installation)}")
    
    # Ask for confirmation
    response = input("\nProceed with installation? (y/n): ").lower().strip()
    if response != 'y':
        print("Installation cancelled.")
        return False
    
    print("\n🚀 Starting installation...")
    
    # Install packages
    success_count = 0
    for package_name in needs_installation:
        if install_package(package_name):
            success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 INSTALLATION SUMMARY")
    print("=" * 60)
    
    if success_count == len(needs_installation):
        print("🎉 ALL PACKAGES INSTALLED SUCCESSFULLY!")
        print("\n✅ Voice commands are now available")
        print("🎤 You can use the following voice commands:")
        print("   • 'Start recognition' - Begin iris scanning")
        print("   • 'Take photo' - Capture screenshot")
        print("   • 'Show gallery' - Open iris gallery")
        print("   • 'Stop recognition' - End scanning")
        print("   • 'Help' - Show voice commands")
        print("\n🚀 Restart the iris recognition application to use voice commands")
        return True
    else:
        print(f"⚠️ {success_count}/{len(needs_installation)} packages installed successfully")
        print("\nSome packages failed to install. You may need to:")
        print("1. Run this script as administrator")
        print("2. Update pip: python -m pip install --upgrade pip")
        print("3. Install manually: pip install SpeechRecognition pyaudio")
        return False

if __name__ == "__main__":
    main()
