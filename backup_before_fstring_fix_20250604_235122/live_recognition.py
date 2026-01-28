"""
Live Video Iris Recognition System
Real-time iris detection and recognition from webcam feed
"""

import cv2
import numpy as np
import threading
import time
from datetime import datetime
from tkinter import messagebox
import queue
import logging

# Import our modules
try:
    from performance_monitor import monitor_recognition
    from database_manager import db
    ENHANCED_FEATURES = True
except ImportError:
    ENHANCED_FEATURES = False

logger = logging.getLogger(__name__)

class LiveIrisRecognition:
    """
    Real-time iris recognition system using webcam
    """
    
    def __init__(self, model=None, iris_extractor=None):
        self.model = model
        self.iris_extractor = iris_extractor
        self.is_running = False
        self.cap = None
        self.recognition_thread = None
        self.frame_queue = queue.Queue(maxsize=10)
        self.result_queue = queue.Queue()

        # Recognition parameters
        self.confidence_threshold = 0.7
        self.recognition_cooldown = 2.0  # seconds between recognitions
        self.last_recognition_time = 0

        # Statistics
        self.total_frames = 0
        self.successful_detections = 0
        self.successful_recognitions = 0

        # Image capture and display
        self.captured_images = []  # Store captured iris images
        self.current_iris_image = None  # Current iris image being displayed
        self.show_iris_window = True  # Whether to show iris capture window
        self.show_gallery_window = True  # Whether to show gallery window
        self.max_captured_images = 50  # Maximum number of images to keep
        self.capture_folder = "captured_iris"  # Folder to save captured images

        # Gallery display settings
        self.gallery_grid_cols = 4  # Number of columns in gallery
        self.gallery_image_size = 150  # Size of each image in gallery
        self.gallery_update_interval = 15  # Update gallery every N frames (faster updates)
        self.frame_count_since_gallery_update = 0

        # Enhanced gallery features
        self.auto_open_gallery = True  # Automatically open gallery when first image is captured
        self.gallery_opened = False  # Track if gallery has been opened
        self.show_detailed_analysis = True  # Show detailed analysis in gallery
        self.gallery_analysis_mode = True  # Enhanced analysis mode for gallery

        # Create capture folder if it doesn't exist
        import os
        if not os.path.exists(self.capture_folder):
            os.makedirs(self.capture_folder)
        
        # Load face cascade for eye detection
        try:
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except Exception as e:
            logger.warning(f"Could not load cascade classifiers: {e}")
            self.eye_cascade = None
            self.face_cascade = None
    
    def start_recognition(self):
        """Start live recognition"""
        if self.is_running:
            return False
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Could not open camera")
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.is_running = True
        
        # Start recognition thread
        self.recognition_thread = threading.Thread(target=self._recognition_worker)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()
        
        # Start main loop
        self._main_loop()
        
        return True
    
    def stop_recognition(self):
        """Stop live recognition"""
        self.is_running = False

        if self.cap:
            self.cap.release()

        # Close all OpenCV windows (handle GUI issues gracefully)
        try:
            cv2.destroyAllWindows()
        except Exception as e:
            logger.warning(f"Could not close windows (headless mode): {e}")

        if self.recognition_thread and self.recognition_thread.is_alive():
            self.recognition_thread.join(timeout=2.0)

        # Print summary of captured images
        if self.captured_images:
            print(f"\n📸 Session Summary: {len(self.captured_images)} iris images captured")
            print(f"   Images saved in: {self.capture_folder}/")
            print("   Gallery window showed real-time updates during capture")
            print("   Use 'c' key during live recognition to view captured images")
    
    def _main_loop(self):
        """Main video capture and display loop"""
        consecutive_failures = 0
        max_failures = 10

        try:
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    consecutive_failures += 1
                    logger.warning(f"Failed to read frame (attempt {consecutive_failures})")
                    if consecutive_failures >= max_failures:
                        logger.error("Too many consecutive frame read failures")
                        break
                    time.sleep(0.1)  # Brief pause before retry
                    continue

                consecutive_failures = 0  # Reset on successful read
                self.total_frames += 1

                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)

                # Add frame to processing queue (non-blocking)
                if not self.frame_queue.full():
                    self.frame_queue.put(frame.copy())

                # Check for recognition results
                try:
                    while not self.result_queue.empty():
                        result = self.result_queue.get_nowait()
                        self._display_result(frame, result)
                except queue.Empty:
                    pass
                except Exception as e:
                    logger.error(f"Error processing recognition result: {e}")

                # Detect and highlight eyes
                try:
                    self._detect_and_highlight_eyes(frame)
                except Exception as e:
                    logger.error(f"Error in eye detection: {e}")

                # Add overlay information
                try:
                    self._add_overlay_info(frame)
                except Exception as e:
                    logger.error(f"Error adding overlay: {e}")

                # Display frame (with fallback for environments without GUI)
                display_available = True
                try:
                    cv2.imshow('Live Iris Recognition', frame)
                except Exception as e:
                    display_available = False
                    logger.warning(f"Display not available (headless mode): {e}")
                    # Continue without display - just process frames
                    print(f"📹 Frame {self.total_frames} processed (headless mode)")
                    if self.total_frames % 30 == 0:  # Print every 30 frames
                        print(f"   📊 Stats: {self.successful_detections} detections, {self.successful_recognitions} recognitions")

                    # Save frame periodically in headless mode
                    if self.total_frames % 60 == 0:  # Save every 60 frames
                        frame_filename = f"live_frame_{self.total_frames}.jpg"
                        cv2.imwrite(frame_filename, frame)
                        print(f"   💾 Frame saved: {frame_filename}")

                # Check for exit (handle both GUI and headless modes)
                if display_available:
                    try:
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q') or key == 27:  # 'q' or ESC
                            logger.info("User requested exit via keyboard")
                            break
                        elif key == ord('s'):  # 's' for screenshot
                            try:
                                self._save_screenshot(frame)
                            except Exception as e:
                                logger.error(f"Error saving screenshot: {e}")
                        elif key == ord('r'):  # 'r' for reset stats
                            try:
                                self._reset_statistics()
                            except Exception as e:
                                logger.error(f"Error resetting statistics: {e}")
                        elif key == ord('i'):  # 'i' for toggle iris window
                            try:
                                self._toggle_iris_window()
                            except Exception as e:
                                logger.error(f"Error toggling iris window: {e}")
                        elif key == ord('c'):  # 'c' for view captured images
                            try:
                                self._show_captured_images()
                            except Exception as e:
                                logger.error(f"Error showing captured images: {e}")
                        elif key == ord('g'):  # 'g' for toggle gallery window
                            try:
                                self._toggle_gallery_window()
                            except Exception as e:
                                logger.error(f"Error toggling gallery window: {e}")
                        elif key == ord('f'):  # 'f' for force enhanced gallery update
                            try:
                                if len(self.captured_images) > 0:
                                    self._update_enhanced_gallery_window()
                                    print("🔄 Enhanced gallery refreshed manually")
                            except Exception as e:
                                logger.error(f"Error forcing enhanced gallery update: {e}")
                    except Exception as key_error:
                        logger.warning(f"Keyboard input not available: {key_error}")
                else:
                    # In headless mode, run for a limited time or until interrupted
                    if self.total_frames > 300:  # Stop after ~10 seconds at 30fps
                        logger.info("Headless mode: stopping after processing frames")
                        break

                # Update iris display window
                if self.show_iris_window and self.current_iris_image is not None:
                    try:
                        self._update_iris_display()
                    except Exception as e:
                        logger.error(f"Error updating iris display: {e}")

                # Update enhanced gallery window periodically
                self.frame_count_since_gallery_update += 1
                if (self.show_gallery_window and
                    self.frame_count_since_gallery_update >= self.gallery_update_interval and
                    len(self.captured_images) > 0):
                    try:
                        self._update_enhanced_gallery_window()
                        self.frame_count_since_gallery_update = 0
                    except Exception as e:
                        logger.error(f"Error updating enhanced gallery window: {e}")

        except Exception as e:
            logger.error(f"Critical error in main loop: {e}")
        finally:
            self.stop_recognition()
    
    def _recognition_worker(self):
        """Background thread for iris recognition"""
        while self.is_running:
            try:
                # Get frame from queue
                frame = self.frame_queue.get(timeout=1.0)
                
                # Check cooldown
                current_time = time.time()
                if current_time - self.last_recognition_time < self.recognition_cooldown:
                    continue
                
                # Process frame for iris recognition
                result = self._process_frame_for_recognition(frame)
                
                if result:
                    self.last_recognition_time = current_time
                    self.result_queue.put(result)
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in recognition worker: {e}")
    
    def _process_frame_for_recognition(self, frame):
        """Process frame for iris recognition"""
        if not self.model or not self.iris_extractor:
            return None
        
        try:
            # Detect eyes in frame
            eyes = self._detect_eyes(frame)
            
            if not eyes:
                return None
            
            best_result = None
            best_confidence = 0
            
            for (x, y, w, h) in eyes:
                # Extract eye region
                eye_roi = frame[y:y+h, x:x+w]
                
                if eye_roi.size == 0:
                    continue
                
                # Extract iris features
                iris_features = self._extract_iris_from_roi(eye_roi)

                if iris_features is not None:
                    self.successful_detections += 1

                    # Perform recognition
                    prediction = self._recognize_iris(iris_features)

                    if prediction and prediction['confidence'] > self.confidence_threshold:
                        if prediction['confidence'] > best_confidence:
                            best_confidence = prediction['confidence']
                            best_result = {
                                'person_id': prediction['person_id'],
                                'confidence': prediction['confidence'],
                                'eye_region': (x, y, w, h),
                                'timestamp': datetime.now(),
                                'iris_image': iris_features.copy(),  # Store the iris image
                                'eye_roi': eye_roi.copy()  # Store the full eye region
                            }

                            # Capture and save the iris image
                            self._capture_iris_image(iris_features, eye_roi, prediction)
            
            if best_result:
                self.successful_recognitions += 1
                
                # Log to database if enhanced features available
                if ENHANCED_FEATURES:
                    try:
                        db.log_access(
                            person_id=best_result['person_id'],
                            access_type='live_recognition',
                            confidence_score=best_result['confidence'],
                            access_granted=True,
                            location='Live Camera',
                            device_id='webcam_0'
                        )
                    except Exception as e:
                        logger.error(f"Error logging to database: {e}")
            
            return best_result
            
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return None
    
    def _detect_eyes(self, frame):
        """Detect eyes in frame using cascade classifiers"""
        if not self.eye_cascade:
            return []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # First detect faces to improve eye detection
        if self.face_cascade:
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            eyes = []
            for (fx, fy, fw, fh) in faces:
                # Look for eyes within face region
                face_roi = gray[fy:fy+fh, fx:fx+fw]
                face_eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
                
                # Convert coordinates back to full frame
                for (ex, ey, ew, eh) in face_eyes:
                    eyes.append((fx + ex, fy + ey, ew, eh))
            
            return eyes
        else:
            # Detect eyes directly
            return self.eye_cascade.detectMultiScale(gray, 1.3, 5)
    
    def _extract_iris_from_roi(self, eye_roi):
        """Extract iris features from eye region - ENHANCED VERSION"""
        try:
            # Resize eye region for better processing
            if eye_roi.shape[0] < 100 or eye_roi.shape[1] < 100:
                eye_roi = cv2.resize(eye_roi, (150, 150))

            # Convert to grayscale for circle detection
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

                # Find the best circle
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
                        # Resize to standard size
                        cropped_iris = cv2.resize(cropped_iris, (64, 64))

                        # Convert back to color for model compatibility
                        if len(cropped_iris.shape) == 2:
                            cropped_iris = cv2.cvtColor(cropped_iris, cv2.COLOR_GRAY2BGR)

                        return cropped_iris

            # If no iris detected, return resized eye region
            eye_roi_resized = cv2.resize(eye_roi, (64, 64))
            if len(eye_roi_resized.shape) == 2:
                eye_roi_resized = cv2.cvtColor(eye_roi_resized, cv2.COLOR_GRAY2BGR)

            return eye_roi_resized

        except Exception as e:
            logger.error(f"Error extracting iris: {e}")
            return None
    
    @monitor_recognition
    def _recognize_iris(self, iris_features):
        """Recognize iris using trained model"""
        if not self.model:
            return None
        
        try:
            # Preprocess features
            img = cv2.resize(iris_features, (64, 64))
            img = np.array(img).reshape(1, 64, 64, 3)
            img = img.astype('float32') / 255.0
            
            # Predict
            predictions = self.model.predict(img, verbose=0)
            person_id = np.argmax(predictions) + 1
            confidence = float(np.max(predictions))
            
            return {
                'person_id': person_id,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error in recognition: {e}")
            return None
    
    def _detect_and_highlight_eyes(self, frame):
        """Detect and highlight eyes in frame"""
        eyes = self._detect_eyes(frame)
        
        for (x, y, w, h) in eyes:
            # Draw rectangle around eye
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Add label
            cv2.putText(frame, 'Eye', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    def _display_result(self, frame, result):
        """Display recognition result on frame"""
        if not result:
            return
        
        x, y, w, h = result['eye_region']
        person_id = result['person_id']
        confidence = result['confidence']
        
        # Draw recognition box
        color = (0, 255, 0) if confidence > 0.8 else (0, 255, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
        
        # Add recognition text
        text = f"Person {person_id}: {confidence:.2f}"
        cv2.putText(frame, text, (x, y-30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Add timestamp
        time_text = result['timestamp'].strftime('%H:%M:%S')
        cv2.putText(frame, time_text, (x, y+h+20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    def _add_overlay_info(self, frame):
        """Add overlay information to frame"""
        h, w = frame.shape[:2]
        
        # Statistics
        stats_text = [
            f"Frames: {self.total_frames}",
            f"Detections: {self.successful_detections}",
            f"Recognitions: {self.successful_recognitions}",
            f"Success Rate: {(self.successful_recognitions/max(1, self.successful_detections)*100):.1f}%"
        ]
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw text
        for i, text in enumerate(stats_text):
            cv2.putText(frame, text, (20, 35 + i*20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Instructions
        instructions = [
            "Press 'q' or ESC to quit",
            "Press 's' for screenshot",
            "Press 'r' to reset stats",
            "Press 'i' to toggle iris window",
            "Press 'c' to view captured images",
            "Press 'g' to toggle ENHANCED gallery",
            "Press 'f' to refresh gallery"
        ]
        
        for i, text in enumerate(instructions):
            cv2.putText(frame, text, (w-250, h-60 + i*15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    def _save_screenshot(self, frame):
        """Save screenshot with timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"screenshot_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Screenshot saved: {filename}")

    def _reset_statistics(self):
        """Reset recognition statistics"""
        self.total_frames = 0
        self.successful_detections = 0
        self.successful_recognitions = 0
        print("Statistics reset")

    def _sync_to_dataset(self, filename, person_id):
        """Automatically sync captured image to sample dataset folder"""
        try:
            import shutil
            import os
            dataset_folder = "sample_dataset"

            # Ensure dataset folder exists
            os.makedirs(dataset_folder, exist_ok=True)

            # Create person folder in dataset
            person_folder = f"{dataset_folder}/person_{str(person_id).zfill(3)}"
            os.makedirs(person_folder, exist_ok=True)

            # Count existing samples in person folder
            existing_samples = len([f for f in os.listdir(person_folder)
                                  if f.startswith('sample_') and f.endswith('.jpg')])

            # Copy image to dataset with sample naming
            sample_filename = f"sample_{existing_samples + 1}.jpg"
            dest_path = os.path.join(person_folder, sample_filename)

            # Only copy if not already exists
            if not os.path.exists(dest_path):
                shutil.copy2(filename, dest_path)
                print(f"📁 Auto-synced to dataset: {dest_path}")
                return True
            return False

        except Exception as e:
            print(f"Error syncing to dataset: {e}")
            return False

    def _capture_iris_image(self, iris_image, eye_roi, prediction):
        """Capture and save iris image when recognition occurs"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # Include milliseconds
            person_id = prediction['person_id']
            confidence = prediction['confidence']

            # Create a composite image showing both eye region and extracted iris
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
            cv2.putText(composite, f"Person {person_id} - Confidence: {confidence:.2f}",
                       (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(composite, "Eye Region", (10, eye_y_offset + eye_roi.shape[0] + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(composite, "Extracted Iris", (iris_x_offset, iris_y_offset + iris_image.shape[0] + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Save the composite image
            filename = f"{self.capture_folder}/iris_person{person_id}_{timestamp}.jpg"
            cv2.imwrite(filename, composite)

            # Auto-sync to dataset folder
            try:
                self._sync_to_dataset(filename, person_id)
            except Exception as e:
                print(f"Warning: Could not auto-sync to dataset: {e}")

            # Calculate additional analysis metrics
            analysis_data = self._calculate_image_analysis(iris_image, eye_roi, confidence)

            # Store in memory for display with enhanced analysis
            capture_data = {
                'composite': composite,
                'iris_image': iris_image,
                'eye_roi': eye_roi,
                'person_id': person_id,
                'confidence': confidence,
                'timestamp': timestamp,
                'filename': filename,
                'analysis': analysis_data,  # Enhanced analysis data
                'capture_time': datetime.now(),  # Full datetime object
                'session_number': len(self.captured_images) + 1  # Image number in session
            }

            self.captured_images.append(capture_data)

            # Keep only the most recent images
            if len(self.captured_images) > self.max_captured_images:
                self.captured_images.pop(0)

            # Update current display
            self.current_iris_image = capture_data

            # Auto-open gallery window on first capture
            if self.auto_open_gallery and not self.gallery_opened and len(self.captured_images) == 1:
                self.gallery_opened = True
                print("🖼️ Auto-opening gallery window for real-time viewing...")
                self._update_enhanced_gallery_window()

            # Force immediate gallery update for real-time feedback
            if self.show_gallery_window:
                self._update_enhanced_gallery_window()

            print(f"📸 Iris captured: Person {person_id} (Confidence: {confidence:.2f}) -> {filename}")
            print(f"   📊 Quality: {analysis_data['quality_score']:.1f}% | Size: {analysis_data['file_size_kb']:.1f}KB")

        except Exception as e:
            logger.error(f"Error capturing iris image: {e}")

    def _calculate_image_analysis(self, iris_image, eye_roi, confidence):
        """Calculate detailed analysis metrics for captured image"""
        try:
            # Basic metrics
            iris_height, iris_width = iris_image.shape[:2]
            eye_height, eye_width = eye_roi.shape[:2]

            # Quality score based on multiple factors
            size_score = min(100, (iris_width * iris_height) / 40.96)  # Normalize to 64x64 = 100%
            confidence_score = confidence * 100
            clarity_score = self._calculate_image_clarity(iris_image)

            quality_score = (size_score * 0.3 + confidence_score * 0.5 + clarity_score * 0.2)

            # File size estimation (before actual file creation)
            estimated_file_size = (iris_width * iris_height * 3 * 0.1) / 1024  # Rough JPEG compression estimate

            analysis_data = {
                'quality_score': quality_score,
                'iris_dimensions': f"{iris_width}x{iris_height}",
                'eye_dimensions': f"{eye_width}x{eye_height}",
                'clarity_score': clarity_score,
                'confidence_score': confidence_score,
                'size_score': size_score,
                'file_size_kb': estimated_file_size,
                'pixel_count': iris_width * iris_height,
                'aspect_ratio': iris_width / iris_height if iris_height > 0 else 1.0
            }

            return analysis_data

        except Exception as e:
            logger.error(f"Error calculating image analysis: {e}")
            return {
                'quality_score': confidence * 100,
                'iris_dimensions': "Unknown",
                'eye_dimensions': "Unknown",
                'clarity_score': 50.0,
                'confidence_score': confidence * 100,
                'size_score': 50.0,
                'file_size_kb': 10.0,
                'pixel_count': 0,
                'aspect_ratio': 1.0
            }

    def _calculate_image_clarity(self, image):
        """Calculate image clarity/sharpness score"""
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image

            # Calculate Laplacian variance (measure of sharpness)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

            # Normalize to 0-100 scale
            clarity_score = min(100, laplacian_var / 10)  # Adjust divisor based on typical values

            return clarity_score

        except Exception as e:
            logger.error(f"Error calculating clarity: {e}")
            return 50.0  # Default moderate clarity

    def _toggle_iris_window(self):
        """Toggle the iris display window"""
        self.show_iris_window = not self.show_iris_window
        if not self.show_iris_window:
            try:
                cv2.destroyWindow('Captured Iris')
            except:
                pass
        print(f"Iris window: {'ON' if self.show_iris_window else 'OFF'}")

    def _toggle_gallery_window(self):
        """Toggle the enhanced gallery display window"""
        self.show_gallery_window = not self.show_gallery_window
        if not self.show_gallery_window:
            try:
                cv2.destroyWindow('Enhanced Iris Gallery')
                cv2.destroyWindow('Iris Gallery')  # Fallback for old window name
            except:
                pass
        else:
            # Force immediate update when turning on
            if len(self.captured_images) > 0:
                self._update_enhanced_gallery_window()
            self.gallery_opened = True
        print(f"Enhanced Gallery window: {'ON' if self.show_gallery_window else 'OFF'}")

    def _update_iris_display(self):
        """Update the iris display window"""
        if self.current_iris_image is not None:
            display_image = self.current_iris_image['composite'].copy()

            # Resize for better visibility
            height, width = display_image.shape[:2]
            if width < 400:
                scale = 400 / width
                new_width = int(width * scale)
                new_height = int(height * scale)
                display_image = cv2.resize(display_image, (new_width, new_height))

            try:
                cv2.imshow('Captured Iris', display_image)
            except Exception as e:
                logger.warning(f"Cannot display iris window (headless mode): {e}")
                # Save iris image instead
                iris_filename = f"captured_iris_display_{len(self.captured_images)}.jpg"
                cv2.imwrite(iris_filename, display_image)
                print(f"💾 Iris image saved: {iris_filename}")

    def _update_enhanced_gallery_window(self):
        """Update the enhanced live gallery window with detailed analysis"""
        if not self.captured_images:
            return

        try:
            # Calculate grid dimensions
            total_images = len(self.captured_images)
            grid_cols = min(self.gallery_grid_cols, total_images)
            grid_rows = (total_images + grid_cols - 1) // grid_cols

            # Calculate window dimensions (larger for analysis info)
            img_size = self.gallery_image_size
            padding = 15
            header_height = 60
            analysis_height = 80  # Extra space for analysis info

            window_width = grid_cols * img_size + (grid_cols + 1) * padding
            window_height = grid_rows * (img_size + analysis_height) + (grid_rows + 1) * padding + header_height

            # Create enhanced gallery canvas
            gallery = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            gallery.fill(25)  # Darker background for better contrast

            # Add enhanced header with session info
            header_text = f"🖼️ Enhanced Iris Gallery - {total_images} Images"
            cv2.putText(gallery, header_text, (padding, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Add session statistics
            if total_images > 0:
                avg_confidence = sum(img['confidence'] for img in self.captured_images) / total_images
                avg_quality = sum(img.get('analysis', {}).get('quality_score', 0) for img in self.captured_images) / total_images
                stats_text = f"Avg Confidence: {avg_confidence:.1f}% | Avg Quality: {avg_quality:.1f}%"
                cv2.putText(gallery, stats_text, (padding, 45),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            # Add timestamp
            timestamp_text = f"Live Updates: {datetime.now().strftime('%H:%M:%S')}"
            cv2.putText(gallery, timestamp_text, (window_width - 200, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 150), 1)

            # Add captured images to grid with analysis
            for i, capture_data in enumerate(self.captured_images):
                row = i // grid_cols
                col = i % grid_cols

                # Calculate position
                x_pos = col * img_size + (col + 1) * padding
                y_pos = row * (img_size + analysis_height) + (row + 1) * padding + header_height

                # Resize and add image
                try:
                    img_resized = cv2.resize(capture_data['composite'], (img_size, img_size//2))
                    gallery[y_pos:y_pos+img_size//2, x_pos:x_pos+img_size] = img_resized

                    # Add image border
                    cv2.rectangle(gallery, (x_pos-1, y_pos-1),
                                 (x_pos+img_size+1, y_pos+img_size//2+1), (100, 100, 100), 1)

                    # Add detailed analysis information
                    analysis = capture_data.get('analysis', {})

                    # Line 1: Person ID and Session Number
                    info_y = y_pos + img_size//2 + 15
                    person_text = f"#{capture_data.get('session_number', i+1)} Person {capture_data['person_id']}"
                    cv2.putText(gallery, person_text, (x_pos, info_y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

                    # Line 2: Confidence and Quality
                    info_y += 15
                    conf_quality_text = f"Conf: {capture_data['confidence']:.1f}% | Qual: {analysis.get('quality_score', 0):.1f}%"
                    cv2.putText(gallery, conf_quality_text, (x_pos, info_y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 255, 150), 1)

                    # Line 3: Dimensions and Clarity
                    info_y += 15
                    dims_text = f"Size: {analysis.get('iris_dimensions', 'N/A')} | Clarity: {analysis.get('clarity_score', 0):.1f}%"
                    cv2.putText(gallery, dims_text, (x_pos, info_y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 255), 1)

                    # Line 4: Timestamp
                    info_y += 15
                    time_text = capture_data['timestamp'][-8:]  # Last 8 chars (HHMMSS_mmm)
                    cv2.putText(gallery, f"Time: {time_text}", (x_pos, info_y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 200, 150), 1)

                    # Quality indicator bar
                    quality_score = analysis.get('quality_score', 0)
                    bar_width = int((img_size - 20) * quality_score / 100)
                    bar_y = y_pos + img_size//2 + analysis_height - 10

                    # Background bar
                    cv2.rectangle(gallery, (x_pos + 10, bar_y),
                                 (x_pos + img_size - 10, bar_y + 5), (50, 50, 50), -1)

                    # Quality bar (color based on quality)
                    if quality_score >= 80:
                        bar_color = (0, 255, 0)  # Green
                    elif quality_score >= 60:
                        bar_color = (0, 255, 255)  # Yellow
                    else:
                        bar_color = (0, 100, 255)  # Orange

                    cv2.rectangle(gallery, (x_pos + 10, bar_y),
                                 (x_pos + 10 + bar_width, bar_y + 5), bar_color, -1)

                except Exception as e:
                    logger.error(f"Error adding image {i} to enhanced gallery: {e}")

            # Add enhanced instructions at bottom
            instructions_y = window_height - 25
            instructions = "🎮 Controls: 'g' toggle | 'f' refresh | 'c' full view | 'i' iris window"
            cv2.putText(gallery, instructions, (padding, instructions_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)

            # Add real-time indicator
            indicator_text = "🔴 LIVE"
            cv2.putText(gallery, indicator_text, (window_width - 80, instructions_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

            # Display enhanced gallery window
            try:
                cv2.imshow('Enhanced Iris Gallery', gallery)
            except Exception as e:
                logger.warning(f"Cannot display enhanced gallery (headless mode): {e}")
                # Save gallery image instead
                gallery_filename = f"enhanced_gallery_{len(self.captured_images)}_items.jpg"
                cv2.imwrite(gallery_filename, gallery)
                print(f"💾 Enhanced gallery saved: {gallery_filename}")

        except Exception as e:
            logger.error(f"Error creating enhanced gallery window: {e}")

    def _update_gallery_window(self):
        """Update the live gallery window showing all captured images"""
        if not self.captured_images:
            return

        try:
            # Calculate grid dimensions
            total_images = len(self.captured_images)
            grid_cols = min(self.gallery_grid_cols, total_images)
            grid_rows = (total_images + grid_cols - 1) // grid_cols

            # Calculate window dimensions
            img_size = self.gallery_image_size
            padding = 10
            header_height = 40

            window_width = grid_cols * img_size + (grid_cols + 1) * padding
            window_height = grid_rows * img_size + (grid_rows + 1) * padding + header_height

            # Create gallery canvas
            gallery = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            gallery.fill(30)  # Dark gray background

            # Add header
            header_text = f"Iris Gallery - {total_images} Images Captured"
            cv2.putText(gallery, header_text, (padding, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Add timestamp
            timestamp_text = f"Last Updated: {datetime.now().strftime('%H:%M:%S')}"
            cv2.putText(gallery, timestamp_text, (window_width - 200, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

            # Add captured images to grid
            for i, capture_data in enumerate(self.captured_images):
                row = i // grid_cols
                col = i % grid_cols

                x = col * img_size + (col + 1) * padding
                y = row * img_size + (row + 1) * padding + header_height

                # Resize composite image to fit grid
                resized_img = cv2.resize(capture_data['composite'], (img_size, img_size))

                # Add image to gallery
                gallery[y:y+img_size, x:x+img_size] = resized_img

                # Add border and info
                cv2.rectangle(gallery, (x-1, y-1), (x+img_size, y+img_size), (100, 100, 100), 1)

                # Add image number and confidence
                info_text = f"#{i+1} P{capture_data['person_id']} ({capture_data['confidence']:.2f})"
                cv2.putText(gallery, info_text, (x, y-5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1)

            # Add instructions at bottom
            instructions_y = window_height - 15
            instructions = "Press 'g' to toggle | 'f' to refresh | 'c' for full view"
            cv2.putText(gallery, instructions, (padding, instructions_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)

            # Display gallery window
            try:
                cv2.imshow('Iris Gallery', gallery)
            except Exception as e:
                logger.warning(f"Cannot display gallery (headless mode): {e}")
                # Save gallery image instead
                gallery_filename = f"iris_gallery_{len(self.captured_images)}_items.jpg"
                cv2.imwrite(gallery_filename, gallery)
                print(f"💾 Iris gallery saved: {gallery_filename}")

        except Exception as e:
            logger.error(f"Error creating gallery window: {e}")

    def _show_captured_images(self):
        """Show all captured images in a grid"""
        if not self.captured_images:
            print("No captured images to display")
            return

        try:
            # Create a grid of captured images
            grid_cols = min(4, len(self.captured_images))
            grid_rows = (len(self.captured_images) + grid_cols - 1) // grid_cols

            # Calculate grid dimensions
            img_width = 200
            img_height = 150
            grid_width = grid_cols * img_width
            grid_height = grid_rows * img_height + 50  # Extra space for text

            grid_image = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

            # Add title
            cv2.putText(grid_image, f"Captured Iris Images ({len(self.captured_images)} total)",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Add images to grid
            for i, capture_data in enumerate(self.captured_images[-grid_cols*grid_rows:]):
                row = i // grid_cols
                col = i % grid_cols

                x = col * img_width
                y = row * img_height + 50

                # Resize composite image to fit grid
                resized = cv2.resize(capture_data['composite'], (img_width, img_height))
                grid_image[y:y+img_height, x:x+img_width] = resized

                # Add border
                cv2.rectangle(grid_image, (x, y), (x+img_width, y+img_height), (100, 100, 100), 1)

            try:
                cv2.imshow('All Captured Images', grid_image)
                print(f"Showing {len(self.captured_images)} captured images. Press any key to close.")
            except Exception as e:
                logger.warning(f"Cannot display captured images (headless mode): {e}")
                # Save grid image instead
                grid_filename = f"all_captured_images_{len(self.captured_images)}_total.jpg"
                cv2.imwrite(grid_filename, grid_image)
                print(f"💾 All captured images saved: {grid_filename}")
                print(f"📊 Total images: {len(self.captured_images)}")

        except Exception as e:
            logger.error(f"Error showing captured images: {e}")
    
    def get_statistics(self):
        """Get current recognition statistics"""
        return {
            'total_frames': self.total_frames,
            'successful_detections': self.successful_detections,
            'successful_recognitions': self.successful_recognitions,
            'detection_rate': self.successful_detections / max(1, self.total_frames) * 100,
            'recognition_rate': self.successful_recognitions / max(1, self.successful_detections) * 100
        }

def start_live_recognition(model=None, iris_extractor=None):
    """Start live iris recognition system - IMPROVED VERSION"""
    live_system = None
    try:
        # Check if camera is available first
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Camera not available or not accessible")
            print("💡 Possible solutions:")
            print("   - Close other applications using the camera")
            print("   - Check camera permissions")
            print("   - Try a different camera index")
            return False
        cap.release()

        print("🎥 Camera check passed")

        # Check if model is loaded
        if model is None:
            print("⚠️  Warning: No model provided - recognition will be limited")
        else:
            print("🧠 Model loaded successfully")

        if iris_extractor is None:
            print("⚠️  Warning: No iris extractor provided")
        else:
            print("👁️  Iris extractor ready")

        live_system = LiveIrisRecognition(model, iris_extractor)

        print("\n🚀 Starting live iris recognition...")
        print("📋 Controls:")
        print("   - Press 'q' or ESC to quit")
        print("   - Press 's' for screenshot")
        print("   - Press 'r' to reset statistics")
        print("   - Press 'i' to toggle iris capture window")
        print("   - Press 'c' to view all captured iris images")
        print("   - Press 'g' to toggle ENHANCED live gallery window")
        print("   - Press 'f' to refresh enhanced gallery display")
        print("\n💾 Data will be stored in:")
        print("   - Database: iris_system.db")
        print("   - Screenshots: screenshot_YYYYMMDD_HHMMSS.jpg")
        print("   - Captured iris images: captured_iris/ folder")
        print("   - Logs: iris_system.log")
        print("\n👁️ Enhanced Image Capture Features:")
        print("   - Iris images automatically captured when recognition occurs")
        print("   - Real-time display of captured iris in separate window")
        print("   - 🆕 ENHANCED live gallery window with detailed analysis")
        print("   - 🆕 Gallery auto-opens on first capture with real-time updates")
        print("   - 🆕 Detailed analysis: quality scores, dimensions, clarity")
        print("   - 🆕 Visual quality indicators and session statistics")
        print("   - Composite images show both eye region and extracted iris")
        print("   - All captured images saved with person ID and timestamp")
        print("   - Gallery displays comprehensive analysis for each image")

        success = live_system.start_recognition()

        if success:
            stats = live_system.get_statistics()
            print(f"\n📊 Session Statistics:")
            print(f"   Total Frames: {stats['total_frames']}")
            print(f"   Successful Detections: {stats['successful_detections']}")
            print(f"   Successful Recognitions: {stats['successful_recognitions']}")
            print(f"   Detection Rate: {stats['detection_rate']:.1f}%")
            print(f"   Recognition Rate: {stats['recognition_rate']:.1f}%")
            print("✅ Live recognition completed successfully")
        else:
            print("⚠️  Live recognition ended unexpectedly")
            print("💡 Check iris_system.log for detailed error information")

        return success

    except KeyboardInterrupt:
        print("\n🛑 User interrupted - stopping live recognition...")
        logger.info("Live recognition stopped by user")
        return False
    except ImportError as e:
        print(f"❌ Import error in live recognition: {e}")
        logger.error(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in live recognition: {e}")
        logger.error(f"Live recognition error: {e}")
        return False
    finally:
        try:
            if live_system:
                live_system.stop_recognition()
                print("🔄 Cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    # Test live recognition without model
    start_live_recognition()
