#!/usr/bin/env python3
"""
🎬 Iris Recognition Project Animation Video Creator
Creates a professional animation video showcasing all project features
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
import os
import time
from datetime import datetime
import json

class IrisProjectAnimator:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.fps = 30
        self.duration = 75  # 75 seconds total
        
        # Colors (matching project theme)
        self.colors = {
            'primary': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f3460',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'error': '#ff4757',
            'text': '#ffffff',
            'text_secondary': '#a0a0a0'
        }
        
        # Video writer
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        
        # Animation scenes
        self.scenes = [
            {'name': 'title', 'duration': 5, 'start': 0},
            {'name': 'overview', 'duration': 8, 'start': 5},
            {'name': 'gui_demo', 'duration': 12, 'start': 13},
            {'name': 'training', 'duration': 10, 'start': 25},
            {'name': 'live_recognition', 'duration': 15, 'start': 35},
            {'name': 'voice_commands', 'duration': 8, 'start': 50},
            {'name': 'analytics', 'duration': 10, 'start': 58},
            {'name': 'gallery', 'duration': 7, 'start': 68},
            {'name': 'closing', 'duration': 7, 'start': 75}
        ]
        
    def create_video(self):
        """Create the complete animation video"""
        print("🎬 Starting Iris Recognition Project Animation Video Creation...")
        
        # Initialize video writer with better codec
        output_path = "iris_recognition_demo.mp4"

        # Try different codecs for better compatibility
        codecs_to_try = [
            cv2.VideoWriter_fourcc(*'mp4v'),  # MP4V codec
            cv2.VideoWriter_fourcc(*'XVID'),  # XVID codec
            cv2.VideoWriter_fourcc(*'MJPG'),  # MJPG codec
            cv2.VideoWriter_fourcc(*'X264')   # X264 codec
        ]

        self.out = None
        for i, codec in enumerate(codecs_to_try):
            print(f"🔄 Trying codec {i+1}/4...")
            self.out = cv2.VideoWriter(output_path, codec, self.fps, (self.width, self.height))
            if self.out.isOpened():
                print(f"✅ Successfully initialized with codec {i+1}")
                break
            else:
                if self.out:
                    self.out.release()

        if not self.out or not self.out.isOpened():
            print("❌ Error: Could not open video writer with any codec")
            return False
        
        total_frames = self.duration * self.fps
        
        print(f"📊 Video specs: {self.width}x{self.height} @ {self.fps}fps, {self.duration}s ({total_frames} frames)")
        
        # Generate all frames
        for frame_num in range(total_frames):
            current_time = frame_num / self.fps
            frame = self.create_frame(current_time)
            
            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.out.write(frame_bgr)
            
            # Progress indicator
            if frame_num % (self.fps * 5) == 0:  # Every 5 seconds
                progress = (frame_num / total_frames) * 100
                print(f"⏳ Progress: {progress:.1f}% ({frame_num}/{total_frames} frames)")
        
        # Cleanup
        self.out.release()
        print(f"✅ Video created successfully: {output_path}")
        return True
    
    def create_frame(self, time_sec):
        """Create a single frame at given time"""
        # Create blank frame
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Determine current scene
        current_scene = None
        for scene in self.scenes:
            if scene['start'] <= time_sec < scene['start'] + scene['duration']:
                current_scene = scene
                break
        
        if not current_scene:
            current_scene = self.scenes[-1]  # Default to last scene
        
        # Calculate scene progress (0.0 to 1.0)
        scene_time = time_sec - current_scene['start']
        scene_progress = min(scene_time / current_scene['duration'], 1.0)
        
        # Render scene
        if current_scene['name'] == 'title':
            frame = self.render_title_scene(frame, scene_progress)
        elif current_scene['name'] == 'overview':
            frame = self.render_overview_scene(frame, scene_progress)
        elif current_scene['name'] == 'gui_demo':
            frame = self.render_gui_demo_scene(frame, scene_progress)
        elif current_scene['name'] == 'training':
            frame = self.render_training_scene(frame, scene_progress)
        elif current_scene['name'] == 'live_recognition':
            frame = self.render_live_recognition_scene(frame, scene_progress)
        elif current_scene['name'] == 'voice_commands':
            frame = self.render_voice_commands_scene(frame, scene_progress)
        elif current_scene['name'] == 'analytics':
            frame = self.render_analytics_scene(frame, scene_progress)
        elif current_scene['name'] == 'gallery':
            frame = self.render_gallery_scene(frame, scene_progress)
        elif current_scene['name'] == 'closing':
            frame = self.render_closing_scene(frame, scene_progress)
        
        return frame
    
    def render_title_scene(self, frame, progress):
        """Render title scene with animated logo and text"""
        # Background gradient
        frame = self.create_gradient_background(frame, self.colors['primary'], self.colors['secondary'])
        
        # Animated title appearance
        if progress > 0.2:
            alpha = min((progress - 0.2) / 0.3, 1.0)
            
            # Main title
            title = "🔍 Advanced Iris Recognition System"
            frame = self.draw_text(frame, title, (self.width//2, self.height//2 - 100), 
                                 size=72, color=self.colors['text'], alpha=alpha, center=True, bold=True)
            
            # Subtitle
            if progress > 0.5:
                subtitle_alpha = min((progress - 0.5) / 0.3, 1.0)
                subtitle = "Deep Learning • Biometric Security • Real-time Recognition"
                frame = self.draw_text(frame, subtitle, (self.width//2, self.height//2 + 20), 
                                     size=36, color=self.colors['text_secondary'], alpha=subtitle_alpha, center=True)
        
        # Animated iris icon
        if progress > 0.7:
            icon_alpha = min((progress - 0.7) / 0.3, 1.0)
            frame = self.draw_iris_icon(frame, (self.width//2, self.height//2 + 150), 
                                      size=120, alpha=icon_alpha, animated=True, progress=progress)
        
        return frame
    
    def render_overview_scene(self, frame, progress):
        """Render system overview with feature highlights"""
        frame = self.create_gradient_background(frame, self.colors['secondary'], self.colors['accent'])
        
        # Title
        title = "🌟 System Overview"
        frame = self.draw_text(frame, title, (self.width//2, 100), 
                             size=64, color=self.colors['text'], center=True, bold=True)
        
        # Feature boxes
        features = [
            {"icon": "🧠", "title": "Deep Learning CNN", "desc": "Advanced neural networks for 98%+ accuracy"},
            {"icon": "👁️", "title": "Real-time Recognition", "desc": "Live video processing with instant results"},
            {"icon": "📊", "title": "Analytics Dashboard", "desc": "Comprehensive performance monitoring"},
            {"icon": "🎤", "title": "Voice Commands", "desc": "Hands-free operation with speech control"},
            {"icon": "🖼️", "title": "Live Gallery", "desc": "Automatic image capture and organization"},
            {"icon": "🔒", "title": "Secure Database", "desc": "Encrypted biometric template storage"}
        ]
        
        # Animate feature boxes
        for i, feature in enumerate(features):
            box_progress = max(0, min((progress - i * 0.15) / 0.2, 1.0))
            if box_progress > 0:
                x = 200 + (i % 3) * 500
                y = 300 + (i // 3) * 250
                frame = self.draw_feature_box(frame, feature, (x, y), box_progress)
        
        return frame
    
    def draw_feature_box(self, frame, feature, pos, alpha):
        """Draw an animated feature box"""
        x, y = pos
        box_width, box_height = 400, 180
        
        # Box background with animation
        scale = 0.8 + 0.2 * alpha
        actual_width = int(box_width * scale)
        actual_height = int(box_height * scale)
        
        # Draw rounded rectangle
        frame = self.draw_rounded_rect(frame, 
                                     (x - actual_width//2, y - actual_height//2, actual_width, actual_height),
                                     self.colors['primary'], alpha=alpha * 0.9, radius=15)
        
        if alpha > 0.5:
            # Icon
            icon_alpha = min((alpha - 0.5) / 0.5, 1.0)
            frame = self.draw_text(frame, feature['icon'], (x, y - 40), 
                                 size=48, alpha=icon_alpha, center=True)
            
            # Title
            frame = self.draw_text(frame, feature['title'], (x, y), 
                                 size=24, color=self.colors['text'], alpha=icon_alpha, center=True, bold=True)
            
            # Description
            frame = self.draw_text(frame, feature['desc'], (x, y + 30), 
                                 size=16, color=self.colors['text_secondary'], alpha=icon_alpha, center=True)
        
        return frame

    def render_gui_demo_scene(self, frame, progress):
        """Render GUI demonstration with interactive elements"""
        frame = self.create_gradient_background(frame, self.colors['accent'], self.colors['primary'])

        # Title
        title = "💻 Modern GUI Interface"
        frame = self.draw_text(frame, title, (self.width//2, 80),
                             size=56, color=self.colors['text'], center=True, bold=True)

        # Mock GUI window
        gui_x, gui_y = self.width//2 - 400, 150
        gui_width, gui_height = 800, 600

        # Window frame
        frame = self.draw_rounded_rect(frame, (gui_x, gui_y, gui_width, gui_height),
                                     self.colors['primary'], alpha=0.95, radius=10)

        # Title bar
        frame = self.draw_rounded_rect(frame, (gui_x, gui_y, gui_width, 40),
                                     self.colors['secondary'], alpha=1.0, radius=10)

        # Window title
        frame = self.draw_text(frame, "👁️ Iris Recognition System", (gui_x + 20, gui_y + 25),
                             size=18, color=self.colors['text'], bold=True)

        # Buttons with animation
        buttons = [
            {"text": "📁 Upload Dataset", "pos": (gui_x + 50, gui_y + 100), "delay": 0.1},
            {"text": "🧠 Train Model", "pos": (gui_x + 250, gui_y + 100), "delay": 0.2},
            {"text": "🔍 Test Recognition", "pos": (gui_x + 450, gui_y + 100), "delay": 0.3},
            {"text": "📊 View Analytics", "pos": (gui_x + 650, gui_y + 100), "delay": 0.4},
            {"text": "📹 Live Recognition", "pos": (gui_x + 50, gui_y + 180), "delay": 0.5},
            {"text": "🖼️ Show Gallery", "pos": (gui_x + 250, gui_y + 180), "delay": 0.6},
            {"text": "🎤 Voice Commands", "pos": (gui_x + 450, gui_y + 180), "delay": 0.7},
            {"text": "⚙️ Settings", "pos": (gui_x + 650, gui_y + 180), "delay": 0.8}
        ]

        for button in buttons:
            button_alpha = max(0, min((progress - button['delay']) / 0.15, 1.0))
            if button_alpha > 0:
                frame = self.draw_button(frame, button['text'], button['pos'], button_alpha)

        # Console area
        if progress > 0.6:
            console_alpha = min((progress - 0.6) / 0.3, 1.0)
            console_y = gui_y + 280
            frame = self.draw_rounded_rect(frame, (gui_x + 20, console_y, gui_width - 40, 280),
                                         '#000000', alpha=console_alpha * 0.8, radius=5)

            # Console text
            console_lines = [
                "🧠 HIGH-ACCURACY IRIS RECOGNITION MODEL - STARTING...",
                "✅ Model architecture: Advanced ResNet-inspired CNN",
                "📊 Training samples: 2160 images across 108 persons",
                "⚡ Training progress: Epoch 25/50 - Accuracy: 97.8%",
                "🎯 Validation accuracy: 96.2% - Loss: 0.0234",
                "💾 Model saved: best_high_accuracy_model.h5",
                "✨ Training completed successfully!"
            ]

            for i, line in enumerate(console_lines):
                line_alpha = max(0, min((progress - 0.7 - i * 0.05) / 0.1, 1.0))
                if line_alpha > 0:
                    frame = self.draw_text(frame, line, (gui_x + 30, console_y + 20 + i * 25),
                                         size=14, color=self.colors['success'], alpha=line_alpha)

        return frame

    def render_training_scene(self, frame, progress):
        """Render model training visualization"""
        frame = self.create_gradient_background(frame, self.colors['primary'], self.colors['secondary'])

        # Title
        title = "🧠 Deep Learning Model Training"
        frame = self.draw_text(frame, title, (self.width//2, 80),
                             size=56, color=self.colors['text'], center=True, bold=True)

        # Training progress visualization
        if progress > 0.2:
            # Progress bar
            bar_width = 600
            bar_height = 30
            bar_x = self.width//2 - bar_width//2
            bar_y = 200

            # Background
            frame = self.draw_rounded_rect(frame, (bar_x, bar_y, bar_width, bar_height),
                                         self.colors['secondary'], alpha=0.8, radius=15)

            # Progress fill
            fill_progress = min((progress - 0.2) / 0.6, 1.0)
            fill_width = int(bar_width * fill_progress)
            if fill_width > 0:
                frame = self.draw_rounded_rect(frame, (bar_x, bar_y, fill_width, bar_height),
                                             self.colors['success'], alpha=0.9, radius=15)

            # Progress text
            progress_text = f"Training Progress: {int(fill_progress * 100)}%"
            frame = self.draw_text(frame, progress_text, (self.width//2, bar_y + 50),
                                 size=24, color=self.colors['text'], center=True)

        # Accuracy graph simulation
        if progress > 0.4:
            graph_alpha = min((progress - 0.4) / 0.3, 1.0)
            frame = self.draw_training_graph(frame, (self.width//2 - 300, 300), graph_alpha, progress)

        # Model architecture visualization
        if progress > 0.7:
            arch_alpha = min((progress - 0.7) / 0.3, 1.0)
            frame = self.draw_model_architecture(frame, (self.width//2 + 100, 350), arch_alpha)

        return frame

    def render_live_recognition_scene(self, frame, progress):
        """Render live recognition demonstration"""
        frame = self.create_gradient_background(frame, self.colors['secondary'], self.colors['accent'])

        # Title
        title = "📹 Live Iris Recognition"
        frame = self.draw_text(frame, title, (self.width//2, 80),
                             size=56, color=self.colors['text'], center=True, bold=True)

        # Camera feed simulation
        camera_x, camera_y = 200, 150
        camera_width, camera_height = 640, 480

        # Camera frame
        frame = self.draw_rounded_rect(frame, (camera_x, camera_y, camera_width, camera_height),
                                     '#000000', alpha=0.9, radius=10)

        # Simulated eye detection
        if progress > 0.3:
            eye_alpha = min((progress - 0.3) / 0.2, 1.0)

            # Draw simulated face/eye
            face_center = (camera_x + camera_width//2, camera_y + camera_height//2)

            # Face outline
            frame = self.draw_circle(frame, face_center, 120, self.colors['text_secondary'],
                                   alpha=eye_alpha * 0.5, thickness=2)

            # Eyes
            left_eye = (face_center[0] - 40, face_center[1] - 20)
            right_eye = (face_center[0] + 40, face_center[1] - 20)

            frame = self.draw_circle(frame, left_eye, 25, self.colors['success'],
                                   alpha=eye_alpha, thickness=3)
            frame = self.draw_circle(frame, right_eye, 25, self.colors['success'],
                                   alpha=eye_alpha, thickness=3)

            # Iris detection boxes
            if progress > 0.5:
                box_alpha = min((progress - 0.5) / 0.2, 1.0)
                frame = self.draw_detection_box(frame, left_eye, 60, box_alpha)
                frame = self.draw_detection_box(frame, right_eye, 60, box_alpha)

        # Recognition results panel
        if progress > 0.6:
            panel_alpha = min((progress - 0.6) / 0.3, 1.0)
            panel_x = camera_x + camera_width + 50
            panel_y = camera_y

            frame = self.draw_recognition_panel(frame, (panel_x, panel_y), panel_alpha, progress)

        return frame

    def render_voice_commands_scene(self, frame, progress):
        """Render voice commands demonstration"""
        frame = self.create_gradient_background(frame, self.colors['accent'], self.colors['primary'])

        # Title
        title = "🎤 Voice Commands"
        frame = self.draw_text(frame, title, (self.width//2, 80),
                             size=56, color=self.colors['text'], center=True, bold=True)

        # Microphone icon
        if progress > 0.2:
            mic_alpha = min((progress - 0.2) / 0.3, 1.0)
            frame = self.draw_microphone_icon(frame, (self.width//2, 250), mic_alpha, progress)

        # Voice commands list
        commands = [
            "🗣️ 'Start recognition'",
            "📸 'Take photo'",
            "🖼️ 'Show gallery'",
            "📊 'View analytics'",
            "🧠 'Train model'",
            "⚙️ 'Open settings'"
        ]

        for i, command in enumerate(commands):
            cmd_alpha = max(0, min((progress - 0.4 - i * 0.1) / 0.15, 1.0))
            if cmd_alpha > 0:
                y_pos = 400 + i * 60
                frame = self.draw_voice_command(frame, command, (self.width//2, y_pos), cmd_alpha)

        return frame

    def render_analytics_scene(self, frame, progress):
        """Render analytics dashboard"""
        frame = self.create_gradient_background(frame, self.colors['primary'], self.colors['secondary'])

        # Title
        title = "📊 Analytics Dashboard"
        frame = self.draw_text(frame, title, (self.width//2, 80),
                             size=56, color=self.colors['text'], center=True, bold=True)

        # Dashboard panels
        if progress > 0.2:
            # Accuracy metrics
            metrics_alpha = min((progress - 0.2) / 0.3, 1.0)
            frame = self.draw_metrics_panel(frame, (200, 200), metrics_alpha)

            # Performance graph
            if progress > 0.5:
                graph_alpha = min((progress - 0.5) / 0.3, 1.0)
                frame = self.draw_performance_graph(frame, (800, 200), graph_alpha)

            # System health
            if progress > 0.7:
                health_alpha = min((progress - 0.7) / 0.3, 1.0)
                frame = self.draw_system_health(frame, (500, 600), health_alpha)

        return frame

    def render_gallery_scene(self, frame, progress):
        """Render gallery demonstration"""
        frame = self.create_gradient_background(frame, self.colors['secondary'], self.colors['accent'])

        # Title
        title = "🖼️ Iris Gallery"
        frame = self.draw_text(frame, title, (self.width//2, 80),
                             size=56, color=self.colors['text'], center=True, bold=True)

        # Gallery grid
        if progress > 0.3:
            grid_alpha = min((progress - 0.3) / 0.4, 1.0)
            frame = self.draw_gallery_grid(frame, (self.width//2, 400), grid_alpha, progress)

        return frame

    def render_closing_scene(self, frame, progress):
        """Render closing scene"""
        frame = self.create_gradient_background(frame, self.colors['primary'], self.colors['secondary'])

        # Main message
        if progress > 0.2:
            msg_alpha = min((progress - 0.2) / 0.3, 1.0)
            title = "✨ Advanced Iris Recognition System"
            frame = self.draw_text(frame, title, (self.width//2, self.height//2 - 100),
                                 size=64, color=self.colors['text'], alpha=msg_alpha, center=True, bold=True)

            subtitle = "Ready for Production • 98%+ Accuracy • Real-time Performance"
            frame = self.draw_text(frame, subtitle, (self.width//2, self.height//2),
                                 size=32, color=self.colors['text_secondary'], alpha=msg_alpha, center=True)

        # Features summary
        if progress > 0.5:
            features_alpha = min((progress - 0.5) / 0.3, 1.0)
            features_text = "🧠 Deep Learning • 👁️ Live Recognition • 🎤 Voice Control • 📊 Analytics • 🖼️ Gallery"
            frame = self.draw_text(frame, features_text, (self.width//2, self.height//2 + 80),
                                 size=24, color=self.colors['success'], alpha=features_alpha, center=True)

        # Call to action
        if progress > 0.7:
            cta_alpha = min((progress - 0.7) / 0.3, 1.0)
            cta_text = "🚀 Start Your Biometric Journey Today!"
            frame = self.draw_text(frame, cta_text, (self.width//2, self.height//2 + 150),
                                 size=36, color=self.colors['warning'], alpha=cta_alpha, center=True, bold=True)

        return frame

    # ===== UTILITY DRAWING FUNCTIONS =====

    def create_gradient_background(self, frame, color1, color2):
        """Create a gradient background"""
        # Convert hex colors to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)

        # Create gradient
        for y in range(self.height):
            ratio = y / self.height
            r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
            g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
            b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
            frame[y, :] = [r, g, b]

        return frame

    def draw_text(self, frame, text, pos, size=24, color='#ffffff', alpha=1.0, center=False, bold=False):
        """Draw text on frame using OpenCV"""
        x, y = pos

        # Convert hex color to BGR
        def hex_to_bgr(hex_color):
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return rgb  # OpenCV uses RGB for putText in our case

        color_rgb = hex_to_bgr(color)

        # Font settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        if bold:
            font = cv2.FONT_HERSHEY_DUPLEX

        thickness = max(1, int(size / 12))
        scale = size / 30.0

        # Get text size for centering
        if center:
            (text_width, text_height), _ = cv2.getTextSize(text, font, scale, thickness)
            x = x - text_width // 2
            y = y + text_height // 2

        # Apply alpha blending if needed
        if alpha < 1.0:
            overlay = frame.copy()
            cv2.putText(overlay, text, (int(x), int(y)), font, scale, color_rgb, thickness)
            frame = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
        else:
            cv2.putText(frame, text, (int(x), int(y)), font, scale, color_rgb, thickness)

        return frame

    def draw_rounded_rect(self, frame, rect, color, alpha=1.0, radius=10):
        """Draw a rounded rectangle"""
        x, y, w, h = rect

        # Convert hex color to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        color_rgb = hex_to_rgb(color)

        # Create overlay for alpha blending
        overlay = frame.copy()

        # Draw rounded rectangle using multiple rectangles and circles
        # Main rectangle
        cv2.rectangle(overlay, (x + radius, y), (x + w - radius, y + h), color_rgb, -1)
        cv2.rectangle(overlay, (x, y + radius), (x + w, y + h - radius), color_rgb, -1)

        # Corner circles
        cv2.circle(overlay, (x + radius, y + radius), radius, color_rgb, -1)
        cv2.circle(overlay, (x + w - radius, y + radius), radius, color_rgb, -1)
        cv2.circle(overlay, (x + radius, y + h - radius), radius, color_rgb, -1)
        cv2.circle(overlay, (x + w - radius, y + h - radius), radius, color_rgb, -1)

        # Apply alpha blending
        if alpha < 1.0:
            frame = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
        else:
            frame = overlay

        return frame

    def draw_circle(self, frame, center, radius, color, alpha=1.0, thickness=1):
        """Draw a circle"""
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        color_rgb = hex_to_rgb(color)

        if alpha < 1.0:
            overlay = frame.copy()
            cv2.circle(overlay, center, radius, color_rgb, thickness)
            frame = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
        else:
            cv2.circle(frame, center, radius, color_rgb, thickness)

        return frame

    def draw_button(self, frame, text, pos, alpha):
        """Draw an animated button"""
        x, y = pos
        button_width, button_height = 180, 50

        # Button background
        frame = self.draw_rounded_rect(frame,
                                     (x - button_width//2, y - button_height//2, button_width, button_height),
                                     self.colors['secondary'], alpha=alpha * 0.9, radius=8)

        # Button border
        frame = self.draw_rounded_rect(frame,
                                     (x - button_width//2, y - button_height//2, button_width, button_height),
                                     self.colors['success'], alpha=alpha * 0.3, radius=8)

        # Button text
        frame = self.draw_text(frame, text, (x, y), size=16, color=self.colors['text'],
                             alpha=alpha, center=True)

        return frame

    # ===== SPECIALIZED DRAWING FUNCTIONS =====

    def draw_iris_icon(self, frame, pos, size=100, alpha=1.0, animated=False, progress=0):
        """Draw an animated iris icon"""
        x, y = pos

        # Outer circle (iris)
        frame = self.draw_circle(frame, (x, y), size//2, self.colors['success'], alpha=alpha, thickness=3)

        # Inner circle (pupil)
        pupil_size = int(size * 0.3)
        frame = self.draw_circle(frame, (x, y), pupil_size//2, self.colors['text'], alpha=alpha, thickness=2)

        if animated:
            # Animated iris patterns
            for i in range(8):
                angle = (i * 45 + progress * 360) % 360
                angle_rad = np.radians(angle)
                start_r = pupil_size // 2 + 5
                end_r = size // 2 - 5

                start_x = x + int(start_r * np.cos(angle_rad))
                start_y = y + int(start_r * np.sin(angle_rad))
                end_x = x + int(end_r * np.cos(angle_rad))
                end_y = y + int(end_r * np.sin(angle_rad))

                # Draw iris pattern lines
                overlay = frame.copy()
                cv2.line(overlay, (start_x, start_y), (end_x, end_y),
                        (0, 255, 136), 2)  # Green color for iris patterns
                frame = cv2.addWeighted(frame, 1 - alpha * 0.5, overlay, alpha * 0.5, 0)

        return frame

    def draw_detection_box(self, frame, center, size, alpha):
        """Draw an animated detection box"""
        x, y = center
        half_size = size // 2

        # Animated corners
        corner_length = 20
        thickness = 3

        # Top-left corner
        cv2.line(frame, (x - half_size, y - half_size),
                (x - half_size + corner_length, y - half_size),
                (0, 255, 0), thickness)
        cv2.line(frame, (x - half_size, y - half_size),
                (x - half_size, y - half_size + corner_length),
                (0, 255, 0), thickness)

        # Top-right corner
        cv2.line(frame, (x + half_size, y - half_size),
                (x + half_size - corner_length, y - half_size),
                (0, 255, 0), thickness)
        cv2.line(frame, (x + half_size, y - half_size),
                (x + half_size, y - half_size + corner_length),
                (0, 255, 0), thickness)

        # Bottom-left corner
        cv2.line(frame, (x - half_size, y + half_size),
                (x - half_size + corner_length, y + half_size),
                (0, 255, 0), thickness)
        cv2.line(frame, (x - half_size, y + half_size),
                (x - half_size, y + half_size - corner_length),
                (0, 255, 0), thickness)

        # Bottom-right corner
        cv2.line(frame, (x + half_size, y + half_size),
                (x + half_size - corner_length, y + half_size),
                (0, 255, 0), thickness)
        cv2.line(frame, (x + half_size, y + half_size),
                (x + half_size, y + half_size - corner_length),
                (0, 255, 0), thickness)

        return frame

    def draw_recognition_panel(self, frame, pos, alpha, progress):
        """Draw recognition results panel"""
        x, y = pos
        panel_width, panel_height = 400, 300

        # Panel background
        frame = self.draw_rounded_rect(frame, (x, y, panel_width, panel_height),
                                     self.colors['primary'], alpha=alpha * 0.9, radius=10)

        # Title
        frame = self.draw_text(frame, "🔍 Recognition Results", (x + 20, y + 30),
                             size=20, color=self.colors['text'], alpha=alpha, bold=True)

        # Results
        results = [
            "👤 Person ID: person_042",
            "🎯 Confidence: 97.8%",
            "⏱️ Processing: 234ms",
            "✅ Status: VERIFIED",
            "📊 Match Score: 0.978"
        ]

        for i, result in enumerate(results):
            result_alpha = max(0, min((progress - 0.7 - i * 0.05) / 0.1, 1.0)) * alpha
            if result_alpha > 0:
                frame = self.draw_text(frame, result, (x + 20, y + 80 + i * 35),
                                     size=16, color=self.colors['success'], alpha=result_alpha)

        return frame

    def draw_microphone_icon(self, frame, pos, alpha, progress):
        """Draw animated microphone icon"""
        x, y = pos

        # Microphone body
        mic_width, mic_height = 40, 60
        frame = self.draw_rounded_rect(frame,
                                     (x - mic_width//2, y - mic_height//2, mic_width, mic_height),
                                     self.colors['text'], alpha=alpha, radius=8)

        # Microphone stand
        cv2.line(frame, (x, y + mic_height//2), (x, y + mic_height//2 + 30),
                (255, 255, 255), 3)

        # Base
        cv2.line(frame, (x - 20, y + mic_height//2 + 30), (x + 20, y + mic_height//2 + 30),
                (255, 255, 255), 3)

        # Animated sound waves
        if progress > 0.5:
            wave_alpha = alpha * 0.7
            for i in range(3):
                radius = 60 + i * 25
                wave_progress = (progress * 3 + i) % 1.0
                wave_alpha_current = wave_alpha * (1 - wave_progress)

                frame = self.draw_circle(frame, (x, y), int(radius * wave_progress),
                                       self.colors['warning'], alpha=wave_alpha_current, thickness=2)

        return frame

    def draw_voice_command(self, frame, command, pos, alpha):
        """Draw a voice command with animation"""
        x, y = pos

        # Command background
        cmd_width = 600
        cmd_height = 40
        frame = self.draw_rounded_rect(frame,
                                     (x - cmd_width//2, y - cmd_height//2, cmd_width, cmd_height),
                                     self.colors['secondary'], alpha=alpha * 0.8, radius=8)

        # Command text
        frame = self.draw_text(frame, command, (x, y), size=24, color=self.colors['text'],
                             alpha=alpha, center=True)

        return frame

    # ===== PLACEHOLDER FUNCTIONS FOR COMPLEX VISUALIZATIONS =====

    def draw_training_graph(self, frame, pos, alpha, progress):
        """Draw a simplified training graph"""
        x, y = pos
        graph_width, graph_height = 500, 200

        # Graph background
        frame = self.draw_rounded_rect(frame, (x, y, graph_width, graph_height),
                                     self.colors['primary'], alpha=alpha * 0.9, radius=10)

        # Title
        frame = self.draw_text(frame, "📈 Training Accuracy", (x + 20, y + 30),
                             size=18, color=self.colors['text'], alpha=alpha, bold=True)

        # Simulated graph line
        points = []
        for i in range(0, graph_width - 40, 10):
            # Simulate accuracy curve
            accuracy = 0.5 + 0.45 * (1 - np.exp(-i / 100))
            point_y = y + graph_height - 40 - int(accuracy * (graph_height - 80))
            points.append((x + 20 + i, point_y))

        # Draw line
        for i in range(len(points) - 1):
            cv2.line(frame, points[i], points[i + 1], (0, 255, 136), 2)

        return frame

    def draw_model_architecture(self, frame, pos, alpha):
        """Draw simplified model architecture"""
        x, y = pos

        # Architecture blocks
        blocks = [
            {"name": "Input", "size": (80, 40), "color": self.colors['text_secondary']},
            {"name": "Conv2D", "size": (100, 50), "color": self.colors['success']},
            {"name": "ResNet", "size": (120, 60), "color": self.colors['warning']},
            {"name": "Dense", "size": (100, 50), "color": self.colors['success']},
            {"name": "Output", "size": (80, 40), "color": self.colors['text_secondary']}
        ]

        for i, block in enumerate(blocks):
            block_x = x + i * 140
            block_y = y
            w, h = block['size']

            # Draw block
            frame = self.draw_rounded_rect(frame, (block_x - w//2, block_y - h//2, w, h),
                                         block['color'], alpha=alpha * 0.8, radius=5)

            # Block label
            frame = self.draw_text(frame, block['name'], (block_x, block_y),
                                 size=14, color=self.colors['text'], alpha=alpha, center=True)

            # Arrow to next block
            if i < len(blocks) - 1:
                arrow_start = (block_x + w//2, block_y)
                arrow_end = (block_x + 140 - blocks[i+1]['size'][0]//2, block_y)
                cv2.arrowedLine(frame, arrow_start, arrow_end, (255, 255, 255), 2)

        return frame

    def draw_metrics_panel(self, frame, pos, alpha):
        """Draw metrics panel"""
        x, y = pos
        panel_width, panel_height = 350, 250

        # Panel background
        frame = self.draw_rounded_rect(frame, (x, y, panel_width, panel_height),
                                     self.colors['primary'], alpha=alpha * 0.9, radius=10)

        # Title
        frame = self.draw_text(frame, "📊 Performance Metrics", (x + 20, y + 30),
                             size=18, color=self.colors['text'], alpha=alpha, bold=True)

        # Metrics
        metrics = [
            "🎯 Accuracy: 98.2%",
            "⚡ Speed: 234ms",
            "👥 Users: 108",
            "✅ Success Rate: 97.8%",
            "🔄 Uptime: 99.9%"
        ]

        for i, metric in enumerate(metrics):
            frame = self.draw_text(frame, metric, (x + 20, y + 70 + i * 30),
                                 size=16, color=self.colors['success'], alpha=alpha)

        return frame

    def draw_performance_graph(self, frame, pos, alpha):
        """Draw performance graph"""
        x, y = pos
        graph_width, graph_height = 400, 200

        # Graph background
        frame = self.draw_rounded_rect(frame, (x, y, graph_width, graph_height),
                                     self.colors['primary'], alpha=alpha * 0.9, radius=10)

        # Title
        frame = self.draw_text(frame, "📈 Recognition Performance", (x + 20, y + 30),
                             size=18, color=self.colors['text'], alpha=alpha, bold=True)

        # Simple bar chart simulation
        bars = [85, 92, 97, 98, 96]
        bar_width = 50
        for i, height in enumerate(bars):
            bar_x = x + 50 + i * 70
            bar_height = int(height * 1.2)
            bar_y = y + graph_height - 40 - bar_height

            frame = self.draw_rounded_rect(frame, (bar_x, bar_y, bar_width, bar_height),
                                         self.colors['success'], alpha=alpha * 0.8, radius=3)

            # Bar label
            frame = self.draw_text(frame, f"{height}%", (bar_x + bar_width//2, bar_y - 10),
                                 size=12, color=self.colors['text'], alpha=alpha, center=True)

        return frame

    def draw_system_health(self, frame, pos, alpha):
        """Draw system health indicators"""
        x, y = pos

        # Health indicators
        indicators = [
            {"name": "🖥️ CPU", "value": "45%", "color": self.colors['success']},
            {"name": "💾 Memory", "value": "62%", "color": self.colors['warning']},
            {"name": "🌡️ Temperature", "value": "68°C", "color": self.colors['success']},
            {"name": "📡 Network", "value": "Online", "color": self.colors['success']}
        ]

        for i, indicator in enumerate(indicators):
            ind_x = x + (i % 2) * 200
            ind_y = y + (i // 2) * 60

            # Indicator background
            frame = self.draw_rounded_rect(frame, (ind_x, ind_y, 180, 40),
                                         self.colors['secondary'], alpha=alpha * 0.8, radius=5)

            # Indicator text
            frame = self.draw_text(frame, f"{indicator['name']} {indicator['value']}",
                                 (ind_x + 10, ind_y + 25), size=14,
                                 color=indicator['color'], alpha=alpha)

        return frame

    def draw_gallery_grid(self, frame, pos, alpha, progress):
        """Draw gallery grid simulation"""
        x, y = pos

        # Grid of iris images (simulated)
        grid_size = 4
        image_size = 80
        spacing = 20

        for row in range(grid_size):
            for col in range(grid_size):
                img_x = x - (grid_size * (image_size + spacing)) // 2 + col * (image_size + spacing)
                img_y = y - (grid_size * (image_size + spacing)) // 2 + row * (image_size + spacing)

                # Image placeholder
                frame = self.draw_rounded_rect(frame, (img_x, img_y, image_size, image_size),
                                             self.colors['secondary'], alpha=alpha * 0.8, radius=5)

                # Simulated iris in image
                iris_center = (img_x + image_size//2, img_y + image_size//2)
                frame = self.draw_circle(frame, iris_center, 25, self.colors['success'],
                                       alpha=alpha * 0.6, thickness=2)
                frame = self.draw_circle(frame, iris_center, 10, self.colors['text'],
                                       alpha=alpha * 0.6, thickness=1)

        return frame


# ===== MAIN EXECUTION =====

def main():
    """Main function to create the animation video"""
    print("🎬 Iris Recognition Project Animation Creator")
    print("=" * 50)

    # Create animator
    animator = IrisProjectAnimator()

    # Create video
    success = animator.create_video()

    if success:
        print("\n🎉 Animation video created successfully!")
        print("📁 Output file: iris_recognition_demo.mp4")
        print("\n📋 Video Details:")
        print(f"   📐 Resolution: {animator.width}x{animator.height}")
        print(f"   🎞️ Frame Rate: {animator.fps} FPS")
        print(f"   ⏱️ Duration: {animator.duration} seconds")
        print(f"   📊 Total Frames: {animator.duration * animator.fps}")
        print("\n✨ Features Showcased:")
        print("   🧠 Deep Learning Model Training")
        print("   👁️ Live Iris Recognition")
        print("   🎤 Voice Commands")
        print("   📊 Analytics Dashboard")
        print("   🖼️ Gallery Features")
        print("   💻 Modern GUI Interface")
        print("\n🚀 Ready to share your amazing project!")
    else:
        print("❌ Failed to create animation video")
        return False

    return True

if __name__ == "__main__":
    main()
