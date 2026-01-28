#!/usr/bin/env python3
"""
Diagnostic script for Live Recognition Issues
Helps identify why live recognition ends unexpectedly
"""

import cv2
import os
import sys
import sqlite3
import logging
from datetime import datetime

def check_camera_access():
    """Check if camera is accessible"""
    print("🔍 Checking camera access...")
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Camera not accessible")
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("❌ Cannot read from camera")
            cap.release()
            return False
        
        print(f"✅ Camera accessible - Frame size: {frame.shape}")
        cap.release()
        return True
    except Exception as e:
        print(f"❌ Camera error: {e}")
        return False

def check_model_files():
    """Check if model files exist"""
    print("\n🔍 Checking model files...")
    model_files = [
        'model/best_model.h5',
        'model/model.json',
        'model/model.weights.h5'
    ]
    
    all_exist = True
    for file_path in model_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} exists ({size} bytes)")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    required_modules = [
        'cv2', 'numpy', 'tensorflow', 'keras', 'sqlite3', 
        'threading', 'queue', 'tkinter'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} missing")
            missing.append(module)
    
    return len(missing) == 0

def check_database():
    """Check database connectivity and tables"""
    print("\n🔍 Checking database...")
    try:
        if not os.path.exists('iris_system.db'):
            print("❌ iris_system.db not found")
            return False
        
        conn = sqlite3.connect('iris_system.db')
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Database connected - Tables: {[t[0] for t in tables]}")
        
        # Check access logs
        cursor.execute("SELECT COUNT(*) FROM access_logs;")
        log_count = cursor.fetchone()[0]
        print(f"✅ Access logs: {log_count} entries")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_cascade_files():
    """Check OpenCV cascade files"""
    print("\n🔍 Checking OpenCV cascade files...")
    try:
        eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
        face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        
        if os.path.exists(eye_cascade_path):
            print(f"✅ Eye cascade: {eye_cascade_path}")
        else:
            print(f"❌ Eye cascade missing: {eye_cascade_path}")
            return False
            
        if os.path.exists(face_cascade_path):
            print(f"✅ Face cascade: {face_cascade_path}")
        else:
            print(f"❌ Face cascade missing: {face_cascade_path}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Cascade error: {e}")
        return False

def test_basic_recognition():
    """Test basic recognition functionality"""
    print("\n🔍 Testing basic recognition...")
    try:
        # Import the live recognition module
        from live_recognition import LiveIrisRecognition
        
        # Create instance without model (basic test)
        live_system = LiveIrisRecognition()
        print("✅ LiveIrisRecognition instance created")
        
        # Test camera initialization
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Test eye detection
                eyes = live_system._detect_eyes(frame)
                print(f"✅ Eye detection test - Found {len(eyes) if eyes else 0} eyes")
            cap.release()
        
        return True
    except Exception as e:
        print(f"❌ Recognition test error: {e}")
        return False

def check_log_files():
    """Check recent log entries"""
    print("\n🔍 Checking recent logs...")
    try:
        if os.path.exists('iris_system.log'):
            with open('iris_system.log', 'r') as f:
                lines = f.readlines()
                recent_lines = lines[-10:] if len(lines) > 10 else lines
                print("📋 Recent log entries:")
                for line in recent_lines:
                    print(f"   {line.strip()}")
        else:
            print("❌ No log file found")
        return True
    except Exception as e:
        print(f"❌ Log check error: {e}")
        return False

def main():
    """Run all diagnostic checks"""
    print("🔧 Live Recognition Diagnostic Tool")
    print("=" * 50)
    
    checks = [
        ("Camera Access", check_camera_access),
        ("Model Files", check_model_files),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("Cascade Files", check_cascade_files),
        ("Basic Recognition", test_basic_recognition),
        ("Log Files", check_log_files)
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results[name] = False
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:20} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Live recognition should work.")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   - Ensure camera is not used by another application")
        print("   - Run: pip install -r requirements.txt")
        print("   - Train a model first using the main application")
        print("   - Check camera permissions")
    
    print("\n📍 Iris data storage locations:")
    print("   - Database: iris_system.db (access_logs, iris_templates tables)")
    print("   - Screenshots: screenshot_YYYYMMDD_HHMMSS.jpg")
    print("   - Performance: performance.db")
    print("   - Logs: iris_system.log")

if __name__ == "__main__":
    main()
