#!/usr/bin/env python3
"""
Test Live Recognition - Simple test to verify live recognition works
"""

import sys
import os
import time

def test_live_recognition():
    """Test the live recognition system"""
    print("🧪 Testing Live Recognition System")
    print("=" * 50)
    
    try:
        # Import the live recognition module
        from live_recognition import start_live_recognition
        from Main import getIrisFeatures
        
        print("✅ Modules imported successfully")
        
        # Test without model first (basic functionality)
        print("\n🔍 Testing basic live recognition (no model)...")
        print("This will test camera access and eye detection only")
        print("Press 'q' to quit after a few seconds")
        
        input("Press Enter to start basic test...")
        
        # Start basic live recognition
        success = start_live_recognition(model=None, iris_extractor=getIrisFeatures)
        
        if success:
            print("✅ Basic live recognition test passed")
        else:
            print("❌ Basic live recognition test failed")
            return False
        
        # Test with model if available
        print("\n🧠 Testing with trained model...")
        try:
            import tensorflow as tf
            from tensorflow import keras
            
            # Try to load the model
            if os.path.exists('model/best_model.h5'):
                print("📁 Loading trained model...")
                model = keras.models.load_model('model/best_model.h5')
                print("✅ Model loaded successfully")
                
                print("This will test full recognition functionality")
                print("Press 'q' to quit after testing")
                
                input("Press Enter to start full test...")
                
                success = start_live_recognition(model=model, iris_extractor=getIrisFeatures)
                
                if success:
                    print("✅ Full live recognition test passed")
                else:
                    print("❌ Full live recognition test failed")
                    
            else:
                print("⚠️  No trained model found - skipping model test")
                print("💡 Train a model first using the main application")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def check_storage_after_test():
    """Check what data was stored during the test"""
    print("\n📊 Checking stored data...")
    
    try:
        import sqlite3
        
        # Check database
        if os.path.exists('iris_system.db'):
            conn = sqlite3.connect('iris_system.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM access_logs")
            log_count = cursor.fetchone()[0]
            print(f"   Access logs: {log_count} entries")
            
            if log_count > 0:
                cursor.execute("""
                    SELECT person_id, confidence_score, timestamp 
                    FROM access_logs 
                    ORDER BY timestamp DESC 
                    LIMIT 3
                """)
                recent_logs = cursor.fetchall()
                print("   Recent entries:")
                for log in recent_logs:
                    print(f"     Person: {log[0]}, Confidence: {log[1]:.2f}, Time: {log[2]}")
            
            conn.close()
        
        # Check screenshots
        screenshots = [f for f in os.listdir('.') if f.startswith('screenshot_')]
        print(f"   Screenshots: {len(screenshots)} files")
        
        # Check log file
        if os.path.exists('iris_system.log'):
            with open('iris_system.log', 'r') as f:
                lines = f.readlines()
                recent_lines = [line for line in lines[-10:] if 'live' in line.lower()]
                if recent_lines:
                    print("   Recent log entries:")
                    for line in recent_lines[-3:]:
                        print(f"     {line.strip()}")
        
    except Exception as e:
        print(f"❌ Error checking storage: {e}")

def main():
    """Main test function"""
    print("🎯 LIVE RECOGNITION TEST SUITE")
    print("=" * 50)
    
    # Run the test
    success = test_live_recognition()
    
    # Check what was stored
    check_storage_after_test()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Live recognition test completed!")
        print("\n💾 Data Storage Summary:")
        print("   - Recognition results → iris_system.db (access_logs table)")
        print("   - Screenshots → screenshot_YYYYMMDD_HHMMSS.jpg")
        print("   - Error logs → iris_system.log")
        print("   - Performance data → performance.db")
    else:
        print("❌ Live recognition test failed!")
        print("💡 Check the error messages above for troubleshooting")

if __name__ == "__main__":
    main()
