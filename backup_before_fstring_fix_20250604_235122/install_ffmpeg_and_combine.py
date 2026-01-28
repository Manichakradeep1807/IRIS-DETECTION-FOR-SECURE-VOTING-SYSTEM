#!/usr/bin/env python3
"""
🔧 Install FFmpeg and Combine Video with Audio
Automated solution to add background music properly
"""

import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ffmpeg_windows():
    """Install ffmpeg on Windows"""
    print("📦 Installing FFmpeg for Windows...")
    
    try:
        # Check if we can use winget (Windows Package Manager)
        try:
            result = subprocess.run(['winget', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("🔄 Installing FFmpeg using winget...")
                result = subprocess.run(['winget', 'install', 'FFmpeg'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ FFmpeg installed successfully!")
                    return True
        except FileNotFoundError:
            pass
        
        # Try chocolatey
        try:
            result = subprocess.run(['choco', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("🔄 Installing FFmpeg using Chocolatey...")
                result = subprocess.run(['choco', 'install', 'ffmpeg', '-y'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ FFmpeg installed successfully!")
                    return True
        except FileNotFoundError:
            pass
        
        print("⚠️ Automatic installation not available")
        return False
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def download_ffmpeg_portable():
    """Download portable FFmpeg"""
    print("📥 Downloading portable FFmpeg...")
    
    try:
        # Create ffmpeg directory
        ffmpeg_dir = "ffmpeg_portable"
        if not os.path.exists(ffmpeg_dir):
            os.makedirs(ffmpeg_dir)
        
        # Download URL (simplified - in real scenario you'd use official builds)
        print("💡 For security reasons, please manually download FFmpeg:")
        print("1. Visit: https://www.gyan.dev/ffmpeg/builds/")
        print("2. Download: ffmpeg-release-essentials.zip")
        print("3. Extract to: ffmpeg_portable/")
        print("4. Run this script again")
        
        return False
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def combine_video_audio_properly():
    """Combine video and audio with proper ffmpeg"""
    video_file = "iris_recognition_enhanced.mp4"
    audio_file = "enhanced_background_music.wav"
    output_file = "iris_recognition_final_with_music.mp4"
    
    if not os.path.exists(video_file):
        print(f"❌ Video file not found: {video_file}")
        return False
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    try:
        cmd = [
            'ffmpeg', '-y',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',
            '-movflags', '+faststart',
            output_file
        ]
        
        print("🎬 Combining video and audio with FFmpeg...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ SUCCESS! Video with music: {output_file}")
                print(f"📊 File size: {file_size:.1f} MB")
                return True
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_batch_file():
    """Create a batch file for easy execution"""
    batch_content = '''@echo off
echo 🎵 Adding Background Music to Iris Recognition Video
echo =====================================================

echo 📦 Checking for FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ FFmpeg not found
    echo 📥 Please install FFmpeg first:
    echo    1. Visit: https://www.gyan.dev/ffmpeg/builds/
    echo    2. Download ffmpeg-release-essentials.zip
    echo    3. Extract and add to PATH
    echo    4. Restart command prompt
    pause
    exit /b 1
)

echo ✅ FFmpeg found!
echo 🎬 Combining video and audio...

ffmpeg -y -i iris_recognition_enhanced.mp4 -i enhanced_background_music.wav -c:v copy -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 -shortest -movflags +faststart iris_recognition_final_with_music.mp4

if %errorlevel% equ 0 (
    echo ✅ SUCCESS! Video with music created!
    echo 📁 File: iris_recognition_final_with_music.mp4
) else (
    echo ❌ Failed to combine video and audio
)

pause
'''
    
    with open("add_music.bat", "w") as f:
        f.write(batch_content)
    
    print("✅ Created batch file: add_music.bat")
    print("💡 You can double-click add_music.bat to combine video and audio")

def main():
    """Main function"""
    print("🎵 FFmpeg Installation and Video-Audio Combiner")
    print("=" * 55)
    
    # Check if ffmpeg is already available
    if check_ffmpeg():
        print("✅ FFmpeg is already installed!")
        success = combine_video_audio_properly()
        if success:
            print("\n🎉 Video with background music created successfully!")
            return True
    else:
        print("❌ FFmpeg not found")
        
        # Try to install ffmpeg
        if sys.platform.startswith('win'):
            print("🔧 Attempting to install FFmpeg on Windows...")
            if install_ffmpeg_windows():
                print("✅ FFmpeg installed! Trying to combine video and audio...")
                success = combine_video_audio_properly()
                if success:
                    return True
        
        # Create batch file as fallback
        print("\n🔄 Creating manual installation helper...")
        create_batch_file()
        
        print("\n📋 Manual Installation Steps:")
        print("1. 📥 Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/")
        print("2. 📦 Download: ffmpeg-release-essentials.zip")
        print("3. 📂 Extract to C:\\ffmpeg")
        print("4. ⚙️ Add C:\\ffmpeg\\bin to your PATH environment variable")
        print("5. 🔄 Restart command prompt")
        print("6. 🎬 Double-click: add_music.bat")
        
        print("\n💡 Alternative: Use online video editors:")
        print("   - Kapwing.com")
        print("   - Clideo.com")
        print("   - Online-video-cutter.com")
        
    return False

if __name__ == "__main__":
    main()
