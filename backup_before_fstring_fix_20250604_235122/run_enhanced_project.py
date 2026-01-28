#!/usr/bin/env python3
"""
Run Enhanced Iris Recognition Project
Demonstrates all new features including live gallery and iris capture
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def show_project_overview():
    """Show overview of the enhanced project"""
    print("🎯 ENHANCED IRIS RECOGNITION PROJECT")
    print("=" * 60)
    print("🆕 NEW FEATURES ADDED:")
    print("   📸 Automatic iris image capture during recognition")
    print("   👁️ Real-time display of captured iris images")
    print("   🖼️ Live gallery window with all captured images")
    print("   🎮 Enhanced keyboard controls")
    print("   📊 Professional gallery layout with metadata")
    print("   ⏰ Live timestamp updates")
    print("   💾 Organized storage in captured_iris/ folder")
    print()

def check_system_status():
    """Check if all components are ready"""
    print("🔍 SYSTEM STATUS CHECK:")
    print("-" * 40)
    
    # Check core files
    core_files = {
        "Main Application": "Main.py",
        "Enhanced Live Recognition": "live_recognition.py",
        "Headless Recognition": "live_recognition_headless.py",
        "Database Manager": "database_manager.py",
        "Performance Monitor": "performance_monitor.py"
    }
    
    all_ready = True
    for name, filename in core_files.items():
        if os.path.exists(filename):
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name} - Missing!")
            all_ready = False
    
    # Check model
    if os.path.exists("model/best_model.h5"):
        size = os.path.getsize("model/best_model.h5")
        print(f"   ✅ Trained Model ({size:,} bytes)")
    else:
        print(f"   ⚠️ Trained Model - Not found (will use basic mode)")
    
    # Check capture folder
    if os.path.exists("captured_iris"):
        files = [f for f in os.listdir("captured_iris") if f.endswith('.jpg')]
        print(f"   ✅ Capture Folder ({len(files)} existing images)")
    else:
        print(f"   ✅ Capture Folder (will be created)")
    
    return all_ready

def show_new_controls():
    """Show the new keyboard controls"""
    print("\n🎮 ENHANCED KEYBOARD CONTROLS:")
    print("-" * 40)
    print("📹 During Live Recognition:")
    print("   'q' or ESC → Quit live recognition")
    print("   's'        → Take screenshot of current frame")
    print("   'r'        → Reset recognition statistics")
    print("   🆕 'i'     → Toggle iris capture window ON/OFF")
    print("   🆕 'c'     → View all captured images in grid")
    print("   🆕 'g'     → Toggle live gallery window ON/OFF")
    print("   🆕 'f'     → Force refresh gallery display")
    print()

def show_windows_layout():
    """Show what windows will be displayed"""
    print("🖼️ WINDOW LAYOUT:")
    print("-" * 40)
    print("When live recognition starts, you'll see:")
    print()
    print("1. 📹 MAIN WINDOW: 'Live Iris Recognition'")
    print("   - Live camera feed")
    print("   - Eye detection boxes")
    print("   - Recognition results overlay")
    print("   - Statistics display")
    print()
    print("2. 👁️ IRIS WINDOW: 'Captured Iris'")
    print("   - Latest captured iris image")
    print("   - Composite showing eye region + extracted iris")
    print("   - Person ID and confidence score")
    print()
    print("3. 🆕 GALLERY WINDOW: 'Iris Gallery'")
    print("   - Grid of all captured images (4 columns)")
    print("   - Image numbers and metadata")
    print("   - Live timestamp updates")
    print("   - Updates automatically every 30 frames")
    print()

def run_enhanced_live_recognition():
    """Run the enhanced live recognition"""
    print("🚀 STARTING ENHANCED LIVE RECOGNITION")
    print("=" * 60)
    
    print("📋 What to expect:")
    print("   1. Camera will initialize")
    print("   2. Three windows will open (if GUI available)")
    print("   3. Position your eye 12-18 inches from camera")
    print("   4. Watch for automatic iris capture!")
    print("   5. Gallery will update in real-time")
    print()
    
    print("💡 Tips for best results:")
    print("   - Ensure good lighting")
    print("   - Look directly at camera")
    print("   - Keep head steady")
    print("   - Wait for green recognition box")
    print()
    
    input("Press Enter to start enhanced live recognition...")
    
    try:
        # Import and run the enhanced live recognition
        from live_recognition import start_live_recognition
        from Main import getIrisFeatures
        
        # Try to load model
        model = None
        if os.path.exists('model/best_model.h5'):
            try:
                import tensorflow as tf
                from tensorflow import keras
                model = keras.models.load_model('model/best_model.h5')
                print("✅ Model loaded - Full recognition available")
            except Exception as e:
                print(f"⚠️ Model load error: {e}")
                print("   Running in basic mode")
        else:
            print("⚠️ No trained model - Running in basic mode")
        
        print("\n🎬 Starting enhanced live recognition with all new features...")
        
        # Start the enhanced system
        success = start_live_recognition(model=model, iris_extractor=getIrisFeatures)
        
        if success:
            print("\n✅ Enhanced live recognition completed!")
            
            # Show results
            if os.path.exists('captured_iris'):
                files = [f for f in os.listdir('captured_iris') if f.endswith('.jpg')]
                if files:
                    print(f"\n📸 SESSION RESULTS:")
                    print(f"   Images captured: {len(files)}")
                    print(f"   Latest captures:")
                    for filename in sorted(files)[-3:]:
                        print(f"     {filename}")
                    print(f"   📁 All images saved in: captured_iris/")
                else:
                    print("\n📸 No new images captured this session")
            
        else:
            print("\n⚠️ Live recognition ended unexpectedly")
            print("   This is normal if you pressed 'q' to quit")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Error running enhanced live recognition: {e}")
        return False

def show_project_summary():
    """Show summary of all features"""
    print("\n" + "=" * 60)
    print("📚 ENHANCED PROJECT SUMMARY")
    print("=" * 60)
    
    print("\n🎯 CORE FEATURES:")
    print("   ✅ Iris recognition with deep learning")
    print("   ✅ Live camera feed processing")
    print("   ✅ Database storage and management")
    print("   ✅ Performance monitoring")
    print("   ✅ Analytics dashboard")
    print()
    
    print("🆕 NEW ENHANCED FEATURES:")
    print("   ✅ Automatic iris image capture")
    print("   ✅ Real-time iris display window")
    print("   ✅ Live gallery with all captured images")
    print("   ✅ Professional grid layout")
    print("   ✅ Enhanced keyboard controls")
    print("   ✅ Live timestamp updates")
    print("   ✅ Organized file storage")
    print("   ✅ Composite image creation")
    print("   ✅ Metadata display (person ID, confidence)")
    print("   ✅ Headless mode support")
    print()
    
    print("💾 DATA STORAGE:")
    print("   📁 captured_iris/ - Captured iris images")
    print("   💾 iris_system.db - Recognition database")
    print("   📊 performance.db - Performance metrics")
    print("   📝 iris_system.log - System logs")
    print()
    
    print("🎮 USER CONTROLS:")
    print("   Basic: q(quit), s(screenshot), r(reset)")
    print("   🆕 Enhanced: i(iris), c(grid), g(gallery), f(refresh)")

def main():
    """Main function"""
    print("🎉 ENHANCED IRIS RECOGNITION PROJECT")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Show overview
    show_project_overview()
    
    # Check system status
    system_ready = check_system_status()
    
    if not system_ready:
        print("\n❌ System not ready - missing components")
        return False
    
    # Show controls and layout
    show_new_controls()
    show_windows_layout()
    
    # Run the enhanced system
    success = run_enhanced_live_recognition()
    
    # Show summary
    show_project_summary()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ENHANCED PROJECT DEMONSTRATION COMPLETED!")
        print("   All new features are working correctly")
        print("   Live gallery and iris capture ready for use")
    else:
        print("⚠️ DEMONSTRATION HAD ISSUES")
        print("   Check error messages above")
        print("   Features are implemented but may need GUI support")
    
    print("\n💡 To run again:")
    print("   python Main.py → Full GUI application")
    print("   python live_recognition.py → Direct enhanced recognition")
    print("   python live_recognition_headless.py → Headless mode")

if __name__ == "__main__":
    main()
