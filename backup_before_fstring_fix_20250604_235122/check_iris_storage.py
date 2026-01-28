#!/usr/bin/env python3
"""
Check Iris Storage - Shows where and how iris data is stored
"""

import sqlite3
import os
from datetime import datetime

def check_database_contents():
    """Check what's stored in the database"""
    print("🔍 Checking iris_system.db contents...")
    
    if not os.path.exists('iris_system.db'):
        print("❌ iris_system.db not found")
        return
    
    try:
        conn = sqlite3.connect('iris_system.db')
        cursor = conn.cursor()
        
        # Check persons table
        print("\n👥 PERSONS TABLE:")
        cursor.execute("SELECT COUNT(*) FROM persons")
        person_count = cursor.fetchone()[0]
        print(f"   Total persons enrolled: {person_count}")
        
        if person_count > 0:
            cursor.execute("SELECT id, name, email, enrollment_date FROM persons LIMIT 5")
            persons = cursor.fetchall()
            for person in persons:
                print(f"   ID: {person[0]}, Name: {person[1]}, Email: {person[2]}, Date: {person[3]}")
        
        # Check access logs
        print("\n📋 ACCESS LOGS TABLE:")
        cursor.execute("SELECT COUNT(*) FROM access_logs")
        log_count = cursor.fetchone()[0]
        print(f"   Total access attempts: {log_count}")
        
        if log_count > 0:
            cursor.execute("""
                SELECT person_id, access_type, confidence_score, access_granted, 
                       timestamp, location, device_id 
                FROM access_logs 
                ORDER BY timestamp DESC 
                LIMIT 5
            """)
            logs = cursor.fetchall()
            print("   Recent access attempts:")
            for log in logs:
                print(f"     Person: {log[0]}, Type: {log[1]}, Confidence: {log[2]:.2f}, "
                      f"Granted: {log[3]}, Time: {log[4]}, Location: {log[5]}")
        
        # Check for iris templates (if table exists)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='iris_templates';")
        if cursor.fetchone():
            print("\n🧬 IRIS TEMPLATES TABLE:")
            cursor.execute("SELECT COUNT(*) FROM iris_templates")
            template_count = cursor.fetchone()[0]
            print(f"   Total iris templates: {template_count}")
            
            if template_count > 0:
                cursor.execute("""
                    SELECT person_id, quality_score, eye_type, created_date 
                    FROM iris_templates 
                    LIMIT 5
                """)
                templates = cursor.fetchall()
                for template in templates:
                    print(f"     Person: {template[0]}, Quality: {template[1]}, "
                          f"Eye: {template[2]}, Date: {template[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

def check_file_storage():
    """Check file-based storage"""
    print("\n📁 FILE STORAGE:")
    
    # Check for screenshots
    screenshot_files = [f for f in os.listdir('.') if f.startswith('screenshot_') and f.endswith('.jpg')]
    print(f"   Screenshots: {len(screenshot_files)} files")
    for i, file in enumerate(screenshot_files[:5]):
        size = os.path.getsize(file)
        print(f"     {file} ({size} bytes)")
        if i >= 4 and len(screenshot_files) > 5:
            print(f"     ... and {len(screenshot_files) - 5} more")
            break
    
    # Check performance database
    if os.path.exists('performance.db'):
        print(f"   Performance database: {os.path.getsize('performance.db')} bytes")
    
    # Check log file
    if os.path.exists('iris_system.log'):
        print(f"   System log: {os.path.getsize('iris_system.log')} bytes")

def show_storage_explanation():
    """Explain how iris data is stored during live recognition"""
    print("\n" + "="*60)
    print("📚 IRIS DATA STORAGE EXPLANATION")
    print("="*60)
    
    print("""
🔄 DURING LIVE RECOGNITION:

1. 📹 REAL-TIME PROCESSING:
   - Camera captures frames continuously
   - Eye detection runs on each frame
   - Iris features extracted from detected eyes
   - Features compared against trained model

2. 💾 DATA STORAGE LOCATIONS:

   a) DATABASE (iris_system.db):
      - access_logs table: Recognition results with timestamps
      - persons table: Enrolled user information
      - iris_templates table: Stored iris feature templates (BLOB)
      
   b) SCREENSHOTS (optional):
      - Press 's' during live recognition
      - Saved as: screenshot_YYYYMMDD_HHMMSS.jpg
      - Contains the current frame with overlays
      
   c) PERFORMANCE DATABASE (performance.db):
      - Recognition performance metrics
      - Response times and accuracy statistics
      
   d) LOG FILES (iris_system.log):
      - Error messages and system events
      - Debugging information

3. 🔍 WHAT GETS STORED:
   - Person ID (if recognized)
   - Confidence score (0.0 to 1.0)
   - Timestamp of recognition
   - Location/device information
   - Access granted/denied status
   - Eye region coordinates (temporary)

4. 🚫 WHAT'S NOT STORED:
   - Raw camera frames (unless screenshot taken)
   - Continuous video recording
   - Biometric templates of unrecognized persons
   - Personal identifying information beyond enrollment data

5. 🔒 PRIVACY NOTES:
   - Only enrolled persons' templates are stored
   - Raw iris images are processed and discarded
   - Database can be encrypted for additional security
   - Access logs help with audit trails
""")

def main():
    """Main function"""
    print("👁️ IRIS RECOGNITION STORAGE CHECKER")
    print("="*50)
    
    check_database_contents()
    check_file_storage()
    show_storage_explanation()
    
    print("\n" + "="*50)
    print("💡 TO VIEW LIVE RECOGNITION DATA:")
    print("   1. Run live recognition from the main application")
    print("   2. Look for new entries in access_logs table")
    print("   3. Check for new screenshot files if 's' was pressed")
    print("   4. Monitor iris_system.log for any errors")

if __name__ == "__main__":
    main()
