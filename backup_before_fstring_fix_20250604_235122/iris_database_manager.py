"""
Enhanced Iris Database Manager
Manages iris recognition data, user enrollment, and access logs
"""

import sqlite3
import os
import cv2
import numpy as np
from datetime import datetime
import json
import hashlib

class IrisDatabaseManager:
    """Enhanced database manager for iris recognition system"""
    
    def __init__(self, db_path="iris_recognition.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER UNIQUE NOT NULL,
                name TEXT,
                email TEXT,
                phone TEXT,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                iris_template_hash TEXT,
                metadata TEXT
            )
        ''')
        
        # Iris templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS iris_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER,
                template_data BLOB,
                template_hash TEXT,
                quality_score REAL,
                eye_type TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES users (person_id)
            )
        ''')
        
        # Access logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER,
                access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_type TEXT,
                confidence_score REAL,
                access_granted BOOLEAN,
                location TEXT,
                device_id TEXT,
                image_path TEXT,
                FOREIGN KEY (person_id) REFERENCES users (person_id)
            )
        ''')
        
        # Recognition statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recognition_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                total_attempts INTEGER DEFAULT 0,
                successful_recognitions INTEGER DEFAULT 0,
                failed_attempts INTEGER DEFAULT 0,
                average_confidence REAL DEFAULT 0.0,
                unique_users INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def enroll_user(self, person_id, name=None, email=None, phone=None, iris_image_path=None):
        """Enroll a new user in the system"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE person_id = ?", (person_id,))
            if cursor.fetchone():
                conn.close()
                return False, "User already enrolled"
            
            # Process iris template if image provided
            iris_template_hash = None
            if iris_image_path and os.path.exists(iris_image_path):
                # Extract iris features and create hash
                iris_features = self._extract_iris_features(iris_image_path)
                if iris_features is not None:
                    iris_template_hash = self._create_template_hash(iris_features)
                    
                    # Save iris template
                    template_data = cv2.imencode('.jpg', iris_features)[1].tobytes()
                    cursor.execute('''
                        INSERT INTO iris_templates 
                        (person_id, template_data, template_hash, quality_score, eye_type)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (person_id, template_data, iris_template_hash, 0.85, 'unknown'))
            
            # Insert user
            cursor.execute('''
                INSERT INTO users (person_id, name, email, phone, iris_template_hash)
                VALUES (?, ?, ?, ?, ?)
            ''', (person_id, name, email, phone, iris_template_hash))
            
            conn.commit()
            conn.close()
            
            return True, "User enrolled successfully"
            
        except Exception as e:
            return False, f"Enrollment error: {str(e)}"
    
    def log_access(self, person_id, access_type="recognition", confidence_score=0.0, 
                   access_granted=True, location="Unknown", device_id="default", image_path=None):
        """Log an access attempt"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO access_logs 
                (person_id, access_type, confidence_score, access_granted, location, device_id, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (person_id, access_type, confidence_score, access_granted, location, device_id, image_path))
            
            conn.commit()
            conn.close()
            
            # Update daily statistics
            self._update_daily_stats(access_granted, confidence_score)
            
            return True
            
        except Exception as e:
            print(f"Error logging access: {e}")
            return False
    
    def get_user_info(self, person_id):
        """Get user information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT person_id, name, email, phone, enrollment_date, is_active
                FROM users WHERE person_id = ?
            ''', (person_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'person_id': result[0],
                    'name': result[1],
                    'email': result[2],
                    'phone': result[3],
                    'enrollment_date': result[4],
                    'is_active': result[5]
                }
            return None
            
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
    
    def get_access_history(self, person_id=None, limit=50):
        """Get access history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if person_id:
                cursor.execute('''
                    SELECT al.*, u.name 
                    FROM access_logs al
                    LEFT JOIN users u ON al.person_id = u.person_id
                    WHERE al.person_id = ?
                    ORDER BY al.access_time DESC
                    LIMIT ?
                ''', (person_id, limit))
            else:
                cursor.execute('''
                    SELECT al.*, u.name 
                    FROM access_logs al
                    LEFT JOIN users u ON al.person_id = u.person_id
                    ORDER BY al.access_time DESC
                    LIMIT ?
                ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'person_id': row[1],
                    'access_time': row[2],
                    'access_type': row[3],
                    'confidence_score': row[4],
                    'access_granted': row[5],
                    'location': row[6],
                    'device_id': row[7],
                    'image_path': row[8],
                    'name': row[9]
                }
                for row in results
            ]
            
        except Exception as e:
            print(f"Error getting access history: {e}")
            return []
    
    def get_system_statistics(self):
        """Get system statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            total_users = cursor.fetchone()[0]
            
            # Total access attempts today
            cursor.execute('''
                SELECT COUNT(*) FROM access_logs 
                WHERE DATE(access_time) = DATE('now')
            ''')
            today_attempts = cursor.fetchone()[0]
            
            # Successful recognitions today
            cursor.execute('''
                SELECT COUNT(*) FROM access_logs 
                WHERE DATE(access_time) = DATE('now') AND access_granted = 1
            ''')
            today_success = cursor.fetchone()[0]
            
            # Average confidence today
            cursor.execute('''
                SELECT AVG(confidence_score) FROM access_logs 
                WHERE DATE(access_time) = DATE('now') AND access_granted = 1
            ''')
            avg_confidence = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            return {
                'total_users': total_users,
                'today_attempts': today_attempts,
                'today_success': today_success,
                'today_success_rate': (today_success / max(1, today_attempts)) * 100,
                'average_confidence': avg_confidence
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def _extract_iris_features(self, image_path):
        """Extract iris features from image"""
        try:
            # Import the iris extraction function from Main.py
            import sys
            sys.path.append('.')
            from Main import getIrisFeatures
            
            return getIrisFeatures(image_path)
            
        except Exception as e:
            print(f"Error extracting iris features: {e}")
            return None
    
    def _create_template_hash(self, iris_features):
        """Create a hash of iris template for quick comparison"""
        try:
            # Convert image to bytes and create hash
            _, buffer = cv2.imencode('.jpg', iris_features)
            return hashlib.md5(buffer).hexdigest()
            
        except Exception as e:
            print(f"Error creating template hash: {e}")
            return None
    
    def _update_daily_stats(self, access_granted, confidence_score):
        """Update daily statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().date()
            
            # Check if today's record exists
            cursor.execute("SELECT id FROM recognition_stats WHERE date = ?", (today,))
            if cursor.fetchone():
                # Update existing record
                cursor.execute('''
                    UPDATE recognition_stats 
                    SET total_attempts = total_attempts + 1,
                        successful_recognitions = successful_recognitions + ?,
                        failed_attempts = failed_attempts + ?
                    WHERE date = ?
                ''', (1 if access_granted else 0, 0 if access_granted else 1, today))
            else:
                # Create new record
                cursor.execute('''
                    INSERT INTO recognition_stats 
                    (date, total_attempts, successful_recognitions, failed_attempts)
                    VALUES (?, 1, ?, ?)
                ''', (today, 1 if access_granted else 0, 0 if access_granted else 1))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating daily stats: {e}")

# Global database instance
db = IrisDatabaseManager()

if __name__ == "__main__":
    # Test the database
    print("Testing Iris Database Manager...")
    
    # Test enrollment
    success, message = db.enroll_user(1, "John Doe", "john@example.com", "123-456-7890")
    print(f"Enrollment: {message}")
    
    # Test access logging
    db.log_access(1, "live_recognition", 0.95, True, "Main Entrance", "camera_01")
    
    # Test statistics
    stats = db.get_system_statistics()
    print(f"Statistics: {stats}")
    
    print("Database test completed!")
