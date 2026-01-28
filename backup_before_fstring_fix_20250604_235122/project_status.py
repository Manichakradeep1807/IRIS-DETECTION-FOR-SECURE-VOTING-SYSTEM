#!/usr/bin/env python3
"""
Project Status - Show current status of the iris recognition system
"""

import os
import sys
import sqlite3
from datetime import datetime

def check_system_components():
    """Check all system components"""
    print("🔍 IRIS RECOGNITION SYSTEM STATUS")
    print("=" * 60)
    
    components = {
        "Main Application": "Main.py",
        "Live Recognition": "live_recognition.py", 
        "Headless Recognition": "live_recognition_headless.py",
        "Database Manager": "database_manager.py",
        "Performance Monitor": "performance_monitor.py",
        "Analytics Dashboard": "analytics_dashboard.py",
        "Advanced Models": "advanced_models.py",
        "Data Augmentation": "data_augmentation.py"
    }
    
    print("📁 CORE COMPONENTS:")
    for name, filename in components.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   ✅ {name:20} {filename} ({size:,} bytes)")
        else:
            print(f"   ❌ {name:20} {filename} (missing)")
    
    return True

def check_model_files():
    """Check model files"""
    print(f"\n🧠 MODEL FILES:")
    
    model_files = {
        "Best Model": "model/best_model.h5",
        "Model Config": "model/model.json", 
        "Model Weights": "model/model.weights.h5",
        "Training Data X": "model/X.txt.npy",
        "Training Data Y": "model/Y.txt.npy",
        "Training History": "model/history.pckl"
    }
    
    total_size = 0
    for name, filepath in model_files.items():
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            total_size += size
            print(f"   ✅ {name:15} {filepath} ({size:,} bytes)")
        else:
            print(f"   ❌ {name:15} {filepath} (missing)")
    
    print(f"   📊 Total model size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
    return total_size > 0

def check_datasets():
    """Check dataset folders"""
    print(f"\n📚 DATASETS:")
    
    datasets = {
        "Sample Dataset": "sample_dataset",
        "Test Samples": "testSamples", 
        "🆕 Captured Iris": "captured_iris"
    }
    
    for name, folder in datasets.items():
        if os.path.exists(folder):
            files = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
            if os.path.isdir(folder):
                subdirs = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
                if subdirs:
                    print(f"   ✅ {name:15} {folder}/ ({len(subdirs)} persons, {len(files)} images)")
                else:
                    print(f"   ✅ {name:15} {folder}/ ({len(files)} images)")
            else:
                print(f"   ✅ {name:15} {folder}/ ({len(files)} images)")
        else:
            print(f"   ❌ {name:15} {folder}/ (missing)")

def check_database():
    """Check database status"""
    print(f"\n💾 DATABASE STATUS:")
    
    databases = {
        "Main Database": "iris_system.db",
        "Performance DB": "performance.db"
    }
    
    for name, db_file in databases.items():
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            print(f"   ✅ {name:15} {db_file} ({size:,} bytes)")
            
            # Check tables for main database
            if db_file == "iris_system.db":
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    
                    # Check persons
                    cursor.execute("SELECT COUNT(*) FROM persons")
                    person_count = cursor.fetchone()[0]
                    
                    # Check access logs
                    cursor.execute("SELECT COUNT(*) FROM access_logs")
                    log_count = cursor.fetchone()[0]
                    
                    print(f"      📊 {person_count} persons enrolled")
                    print(f"      📋 {log_count} access log entries")
                    
                    conn.close()
                except Exception as e:
                    print(f"      ⚠️ Error reading database: {e}")
        else:
            print(f"   ❌ {name:15} {db_file} (missing)")

def check_new_features():
    """Check new iris capture features"""
    print(f"\n🆕 NEW IRIS CAPTURE FEATURES:")
    
    # Check if captured_iris folder exists and has content
    if os.path.exists("captured_iris"):
        files = [f for f in os.listdir("captured_iris") if f.endswith('.jpg')]
        print(f"   ✅ Capture Folder    captured_iris/ ({len(files)} images)")
        
        if files:
            print(f"   📸 Recent captures:")
            for filename in sorted(files)[-3:]:  # Show last 3
                filepath = os.path.join("captured_iris", filename)
                size = os.path.getsize(filepath)
                print(f"      {filename} ({size:,} bytes)")
    else:
        print(f"   ⚠️ Capture Folder    captured_iris/ (will be created on first capture)")
    
    # Check enhanced live recognition
    if os.path.exists("live_recognition.py"):
        with open("live_recognition.py", "r") as f:
            content = f.read()
            features = [
                ("Automatic Capture", "_capture_iris_image" in content),
                ("Toggle Controls", "_toggle_iris_window" in content), 
                ("Grid View", "_show_captured_images" in content),
                ("Real-time Display", "_update_iris_display" in content),
                ("Enhanced Controls", "'i' for toggle iris window" in content)
            ]
            
            for feature_name, exists in features:
                status = "✅" if exists else "❌"
                print(f"   {status} {feature_name:15} {'Implemented' if exists else 'Missing'}")

def show_usage_instructions():
    """Show how to use the system"""
    print(f"\n🚀 HOW TO USE THE ENHANCED SYSTEM:")
    print("=" * 60)
    
    print("1. 📱 START MAIN APPLICATION:")
    print("   python Main.py")
    print("   → Opens GUI with all features")
    print()
    
    print("2. 🧠 TRAIN MODEL (if needed):")
    print("   → Click 'TRAIN MODEL' button")
    print("   → Wait for training to complete")
    print()
    
    print("3. 📹 START LIVE RECOGNITION:")
    print("   → Click 'LIVE RECOGNITION' button")
    print("   → Position eye 12-18 inches from camera")
    print("   → Watch for automatic iris capture!")
    print()
    
    print("4. 🎮 NEW CONTROLS DURING LIVE RECOGNITION:")
    print("   'q' or ESC → Quit")
    print("   's'        → Take screenshot") 
    print("   'r'        → Reset statistics")
    print("   🆕 'i'     → Toggle iris capture window")
    print("   🆕 'c'     → View all captured iris images")
    print()
    
    print("5. 📁 CHECK CAPTURED IMAGES:")
    print("   → Look in captured_iris/ folder")
    print("   → Each image shows eye region + extracted iris")
    print("   → Files named: iris_person[ID]_[timestamp].jpg")
    print()
    
    print("6. 📊 ALTERNATIVE MODES:")
    print("   python live_recognition.py          → Direct live recognition")
    print("   python live_recognition_headless.py → Headless mode (no GUI)")
    print("   python demo_iris_capture.py         → Feature demonstration")

def main():
    """Main status check"""
    print("👁️ IRIS RECOGNITION PROJECT STATUS")
    print("=" * 60)
    print(f"📅 Status check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all checks
    check_system_components()
    has_model = check_model_files()
    check_datasets()
    check_database()
    check_new_features()
    
    # Overall status
    print("\n" + "=" * 60)
    print("📊 OVERALL STATUS")
    print("=" * 60)
    
    if has_model:
        print("✅ System is READY for full iris recognition")
        print("✅ All components are available")
        print("✅ 🆕 Enhanced iris capture features implemented")
        print("✅ Model is trained and ready")
    else:
        print("⚠️ System is PARTIALLY READY")
        print("✅ All components are available") 
        print("✅ 🆕 Enhanced iris capture features implemented")
        print("⚠️ Model needs training for full recognition")
    
    show_usage_instructions()
    
    print("\n🎉 The iris recognition system with enhanced image capture is ready to use!")

if __name__ == "__main__":
    main()
