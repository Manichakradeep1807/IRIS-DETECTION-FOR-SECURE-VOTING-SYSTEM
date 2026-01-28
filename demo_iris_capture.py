#!/usr/bin/env python3
"""
Demo: Enhanced Live Recognition with Iris Image Capture
Shows the new image capture and display features
"""

import os
import sys
import time

def demo_iris_capture():
    """Demonstrate the enhanced iris capture features"""
    print("🎯 ENHANCED LIVE RECOGNITION DEMO")
    print("=" * 60)
    print("This demo shows the new iris image capture features:")
    print()
    print("🆕 NEW FEATURES:")
    print("   📸 Automatic iris image capture when recognition occurs")
    print("   👁️  Real-time display of captured iris images")
    print("   🖼️  Composite images showing eye region + extracted iris")
    print("   💾 Organized storage in 'captured_iris' folder")
    print("   🔍 View all captured images in a grid layout")
    print()
    
    # Check if we have the required components
    try:
        from live_recognition import start_live_recognition
        from Main import getIrisFeatures
        print("✅ Live recognition modules loaded")
    except ImportError as e:
        print("❌ Import error: {}".format(e))
        return False
    
    # Check for trained model
    model = None
    if os.path.exists('model/best_model.h5'):
        try:
            import tensorflow as tf
            from tensorflow import keras
            model = keras.models.load_model('model/best_model.h5')
            print("✅ Trained model loaded")
        except Exception as e:
            print("⚠️  Could not load model: {}".format(e))
            print("   Demo will run with basic eye detection only")
    else:
        print("⚠️  No trained model found")
        print("   Demo will run with basic eye detection only")
    
    print("\n" + "=" * 60)
    print("🚀 STARTING ENHANCED LIVE RECOGNITION")
    print("=" * 60)
    
    print("\n📋 ENHANCED CONTROLS:")
    print("   🔴 'q' or ESC    → Quit")
    print("   📷 's'           → Take screenshot")
    print("   🔄 'r'           → Reset statistics")
    print("   👁️  'i'           → Toggle iris capture window ON/OFF")
    print("   🖼️  'c'           → View all captured iris images")
    print()
    
    print("💡 WHAT TO EXPECT:")
    print("   1. Main window shows live video with eye detection")
    print("   2. When iris is recognized, image is automatically captured")
    print("   3. 'Captured Iris' window shows the latest captured image")
    print("   4. Press 'c' to see all captured images in a grid")
    print("   5. All images are saved in 'captured_iris/' folder")
    print()
    
    input("Press Enter to start the demo...")
    
    try:
        # Start the enhanced live recognition
        success = start_live_recognition(model=model, iris_extractor=getIrisFeatures)
        
        if success:
            print("\n✅ Demo completed successfully!")
            
            # Show what was captured
            if os.path.exists('captured_iris'):
                captured_files = [f for f in os.listdir('captured_iris') if f.endswith('.jpg')]
                if captured_files:
                    print("\n📸 CAPTURED IMAGES: {} files".format(len(captured_files)))
                    print("   Location: captured_iris/ folder")
                    print("   Files:")
                    for i, filename in enumerate(captured_files[-5:]):  # Show last 5
                        print("     {}. {filename}".format(i+1))
                    if len(captured_files) > 5:
                        print("     ... and {} more".format(len(captured_files) - 5))
                else:
                    print("\n📸 No iris images were captured during this session")
                    print("   💡 Try positioning your eye closer to the camera")
                    print("   💡 Ensure good lighting conditions")
            
        else:
            print("\n❌ Demo ended unexpectedly")
            print("   Check the error messages above for troubleshooting")
        
        return success
        
    except Exception as e:
        print("\n❌ Demo error: {}".format(e))
        return False

def show_capture_folder_info():
    """Show information about the capture folder"""
    print("\n" + "=" * 60)
    print("📁 CAPTURE FOLDER INFORMATION")
    print("=" * 60)
    
    if os.path.exists('captured_iris'):
        files = [f for f in os.listdir('captured_iris') if f.endswith('.jpg')]
        total_size = sum(os.path.getsize(os.path.join('captured_iris', f)) for f in files)
        
        print(f"📂 Folder: captured_iris/")
        print("📊 Files: {} iris images".format(len(files)))
        print("💾 Size: {} KB".format(total_size / 1024:.1f))
        
        if files:
            print(f"\n📋 Recent files:")
            for filename in sorted(files)[-3:]:
                filepath = os.path.join('captured_iris', filename)
                size = os.path.getsize(filepath)
                print("   {} ({size} bytes)".format(filename))
        
        print(f"\n🔍 File naming pattern:")
        print(f"   iris_person[ID]_[YYYYMMDD_HHMMSS_mmm].jpg")
        print(f"   Example: iris_person1_20241202_143052_123.jpg")
        
    else:
        print("📂 Capture folder not created yet")
        print("   Will be created automatically when first iris is captured")

def main():
    """Main demo function"""
    print("👁️ IRIS RECOGNITION - IMAGE CAPTURE DEMO")
    print("=" * 60)
    
    # Run the demo
    success = demo_iris_capture()
    
    # Show folder information
    show_capture_folder_info()
    
    print("\n" + "=" * 60)
    print("📚 SUMMARY OF NEW FEATURES")
    print("=" * 60)
    
    features = [
        "✨ Automatic iris image capture during recognition",
        "🖼️  Real-time display in separate 'Captured Iris' window",
        "📁 Organized storage in 'captured_iris/' folder",
        "🎨 Composite images showing eye region + extracted iris",
        "🔍 Grid view of all captured images (press 'c')",
        "⚙️  Toggle capture window on/off (press 'i')",
        "📊 Person ID and confidence score labeling",
        "⏰ Timestamp-based file naming",
        "💾 Automatic cleanup (keeps last 50 images)",
        "📝 Console feedback for each capture"
    ]
    
    for feature in features:
        print("   {}".format(feature))
    
    print("\n💡 USAGE TIPS:")
    print("   - Position your eye 12-18 inches from camera")
    print("   - Ensure good lighting (avoid shadows)")
    print("   - Look directly at the camera")
    print("   - Wait for green recognition box to appear")
    print("   - Check 'Captured Iris' window for real-time feedback")
    
    if success:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n⚠️  Demo had issues - check error messages above")

if __name__ == "__main__":
    main()
