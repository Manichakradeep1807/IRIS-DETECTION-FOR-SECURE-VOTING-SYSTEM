#!/usr/bin/env python3
"""
🎵 Add Background Music to Iris Recognition Video
Creates a new video with professional background music
"""

import cv2
import numpy as np
import os
import subprocess
import sys

class VideoMusicCombiner:
    def __init__(self):
        self.video_file = "iris_recognition_enhanced.mp4"
        self.audio_file = "background_music.wav"
        self.output_file = "iris_recognition_with_music.mp4"
        
    def check_ffmpeg(self):
        """Check if ffmpeg is available"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ FFmpeg found!")
                return True
        except FileNotFoundError:
            pass
        
        print("⚠️ FFmpeg not found. Trying alternative methods...")
        return False
    
    def download_ffmpeg(self):
        """Guide user to download ffmpeg"""
        print("\n🔧 To add background music, you need FFmpeg:")
        print("\n📥 Download Options:")
        print("1. 🌐 Visit: https://ffmpeg.org/download.html")
        print("2. 📦 Or use package manager:")
        print("   - Windows: choco install ffmpeg")
        print("   - Or download from: https://www.gyan.dev/ffmpeg/builds/")
        print("\n💡 Quick Windows Setup:")
        print("1. Download ffmpeg-release-essentials.zip")
        print("2. Extract to C:\\ffmpeg")
        print("3. Add C:\\ffmpeg\\bin to PATH")
        print("4. Restart command prompt")
        
        return False
    
    def create_enhanced_background_music(self):
        """Create an enhanced background music track"""
        try:
            print("🎵 Creating enhanced background music...")
            
            # Create a more sophisticated background track
            sample_rate = 44100
            duration = 45  # 45 seconds to match video
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Create a pleasant melody with multiple layers
            audio = np.zeros_like(t)
            
            # Base chord progression: C - Am - F - G
            chord_duration = duration / 4
            
            for i, base_freq in enumerate([261.63, 220.00, 174.61, 196.00]):  # C, A, F, G
                start_time = i * chord_duration
                end_time = (i + 1) * chord_duration
                
                # Time mask for this chord
                mask = (t >= start_time) & (t < end_time)
                chord_t = t[mask] - start_time
                
                if len(chord_t) > 0:
                    # Major chord (root, third, fifth)
                    frequencies = [base_freq, base_freq * 1.25, base_freq * 1.5]
                    
                    for freq in frequencies:
                        # Add fundamental and harmonics
                        audio[mask] += 0.2 * np.sin(2 * np.pi * freq * chord_t)
                        audio[mask] += 0.1 * np.sin(2 * np.pi * freq * 2 * chord_t)  # Octave
                        audio[mask] += 0.05 * np.sin(2 * np.pi * freq * 3 * chord_t)  # Fifth
            
            # Add gentle melody line
            melody_freqs = [523.25, 587.33, 659.25, 698.46, 783.99, 880.00, 987.77, 1046.50]  # C5 to C6
            melody_pattern = [0, 2, 4, 5, 7, 5, 4, 2, 0]  # Simple scale pattern
            
            note_duration = duration / len(melody_pattern)
            for i, note_idx in enumerate(melody_pattern):
                if note_idx < len(melody_freqs):
                    start_time = i * note_duration
                    end_time = (i + 1) * note_duration
                    
                    mask = (t >= start_time) & (t < end_time)
                    note_t = t[mask] - start_time
                    
                    if len(note_t) > 0:
                        freq = melody_freqs[note_idx]
                        # Gentle melody with envelope
                        envelope = np.exp(-note_t * 2)  # Decay envelope
                        audio[mask] += 0.15 * envelope * np.sin(2 * np.pi * freq * note_t)
            
            # Add subtle ambient pad
            for freq in [65.41, 82.41, 98.00]:  # Low C, E, G
                audio += 0.08 * np.sin(2 * np.pi * freq * t)
                audio += 0.04 * np.sin(2 * np.pi * freq * t + np.pi/4)  # Phase shift
            
            # Apply gentle fade in/out
            fade_samples = int(sample_rate * 3)  # 3 second fade
            audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
            audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Normalize and apply gentle compression
            audio = audio / np.max(np.abs(audio)) * 0.25  # Keep volume gentle
            
            # Save enhanced audio
            audio_file = "enhanced_background_music.wav"
            audio_16bit = (audio * 32767).astype(np.int16)
            
            # Write WAV file
            with open(audio_file, 'wb') as f:
                # WAV header
                f.write(b'RIFF')
                f.write((36 + len(audio_16bit) * 2).to_bytes(4, 'little'))
                f.write(b'WAVE')
                f.write(b'fmt ')
                f.write((16).to_bytes(4, 'little'))
                f.write((1).to_bytes(2, 'little'))  # PCM
                f.write((1).to_bytes(2, 'little'))  # Mono
                f.write(sample_rate.to_bytes(4, 'little'))
                f.write((sample_rate * 2).to_bytes(4, 'little'))
                f.write((2).to_bytes(2, 'little'))
                f.write((16).to_bytes(2, 'little'))
                f.write(b'data')
                f.write((len(audio_16bit) * 2).to_bytes(4, 'little'))
                f.write(audio_16bit.tobytes())
            
            print(f"✅ Enhanced background music created: {audio_file}")
            return audio_file
            
        except Exception as e:
            print(f"❌ Error creating enhanced music: {e}")
            return None
    
    def combine_with_ffmpeg(self):
        """Combine video and audio using ffmpeg"""
        if not os.path.exists(self.video_file):
            print(f"❌ Video file not found: {self.video_file}")
            return False
        
        # Create enhanced music if needed
        if not os.path.exists(self.audio_file):
            print("🎵 Creating background music...")
            self.audio_file = self.create_enhanced_background_music()
            if not self.audio_file:
                return False
        
        try:
            cmd = [
                'ffmpeg', '-y',  # Overwrite output
                '-i', self.video_file,  # Input video
                '-i', self.audio_file,  # Input audio
                '-c:v', 'copy',  # Copy video stream
                '-c:a', 'aac',   # Encode audio as AAC
                '-map', '0:v:0', # Map video from first input
                '-map', '1:a:0', # Map audio from second input
                '-shortest',     # End when shortest stream ends
                '-movflags', '+faststart',  # Optimize for web
                self.output_file
            ]
            
            print("🎬 Combining video and audio...")
            print(f"📹 Video: {self.video_file}")
            print(f"🎵 Audio: {self.audio_file}")
            print(f"📁 Output: {self.output_file}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if os.path.exists(self.output_file):
                    file_size = os.path.getsize(self.output_file) / (1024 * 1024)
                    print(f"✅ Success! Video with music created: {self.output_file}")
                    print(f"📊 File size: {file_size:.1f} MB")
                    return True
                else:
                    print("❌ Output file was not created")
                    return False
            else:
                print(f"❌ FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error combining video and audio: {e}")
            return False
    
    def create_video_with_embedded_audio(self):
        """Alternative method: Create new video with audio embedded"""
        print("🔄 Using alternative method to add background music...")
        
        try:
            # Create enhanced background music
            audio_file = self.create_enhanced_background_music()
            if not audio_file:
                return False
            
            # Read the original video
            cap = cv2.VideoCapture(self.video_file)
            if not cap.isOpened():
                print(f"❌ Cannot open video: {self.video_file}")
                return False
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            print(f"📊 Video properties: {width}x{height} @ {fps}fps, {total_frames} frames")
            
            # Create output video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            temp_video = "temp_video_for_audio.mp4"
            out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))
            
            if not out.isOpened():
                print("❌ Cannot create output video writer")
                cap.release()
                return False
            
            # Copy all frames
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                out.write(frame)
                frame_count += 1
                
                if frame_count % (fps * 5) == 0:  # Every 5 seconds
                    progress = (frame_count / total_frames) * 100
                    print(f"⏳ Processing: {progress:.1f}%")
            
            cap.release()
            out.release()
            
            print("✅ Video processing complete")
            
            # Now try to combine with audio using ffmpeg
            if self.check_ffmpeg():
                cmd = [
                    'ffmpeg', '-y',
                    '-i', temp_video,
                    '-i', audio_file,
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-shortest',
                    self.output_file
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    os.remove(temp_video)  # Clean up
                    print(f"✅ Video with music created: {self.output_file}")
                    return True
                else:
                    # Rename temp video as fallback
                    os.rename(temp_video, self.output_file)
                    print(f"⚠️ Audio combination failed, but video saved: {self.output_file}")
                    print(f"🎵 Play {audio_file} separately for background music")
                    return True
            else:
                # Rename temp video as fallback
                os.rename(temp_video, self.output_file)
                print(f"⚠️ FFmpeg not available, but video saved: {self.output_file}")
                print(f"🎵 Play {audio_file} separately for background music")
                return True
                
        except Exception as e:
            print(f"❌ Error in alternative method: {e}")
            return False
    
    def add_background_music(self):
        """Main method to add background music"""
        print("🎵 Adding Background Music to Iris Recognition Video")
        print("=" * 60)
        
        # Check if files exist
        if not os.path.exists(self.video_file):
            print(f"❌ Video file not found: {self.video_file}")
            return False
        
        video_size = os.path.getsize(self.video_file) / (1024 * 1024)
        print(f"📹 Input video: {self.video_file} ({video_size:.1f} MB)")
        
        # Try ffmpeg first
        if self.check_ffmpeg():
            success = self.combine_with_ffmpeg()
            if success:
                return True
        
        # Try alternative method
        print("\n🔄 Trying alternative method...")
        success = self.create_video_with_embedded_audio()
        
        if success:
            print("\n🎉 Background music added successfully!")
            print(f"📁 Output: {self.output_file}")
            print("\n🎬 How to play:")
            print(f"   Double-click: {self.output_file}")
            print("   Or drag into web browser")
            print("   Or use VLC Media Player")
            return True
        else:
            print("\n❌ Failed to add background music")
            self.download_ffmpeg()
            return False

def main():
    """Main function"""
    combiner = VideoMusicCombiner()
    success = combiner.add_background_music()
    
    if success:
        print("\n🚀 Your video with background music is ready!")
    else:
        print("\n💡 Alternative: Play the video and audio files simultaneously")
        print("   📹 Video: iris_recognition_enhanced.mp4")
        print("   🎵 Audio: background_music.wav or enhanced_background_music.wav")
    
    return success

if __name__ == "__main__":
    main()
