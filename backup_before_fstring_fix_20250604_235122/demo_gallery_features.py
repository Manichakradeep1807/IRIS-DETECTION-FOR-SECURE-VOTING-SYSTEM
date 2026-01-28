#!/usr/bin/env python3
"""
Demo: Enhanced Live Recognition with Real-time Gallery
Shows the new live gallery window features
"""

import os
import sys
import time
import cv2
import numpy as np
from datetime import datetime

def create_demo_gallery():
    """Create a demo gallery window to show the new features"""
    print("🖼️ LIVE GALLERY FEATURES DEMO")
    print("=" * 60)
    
    # Simulate captured iris images
    demo_images = []
    
    # Create some demo composite images
    for i in range(8):
        # Create a demo composite image
        composite_height = 200
        composite_width = 300
        composite = np.zeros((composite_height, composite_width, 3), dtype=np.uint8)
        
        # Add some demo content
        # Eye region (left side)
        eye_region = np.random.randint(50, 200, (150, 140, 3), dtype=np.uint8)
        composite[30:180, 10:150] = eye_region
        
        # Iris region (right side)
        iris_region = np.random.randint(80, 220, (64, 64, 3), dtype=np.uint8)
        composite[68:132, 170:234] = iris_region
        
        # Add labels
        cv2.putText(composite, f"Demo Person {i+1} - Confidence: 0.{85+i}", 
                   (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(composite, "Eye Region", (10, 190), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv2.putText(composite, "Extracted Iris", (170, 190), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Store demo data
        demo_data = {
            'composite': composite,
            'person_id': i + 1,
            'confidence': 0.85 + i * 0.02,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        demo_images.append(demo_data)
    
    return demo_images

def create_gallery_window(captured_images, title="Live Iris Gallery Demo"):
    """Create a gallery window similar to the live recognition system"""
    if not captured_images:
        return None
    
    # Gallery settings
    gallery_grid_cols = 4
    gallery_image_size = 150
    
    # Calculate grid dimensions
    total_images = len(captured_images)
    grid_cols = min(gallery_grid_cols, total_images)
    grid_rows = (total_images + grid_cols - 1) // grid_cols
    
    # Calculate window dimensions
    img_size = gallery_image_size
    padding = 10
    header_height = 60
    footer_height = 40
    
    window_width = grid_cols * img_size + (grid_cols + 1) * padding
    window_height = grid_rows * img_size + (grid_rows + 1) * padding + header_height + footer_height
    
    # Create gallery canvas
    gallery = np.zeros((window_height, window_width, 3), dtype=np.uint8)
    gallery.fill(30)  # Dark gray background
    
    # Add header
    header_text = f"{title}"
    cv2.putText(gallery, header_text, (padding, 25), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Add subtitle
    subtitle_text = f"{total_images} Images Captured - Live Updates"
    cv2.putText(gallery, subtitle_text, (padding, 45), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Add timestamp
    timestamp_text = f"Updated: {datetime.now().strftime('%H:%M:%S')}"
    cv2.putText(gallery, timestamp_text, (window_width - 150, 25), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 255, 150), 1)
    
    # Add captured images to grid
    for i, capture_data in enumerate(captured_images):
        row = i // grid_cols
        col = i % grid_cols
        
        x = col * img_size + (col + 1) * padding
        y = row * img_size + (row + 1) * padding + header_height
        
        # Resize composite image to fit grid
        resized_img = cv2.resize(capture_data['composite'], (img_size, img_size))
        
        # Add image to gallery
        gallery[y:y+img_size, x:x+img_size] = resized_img
        
        # Add border
        cv2.rectangle(gallery, (x-2, y-2), (x+img_size+1, y+img_size+1), (100, 100, 100), 2)
        
        # Add image info
        info_text = f"#{i+1} Person {capture_data['person_id']}"
        cv2.putText(gallery, info_text, (x, y-8), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 0), 1)
        
        # Add confidence
        conf_text = f"Conf: {capture_data['confidence']:.2f}"
        cv2.putText(gallery, conf_text, (x, y+img_size+15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
    
    # Add footer instructions
    footer_y = window_height - 25
    instructions = "🆕 NEW: Live gallery updates automatically during recognition!"
    cv2.putText(gallery, instructions, (padding, footer_y), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 255, 100), 1)
    
    footer_y2 = window_height - 10
    controls = "Controls: 'g' toggle | 'f' refresh | 'c' full view | 'q' quit"
    cv2.putText(gallery, controls, (padding, footer_y2), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1)
    
    return gallery

def demo_live_gallery():
    """Demonstrate the live gallery features"""
    print("\n🎯 LIVE GALLERY DEMONSTRATION")
    print("=" * 60)
    
    print("This demo shows the new live gallery window features:")
    print("✨ Real-time updates as iris images are captured")
    print("🖼️ Grid layout showing all captured images")
    print("📊 Image info: number, person ID, confidence score")
    print("⏰ Live timestamp updates")
    print("🎮 Interactive controls")
    print()
    
    # Create demo images
    demo_images = create_demo_gallery()
    
    print("🚀 Starting live gallery demo...")
    print("📋 Demo will show:")
    print("   1. Empty gallery (no captures yet)")
    print("   2. Gallery filling up with captures")
    print("   3. Full gallery with all features")
    print()
    
    input("Press Enter to start the demo...")
    
    try:
        # Show progressive gallery updates
        for i in range(len(demo_images) + 1):
            if i == 0:
                print("📱 Gallery: No captures yet...")
                time.sleep(1)
                continue
            
            # Show gallery with i images
            current_images = demo_images[:i]
            gallery = create_gallery_window(current_images, f"Live Gallery Demo - Step {i}")
            
            if gallery is not None:
                cv2.imshow('Live Iris Gallery Demo', gallery)
                print(f"📸 Gallery updated: {i} image(s) captured")
                
                # Wait for key press or timeout
                key = cv2.waitKey(2000) & 0xFF
                if key == ord('q') or key == 27:
                    break
        
        # Show final gallery
        if demo_images:
            final_gallery = create_gallery_window(demo_images, "Complete Live Gallery")
            cv2.imshow('Live Iris Gallery Demo', final_gallery)
            
            print("\n🎉 Demo complete! Final gallery showing all features:")
            print(f"   📊 {len(demo_images)} images in gallery")
            print("   🖼️ Grid layout with borders and labels")
            print("   📝 Image numbers, person IDs, and confidence scores")
            print("   ⏰ Live timestamp display")
            print()
            print("Press any key to close the demo...")
            
            cv2.waitKey(0)
        
        cv2.destroyAllWindows()
        
        print("\n✅ Live gallery demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return False
    finally:
        cv2.destroyAllWindows()

def show_feature_comparison():
    """Show comparison between old and new features"""
    print("\n" + "=" * 60)
    print("📊 FEATURE COMPARISON: OLD vs NEW")
    print("=" * 60)
    
    print("\n🔄 BEFORE (Original System):")
    print("   📸 Iris images captured and saved to files")
    print("   💾 Images stored in captured_iris/ folder")
    print("   👁️ Single 'Captured Iris' window for latest image")
    print("   🔍 Press 'c' to view all images in static grid")
    
    print("\n🆕 AFTER (Enhanced System):")
    print("   📸 Iris images captured and saved to files")
    print("   💾 Images stored in captured_iris/ folder")
    print("   👁️ Single 'Captured Iris' window for latest image")
    print("   🔍 Press 'c' to view all images in static grid")
    print("   🖼️ NEW: Live 'Iris Gallery' window")
    print("   ⚡ NEW: Real-time updates every 30 frames")
    print("   🎮 NEW: Toggle gallery with 'g' key")
    print("   🔄 NEW: Force refresh with 'f' key")
    print("   📊 NEW: Image numbers and metadata display")
    print("   ⏰ NEW: Live timestamp updates")
    
    print("\n💡 BENEFITS:")
    print("   ✅ See all captured images without interrupting recognition")
    print("   ✅ Real-time feedback on capture progress")
    print("   ✅ Better user experience with live updates")
    print("   ✅ Easy monitoring of recognition quality")
    print("   ✅ Professional gallery-style display")

def main():
    """Main demo function"""
    print("🖼️ LIVE IRIS GALLERY - FEATURE DEMO")
    print("=" * 60)
    
    # Show feature comparison
    show_feature_comparison()
    
    # Run the demo
    success = demo_live_gallery()
    
    print("\n" + "=" * 60)
    print("📚 HOW TO USE IN LIVE RECOGNITION")
    print("=" * 60)
    
    print("\n🚀 To use the new gallery features:")
    print("   1. Start live recognition: python live_recognition.py")
    print("   2. Position your eye in front of camera")
    print("   3. Watch the 'Iris Gallery' window update automatically")
    print("   4. Use new controls:")
    print("      - 'g' → Toggle gallery window ON/OFF")
    print("      - 'f' → Force gallery refresh")
    print("      - 'c' → View full-size grid (existing feature)")
    
    print("\n🎯 Gallery Features:")
    print("   📊 Shows all captured images in real-time")
    print("   🔢 Displays image numbers and person IDs")
    print("   📈 Shows confidence scores for each capture")
    print("   ⏰ Updates timestamp automatically")
    print("   🖼️ Professional grid layout with borders")
    
    if success:
        print("\n🎉 Gallery features are ready to use!")
    else:
        print("\n⚠️ Demo had issues - check error messages above")

if __name__ == "__main__":
    main()
