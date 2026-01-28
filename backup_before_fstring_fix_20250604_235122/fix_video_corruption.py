#!/usr/bin/env python3
"""
🔧 Video Corruption Fix Script
Removes corrupted video and creates a new working version
"""

import os
import sys

def main():
    """Fix video corruption issues"""
    print("🔧 Video Corruption Fix Script")
    print("=" * 40)
    
    # Check for corrupted files
    corrupted_files = []
    if os.path.exists("iris_recognition_demo.mp4"):
        file_size = os.path.getsize("iris_recognition_demo.mp4") / (1024 * 1024)
        print(f"📁 Found: iris_recognition_demo.mp4 ({file_size:.1f} MB)")
        
        # If file is suspiciously small or large, it might be corrupted
        if file_size < 5 or file_size > 100:
            corrupted_files.append("iris_recognition_demo.mp4")
    
    # Check for working simple version
    if os.path.exists("iris_demo_simple.mp4"):
        file_size = os.path.getsize("iris_demo_simple.mp4") / (1024 * 1024)
        print(f"✅ Found working: iris_demo_simple.mp4 ({file_size:.1f} MB)")
    
    if corrupted_files:
        print(f"\n⚠️ Potentially corrupted files detected: {corrupted_files}")
        
        response = input("\n🗑️ Remove corrupted files and create new ones? (y/n): ").lower()
        if response == 'y':
            # Remove corrupted files
            for file in corrupted_files:
                try:
                    os.remove(file)
                    print(f"🗑️ Removed: {file}")
                except Exception as e:
                    print(f"❌ Error removing {file}: {e}")
            
            # Create new working version
            print("\n🎬 Creating new working animation...")
            try:
                from create_simple_animation import main as create_simple
                success = create_simple()
                
                if success:
                    print("\n✅ New working animation created!")
                    print("📁 File: iris_demo_simple.mp4")
                else:
                    print("\n❌ Failed to create new animation")
                    
            except Exception as e:
                print(f"❌ Error creating animation: {e}")
        else:
            print("🚫 Keeping existing files")
    
    # Provide playback instructions
    print("\n" + "=" * 50)
    print("🎬 HOW TO PLAY YOUR VIDEO")
    print("=" * 50)
    
    if os.path.exists("iris_demo_simple.mp4"):
        print("\n✅ Working video available: iris_demo_simple.mp4")
        print("\n📱 How to play:")
        print("   1. Double-click the file")
        print("   2. Or drag it into any web browser")
        print("   3. Or use VLC Media Player")
        
        print("\n📊 Video specs:")
        file_size = os.path.getsize("iris_demo_simple.mp4") / (1024 * 1024)
        print(f"   📐 Resolution: 1280x720 (HD)")
        print(f"   ⏱️ Duration: 30 seconds")
        print(f"   📁 Size: {file_size:.1f} MB")
        print(f"   🎞️ Format: MP4 (Universal)")
        
        print("\n🎯 What you'll see:")
        print("   🎬 Professional title sequence")
        print("   ✨ Key features overview")
        print("   👁️ Live recognition demo")
        print("   📊 Analytics dashboard")
        print("   🎉 Professional closing")
        
    else:
        print("\n❌ No working video found")
        print("🔄 Run: python create_simple_animation.py")
    
    print("\n🚀 Your animation is ready to impress!")

if __name__ == "__main__":
    main()
