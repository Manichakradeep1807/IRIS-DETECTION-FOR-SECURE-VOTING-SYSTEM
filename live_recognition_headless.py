#!/usr/bin/env python3
"""
Headless Live Recognition with Iris Capture
Works without GUI display - captures and saves iris images
"""

import cv2
import numpy as np
import time
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HeadlessIrisCapture:
    """
    Headless iris capture system that works without GUI
    """
    
    def __init__(self):
        self.capture_folder = "captured_iris"
        self.captured_count = 0
        self.total_frames = 0
        
        # Create capture folder
        if not os.path.exists(self.capture_folder):
            os.makedirs(self.capture_folder)
            
        # Load cascades
        try:
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            logger.info("Cascade classifiers loaded successfully")
        except Exception as e:
            logger.error("Error loading cascades: {}".format(e))
            self.eye_cascade = None
            self.face_cascade = None
    
    def detect_eyes(self, frame):
        """Detect eyes in frame"""
        if not self.eye_cascade:
            return []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # First detect faces
        if self.face_cascade:
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            eyes = []
            for (fx, fy, fw, fh) in faces:
                face_roi = gray[fy:fy+fh, fx:fx+fw]
                face_eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
                
                for (ex, ey, ew, eh) in face_eyes:
                    eyes.append((fx + ex, fy + ey, ew, eh))
            
            return eyes
        else:
            return self.eye_cascade.detectMultiScale(gray, 1.3, 5)
    
    def extract_iris_from_roi(self, eye_roi):
        """Extract iris features from eye region"""
        try:
            # Resize for better processing
            if eye_roi.shape[0] < 100 or eye_roi.shape[1] < 100:
                eye_roi = cv2.resize(eye_roi, (150, 150))
            
            # Convert to grayscale
            gray = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY) if len(eye_roi.shape) == 3 else eye_roi
            
            # Enhance contrast
            gray = cv2.equalizeHist(gray)
            gray = cv2.medianBlur(gray, 5)
            
            # Detect circles (iris/pupil)
            circles = cv2.HoughCircles(
                gray,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=int(gray.shape[0]/4),
                param1=50,
                param2=30,
                minRadius=int(gray.shape[0]/8),
                maxRadius=int(gray.shape[0]/3)
            )
            
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                
                # Find best circle
                best_circle = None
                max_radius = 0
                
                for (x, y, r) in circles:
                    if r > max_radius and x-r > 0 and y-r > 0 and x+r < gray.shape[1] and y+r < gray.shape[0]:
                        max_radius = r
                        best_circle = (x, y, r)
                
                if best_circle is not None:
                    x, y, r = best_circle
                    
                    # Create mask for iris region
                    mask = np.zeros(gray.shape, np.uint8)
                    cv2.circle(mask, (x, y), r, 255, -1)
                    
                    # Extract iris region
                    iris_region = cv2.bitwise_and(gray, gray, mask=mask)
                    
                    # Crop to bounding box
                    crop_x = max(0, x - r)
                    crop_y = max(0, y - r)
                    crop_w = min(gray.shape[1] - crop_x, 2 * r)
                    crop_h = min(gray.shape[0] - crop_y, 2 * r)
                    
                    cropped_iris = iris_region[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
                    
                    if cropped_iris.size > 0:
                        cropped_iris = cv2.resize(cropped_iris, (64, 64))
                        
                        # Convert back to color
                        if len(cropped_iris.shape) == 2:
                            cropped_iris = cv2.cvtColor(cropped_iris, cv2.COLOR_GRAY2BGR)
                        
                        return cropped_iris
            
            # If no iris detected, return resized eye region
            eye_roi_resized = cv2.resize(eye_roi, (64, 64))
            if len(eye_roi_resized.shape) == 2:
                eye_roi_resized = cv2.cvtColor(eye_roi_resized, cv2.COLOR_GRAY2BGR)
            
            return eye_roi_resized
            
        except Exception as e:
            logger.error("Error extracting iris: {}".format(e))
            return None
    
    def capture_iris_image(self, iris_image, eye_roi, person_id=1, confidence=0.85):
        """Capture and save iris image"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%')[:-3]
            
            # Create composite image
            composite_height = max(eye_roi.shape[0], iris_image.shape[0]) + 60
            composite_width = eye_roi.shape[1] + iris_image.shape[1] + 30
            composite = np.zeros((composite_height, composite_width, 3), dtype=np.uint8)
            
            # Add eye region
            eye_y_offset = 30
            composite[eye_y_offset:eye_y_offset+eye_roi.shape[0], 0:eye_roi.shape[1]] = eye_roi
            
            # Add iris image
            iris_x_offset = eye_roi.shape[1] + 10
            iris_y_offset = 30
            composite[iris_y_offset:iris_y_offset+iris_image.shape[0],
                     iris_x_offset:iris_x_offset+iris_image.shape[1]] = iris_image
            
            # Add text labels
            cv2.putText(composite, "Person {} - Confidence: {}".format(person_id),
                       (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(composite, "Eye Region", (10, eye_y_offset + eye_roi.shape[0] + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(composite, "Extracted Iris", (iris_x_offset, iris_y_offset + iris_image.shape[0] + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Save the composite image
            filename = "{}/iris_person{person_id}_{timestamp}.jpg".format(self.capture_folder)
            cv2.imwrite(filename, composite)
            
            self.captured_count += 1
            print("📸 Iris captured #{}: Person {person_id} (Confidence: {confidence:.2f})".format(self.captured_count))
            print("   Saved: {}".format(filename))
            
            return filename
            
        except Exception as e:
            logger.error("Error capturing iris image: {}".format(e))
            return None
    
    def run_capture_demo(self, duration=30):
        """Run headless capture demo"""
        print("🚀 Starting Headless Iris Capture Demo")
        print("=" * 50)
        print("Duration: {} seconds".format(duration))
        print("Features:")
        print("   📸 Automatic iris detection and capture")
        print("   💾 Saves composite images to captured_iris/ folder")
        print("   🔍 Works without GUI display")
        print()
        
        # Initialize camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Camera not accessible")
            return False
        
        print("✅ Camera initialized")
        print("📹 Starting capture...")
        
        start_time = time.time()
        last_capture_time = 0
        capture_cooldown = 3.0  # Capture every 3 seconds max
        
        try:
            while time.time() - start_time < duration:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                self.total_frames += 1
                
                # Detect eyes
                eyes = self.detect_eyes(frame)
                
                if eyes and time.time() - last_capture_time > capture_cooldown:
                    for (x, y, w, h) in eyes[:1]:  # Process first eye only
                        # Extract eye region
                        eye_roi = frame[y:y+h, x:x+w]
                        
                        if eye_roi.size == 0:
                            continue
                        
                        # Extract iris
                        iris_features = self.extract_iris_from_roi(eye_roi)
                        
                        if iris_features is not None:
                            # Simulate recognition (random person ID and confidence)
                            person_id = np.random.randint(1, 6)  # Random person 1-5
                            confidence = np.random.uniform(0.7, 0.95)  # Random confidence
                            
                            # Capture the iris image
                            filename = self.capture_iris_image(iris_features, eye_roi, person_id, confidence)
                            
                            if filename:
                                last_capture_time = time.time()
                                break
                
                # Show progress every 5 seconds
                elapsed = time.time() - start_time
                if int(elapsed) % 5 == 0 and elapsed > 0:
                    remaining = duration - elapsed
                    print("⏱️  Progress: {}s elapsed, {remaining:.0f}s remaining, {self.captured_count} captures".format(elapsed:.0f))
                    time.sleep(1)  # Prevent multiple prints
        
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
        
        finally:
            cap.release()
        
        print(f"\n📊 Demo Results:")
        print("   Total frames processed: {}".format(self.total_frames))
        print("   Iris images captured: {}".format(self.captured_count))
        print("   Images saved in: {}/".format(self.capture_folder))
        
        # List captured files
        if os.path.exists(self.capture_folder):
            files = [f for f in os.listdir(self.capture_folder) if f.endswith('.format(confidence:.2f).jpg')]
            if files:
                print(f"\n📁 Captured files:")
                for filename in sorted(files)[-5:]:  # Show last 5
                    filepath = os.path.join(self.capture_folder, filename)
                    size = os.path.getsize(filepath)
                    print("     {} ({size} bytes)".format(filename))
        
        return True

def main():
    """Main function"""
    print("👁️ HEADLESS IRIS CAPTURE DEMO")
    print("=" * 50)
    print("This demo runs iris capture without GUI display")
    print("Perfect for environments where OpenCV GUI is not available")
    print()
    
    # Create capture system
    capture_system = HeadlessIrisCapture()
    
    # Run demo
    duration = 20  # Run for 20 seconds
    success = capture_system.run_capture_demo(duration)
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("\n💡 The iris capture features work even without GUI display")
        print("   All captured images are saved to the captured_iris/ folder")
    else:
        print("\n❌ Demo failed - check error messages above")

if __name__ == "__main__":
    main()
