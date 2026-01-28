#!/usr/bin/env python3
"""
🎬 Simple Iris Recognition Animation Creator
Simplified version with better error handling and codec compatibility
"""

import cv2
import numpy as np
import os

class SimpleIrisAnimator:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.fps = 24
        self.duration = 30  # Shorter duration for reliability
        
        # Colors
        self.colors = {
            'bg': (26, 26, 46),      # Dark blue background
            'primary': (22, 33, 62),  # Primary blue
            'accent': (15, 52, 96),   # Accent blue
            'success': (0, 255, 136), # Green
            'warning': (255, 170, 0), # Orange
            'text': (255, 255, 255),  # White
            'secondary': (160, 160, 160) # Gray
        }
        
    def create_video(self):
        """Create a simple but effective animation video"""
        print("🎬 Creating Simple Iris Recognition Animation...")
        
        output_path = "iris_demo_simple.mp4"
        
        # Try multiple codecs for maximum compatibility
        codecs = [
            ('mp4v', cv2.VideoWriter_fourcc(*'mp4v')),
            ('XVID', cv2.VideoWriter_fourcc(*'XVID')),
            ('MJPG', cv2.VideoWriter_fourcc(*'MJPG'))
        ]
        
        writer = None
        for codec_name, fourcc in codecs:
            print(f"🔄 Trying {codec_name} codec...")
            writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
            if writer.isOpened():
                print(f"✅ Success with {codec_name} codec!")
                break
            writer.release()
        
        if not writer or not writer.isOpened():
            print("❌ Failed to initialize video writer")
            return False
        
        total_frames = self.duration * self.fps
        print(f"📊 Creating {total_frames} frames at {self.width}x{self.height}")
        
        try:
            for frame_num in range(total_frames):
                progress = frame_num / total_frames
                frame = self.create_frame(progress)
                
                # Ensure frame is in correct format
                if frame.dtype != np.uint8:
                    frame = frame.astype(np.uint8)
                
                writer.write(frame)
                
                # Progress update
                if frame_num % (self.fps * 2) == 0:  # Every 2 seconds
                    percent = (frame_num / total_frames) * 100
                    print(f"⏳ Progress: {percent:.1f}%")
            
            writer.release()
            
            # Verify file was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"✅ Video created: {output_path} ({file_size:.1f} MB)")
                return True
            else:
                print("❌ Video file was not created")
                return False
                
        except Exception as e:
            print(f"❌ Error during video creation: {e}")
            writer.release()
            return False
    
    def create_frame(self, progress):
        """Create a single frame based on progress (0.0 to 1.0)"""
        # Create blank frame
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame[:] = self.colors['bg']
        
        # Determine current scene
        if progress < 0.2:
            frame = self.draw_title_scene(frame, progress / 0.2)
        elif progress < 0.4:
            frame = self.draw_features_scene(frame, (progress - 0.2) / 0.2)
        elif progress < 0.6:
            frame = self.draw_demo_scene(frame, (progress - 0.4) / 0.2)
        elif progress < 0.8:
            frame = self.draw_analytics_scene(frame, (progress - 0.6) / 0.2)
        else:
            frame = self.draw_closing_scene(frame, (progress - 0.8) / 0.2)
        
        return frame
    
    def draw_title_scene(self, frame, progress):
        """Draw title scene"""
        if progress > 0.3:
            alpha = min((progress - 0.3) / 0.4, 1.0)
            
            # Main title
            self.draw_text(frame, "Iris Recognition System", 
                          (self.width//2, self.height//2 - 50), 
                          size=2.0, color=self.colors['text'], alpha=alpha)
            
            # Subtitle
            if progress > 0.6:
                sub_alpha = min((progress - 0.6) / 0.4, 1.0)
                self.draw_text(frame, "Advanced Biometric Security", 
                              (self.width//2, self.height//2 + 20), 
                              size=1.0, color=self.colors['secondary'], alpha=sub_alpha)
        
        # Animated iris
        if progress > 0.7:
            iris_alpha = min((progress - 0.7) / 0.3, 1.0)
            self.draw_iris(frame, (self.width//2, self.height//2 + 100), 
                          size=80, alpha=iris_alpha)
        
        return frame
    
    def draw_features_scene(self, frame, progress):
        """Draw features overview"""
        # Title
        self.draw_text(frame, "Key Features", 
                      (self.width//2, 100), 
                      size=1.5, color=self.colors['text'])
        
        features = [
            "Deep Learning CNN Models",
            "Real-time Recognition", 
            "Voice Commands",
            "Analytics Dashboard",
            "Live Gallery",
            "98%+ Accuracy"
        ]
        
        for i, feature in enumerate(features):
            feature_progress = max(0, min((progress - i * 0.15) / 0.2, 1.0))
            if feature_progress > 0:
                y_pos = 200 + i * 60
                
                # Feature box
                box_alpha = int(feature_progress * 100)
                cv2.rectangle(frame, 
                            (200, y_pos - 20), 
                            (self.width - 200, y_pos + 20),
                            self.colors['primary'], -1)
                
                # Feature text
                self.draw_text(frame, f"• {feature}", 
                              (220, y_pos), 
                              size=0.8, color=self.colors['success'], alpha=feature_progress)
        
        return frame
    
    def draw_demo_scene(self, frame, progress):
        """Draw demo visualization"""
        # Title
        self.draw_text(frame, "Live Recognition Demo", 
                      (self.width//2, 80), 
                      size=1.5, color=self.colors['text'])
        
        # Camera frame simulation
        cam_x, cam_y = 200, 150
        cam_w, cam_h = 400, 300
        
        cv2.rectangle(frame, (cam_x, cam_y), (cam_x + cam_w, cam_y + cam_h), 
                     (50, 50, 50), -1)
        cv2.rectangle(frame, (cam_x, cam_y), (cam_x + cam_w, cam_y + cam_h), 
                     self.colors['success'], 2)
        
        # Simulated eye detection
        if progress > 0.3:
            eye_center = (cam_x + cam_w//2, cam_y + cam_h//2)
            
            # Face outline
            cv2.circle(frame, eye_center, 80, self.colors['secondary'], 2)
            
            # Eyes
            left_eye = (eye_center[0] - 30, eye_center[1] - 10)
            right_eye = (eye_center[0] + 30, eye_center[1] - 10)
            
            cv2.circle(frame, left_eye, 20, self.colors['success'], 2)
            cv2.circle(frame, right_eye, 20, self.colors['success'], 2)
            
            # Detection boxes
            if progress > 0.6:
                self.draw_detection_box(frame, left_eye, 50)
                self.draw_detection_box(frame, right_eye, 50)
        
        # Results panel
        if progress > 0.5:
            panel_x = cam_x + cam_w + 50
            panel_y = cam_y
            
            cv2.rectangle(frame, (panel_x, panel_y), 
                         (panel_x + 300, panel_y + 200), 
                         self.colors['primary'], -1)
            
            results = [
                "Person ID: person_042",
                "Confidence: 97.8%", 
                "Status: VERIFIED",
                "Time: 234ms"
            ]
            
            for i, result in enumerate(results):
                self.draw_text(frame, result, 
                              (panel_x + 20, panel_y + 40 + i * 30), 
                              size=0.6, color=self.colors['success'])
        
        return frame

    def draw_analytics_scene(self, frame, progress):
        """Draw analytics dashboard"""
        # Title
        self.draw_text(frame, "Analytics Dashboard",
                      (self.width//2, 80),
                      size=1.5, color=self.colors['text'])

        # Metrics boxes
        metrics = [
            ("Accuracy", "98.2%"),
            ("Speed", "234ms"),
            ("Users", "108"),
            ("Uptime", "99.9%")
        ]

        for i, (label, value) in enumerate(metrics):
            box_progress = max(0, min((progress - i * 0.2) / 0.3, 1.0))
            if box_progress > 0:
                x = 200 + (i % 2) * 400
                y = 200 + (i // 2) * 150

                # Metric box
                cv2.rectangle(frame, (x, y), (x + 300, y + 100),
                             self.colors['primary'], -1)
                cv2.rectangle(frame, (x, y), (x + 300, y + 100),
                             self.colors['success'], 2)

                # Metric text
                self.draw_text(frame, label, (x + 150, y + 30),
                              size=0.8, color=self.colors['text'])
                self.draw_text(frame, value, (x + 150, y + 70),
                              size=1.2, color=self.colors['success'])

        return frame

    def draw_closing_scene(self, frame, progress):
        """Draw closing scene"""
        if progress > 0.2:
            alpha = min((progress - 0.2) / 0.3, 1.0)

            # Main message
            self.draw_text(frame, "Advanced Iris Recognition",
                          (self.width//2, self.height//2 - 80),
                          size=1.8, color=self.colors['text'], alpha=alpha)

            self.draw_text(frame, "Ready for Production",
                          (self.width//2, self.height//2 - 20),
                          size=1.2, color=self.colors['secondary'], alpha=alpha)

        if progress > 0.5:
            features_alpha = min((progress - 0.5) / 0.3, 1.0)
            self.draw_text(frame, "98%+ Accuracy • Real-time • Voice Control",
                          (self.width//2, self.height//2 + 40),
                          size=0.8, color=self.colors['success'], alpha=features_alpha)

        if progress > 0.7:
            cta_alpha = min((progress - 0.7) / 0.3, 1.0)
            self.draw_text(frame, "Start Your Biometric Journey Today!",
                          (self.width//2, self.height//2 + 100),
                          size=1.0, color=self.colors['warning'], alpha=cta_alpha)

        return frame

    def draw_text(self, frame, text, pos, size=1.0, color=(255, 255, 255), alpha=1.0):
        """Draw text with proper centering"""
        x, y = pos
        font = cv2.FONT_HERSHEY_SIMPLEX
        thickness = max(1, int(size * 2))

        # Get text size for centering
        (text_width, text_height), _ = cv2.getTextSize(text, font, size, thickness)
        x = x - text_width // 2
        y = y + text_height // 2

        # Apply alpha if needed
        if alpha < 1.0:
            overlay = frame.copy()
            cv2.putText(overlay, text, (int(x), int(y)), font, size, color, thickness)
            cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0, frame)
        else:
            cv2.putText(frame, text, (int(x), int(y)), font, size, color, thickness)

    def draw_iris(self, frame, pos, size=60, alpha=1.0):
        """Draw a simple iris icon"""
        x, y = pos

        # Outer circle (iris)
        cv2.circle(frame, (x, y), size//2, self.colors['success'], 2)

        # Inner circle (pupil)
        cv2.circle(frame, (x, y), size//4, self.colors['text'], 2)

        # Iris patterns
        for i in range(8):
            angle = i * 45
            angle_rad = np.radians(angle)
            start_r = size//4 + 5
            end_r = size//2 - 5

            start_x = x + int(start_r * np.cos(angle_rad))
            start_y = y + int(start_r * np.sin(angle_rad))
            end_x = x + int(end_r * np.cos(angle_rad))
            end_y = y + int(end_r * np.sin(angle_rad))

            cv2.line(frame, (start_x, start_y), (end_x, end_y),
                    self.colors['success'], 1)

    def draw_detection_box(self, frame, center, size):
        """Draw detection box corners"""
        x, y = center
        half_size = size // 2
        corner_length = 15

        # Top-left
        cv2.line(frame, (x - half_size, y - half_size),
                (x - half_size + corner_length, y - half_size),
                self.colors['warning'], 2)
        cv2.line(frame, (x - half_size, y - half_size),
                (x - half_size, y - half_size + corner_length),
                self.colors['warning'], 2)

        # Top-right
        cv2.line(frame, (x + half_size, y - half_size),
                (x + half_size - corner_length, y - half_size),
                self.colors['warning'], 2)
        cv2.line(frame, (x + half_size, y - half_size),
                (x + half_size, y - half_size + corner_length),
                self.colors['warning'], 2)

        # Bottom-left
        cv2.line(frame, (x - half_size, y + half_size),
                (x - half_size + corner_length, y + half_size),
                self.colors['warning'], 2)
        cv2.line(frame, (x - half_size, y + half_size),
                (x - half_size, y + half_size - corner_length),
                self.colors['warning'], 2)

        # Bottom-right
        cv2.line(frame, (x + half_size, y + half_size),
                (x + half_size - corner_length, y + half_size),
                self.colors['warning'], 2)
        cv2.line(frame, (x + half_size, y + half_size),
                (x + half_size, y + half_size - corner_length),
                self.colors['warning'], 2)


def main():
    """Create the simple animation"""
    print("🎬 Simple Iris Recognition Animation Creator")
    print("=" * 50)

    animator = SimpleIrisAnimator()
    success = animator.create_video()

    if success:
        print("\n🎉 Simple animation created successfully!")
        print("📁 Output: iris_demo_simple.mp4")
        print("📊 Specs: 1280x720, 24fps, 30 seconds")
        print("\n✨ This version should play without issues!")
    else:
        print("\n❌ Failed to create animation")

    return success

if __name__ == "__main__":
    main()
