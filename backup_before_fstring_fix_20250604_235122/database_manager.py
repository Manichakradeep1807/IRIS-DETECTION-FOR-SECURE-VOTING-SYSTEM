"""
Database Management System for Iris Recognition
Handles person enrollment, access logs, and system data
"""

import sqlite3
import numpy as np
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
import logging
from contextlib import contextmanager
import pickle
import base64

logger = logging.getLogger(__name__)

class IrisDatabase:
    """
    Comprehensive database manager for iris recognition system
    """
    
    def __init__(self, db_path='iris_system.db'):
        self.db_path = db_path
        self.init_database()
        logger.info("Database initialized: {}".format(db_path))
    
    def init_database(self):
        """Initialize all database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Persons table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    department TEXT,
                    role TEXT,
                    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_access TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    iris_template BLOB,
                    face_template BLOB,
                    metadata TEXT
                )
            ''')
            
            # Access logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER,
                    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_type TEXT,  -- 'entry', 'exit', 'voting', 'authentication'
                    confidence_score REAL,
                    access_granted BOOLEAN,
                    location TEXT,
                    device_id TEXT,
                    error_message TEXT,
                    additional_data TEXT,
                    FOREIGN KEY (person_id) REFERENCES persons (id)
                )
            ''')
            
            # System settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_name TEXT UNIQUE NOT NULL,
                    setting_value TEXT NOT NULL,
                    setting_type TEXT DEFAULT 'string',
                    description TEXT,
                    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Voting records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS voting_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER,
                    vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    election_id TEXT,
                    vote_hash TEXT,
                    confidence_score REAL,
                    verification_method TEXT,
                    FOREIGN KEY (person_id) REFERENCES persons (id)
                )
            ''')
            
            # Model versions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS model_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version_name TEXT NOT NULL,
                    model_path TEXT NOT NULL,
                    accuracy REAL,
                    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 0,
                    model_metadata TEXT
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_access_logs_person_id ON access_logs(person_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_access_logs_time ON access_logs(access_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_persons_email ON persons(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_voting_person_id ON voting_records(person_id)')
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error("Database error: {}".format(str(e)))
            raise
        finally:
            conn.close()
    
    def enroll_person(self, 
                     name: str, 
                     iris_template: np.ndarray,
                     email: Optional[str] = None,
                     phone: Optional[str] = None,
                     department: Optional[str] = None,
                     role: Optional[str] = None,
                     face_template: Optional[np.ndarray] = None,
                     metadata: Optional[Dict] = None) -> int:
        """Enroll a new person in the system"""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Serialize templates
            iris_blob = pickle.dumps(iris_template) if iris_template is not None else None
            face_blob = pickle.dumps(face_template) if face_template is not None else None
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute('''
                INSERT INTO persons 
                (name, email, phone, department, role, iris_template, face_template, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, department, role, iris_blob, face_blob, metadata_json))
            
            person_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Person enrolled: {name} (ID: {person_id})")
            return person_id
    
    def get_person(self, person_id: int) -> Optional[Dict]:
        """Get person information by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM persons WHERE id = ?', (person_id,))
            row = cursor.fetchone()
            
            if row:
                person = dict(row)
                # Deserialize templates
                if person['iris_template']:
                    person['iris_template'] = pickle.loads(person['iris_template'])
                if person['face_template']:
                    person['face_template'] = pickle.loads(person['face_template'])
                if person['metadata']:
                    person['metadata'] = json.loads(person['metadata'])
                
                return person
            return None
    
    def get_all_persons(self, active_only: bool = True) -> List[Dict]:
        """Get all persons in the system"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = 'SELECT * FROM persons'
            if active_only:
                query += ' WHERE is_active = 1'
            query += ' ORDER BY name'
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            persons = []
            for row in rows:
                person = dict(row)
                # Don't load templates for list view (performance)
                person['iris_template'] = None
                person['face_template'] = None
                if person['metadata']:
                    person['metadata'] = json.loads(person['metadata'])
                persons.append(person)
            
            return persons
    
    def update_person(self, person_id: int, **kwargs) -> bool:
        """Update person information"""
        if not kwargs:
            return False
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Handle special fields
            if 'iris_template' in kwargs and kwargs['iris_template'] is not None:
                kwargs['iris_template'] = pickle.dumps(kwargs['iris_template'])
            if 'face_template' in kwargs and kwargs['face_template'] is not None:
                kwargs['face_template'] = pickle.dumps(kwargs['face_template'])
            if 'metadata' in kwargs and kwargs['metadata'] is not None:
                kwargs['metadata'] = json.dumps(kwargs['metadata'])
            
            # Build update query
            set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
            values = list(kwargs.values()) + [person_id]
            
            cursor.execute(f'UPDATE persons SET {set_clause} WHERE id = ?', values)
            conn.commit()
            
            return cursor.rowcount > 0
    
    def deactivate_person(self, person_id: int) -> bool:
        """Deactivate a person (soft delete)"""
        return self.update_person(person_id, is_active=False)
    
    def log_access(self, 
                   person_id: int,
                   access_type: str,
                   confidence_score: float,
                   access_granted: bool,
                   location: Optional[str] = None,
                   device_id: Optional[str] = None,
                   error_message: Optional[str] = None,
                   additional_data: Optional[Dict] = None) -> int:
        """Log an access attempt"""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            additional_json = json.dumps(additional_data) if additional_data else None
            
            cursor.execute('''
                INSERT INTO access_logs 
                (person_id, access_type, confidence_score, access_granted, 
                 location, device_id, error_message, additional_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (person_id, access_type, confidence_score, access_granted,
                  location, device_id, error_message, additional_json))
            
            log_id = cursor.lastrowid
            
            # Update last access time for person
            if access_granted:
                cursor.execute(
                    'UPDATE persons SET last_access = CURRENT_TIMESTAMP WHERE id = ?',
                    (person_id,)
                )
            
            conn.commit()
            return log_id
    
    def record_vote(self, 
                   person_id: int,
                   election_id: str,
                   confidence_score: float,
                   verification_method: str = 'iris') -> bool:
        """Record a vote"""
        
        # Check if person already voted
        if self.has_voted(person_id, election_id):
            return False
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create vote hash for verification
            vote_data = "{}_{}_{}" .format(person_id, election_id, datetime.now().isoformat())
            vote_hash = hashlib.sha256(vote_data.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO voting_records 
                (person_id, election_id, vote_hash, confidence_score, verification_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (person_id, election_id, vote_hash, confidence_score, verification_method))
            
            conn.commit()
            return True
    
    def has_voted(self, person_id: int, election_id: str) -> bool:
        """Check if person has already voted"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM voting_records 
                WHERE person_id = ? AND election_id = ?
            ''', (person_id, election_id))
            
            count = cursor.fetchone()[0]
            return count > 0
    
    def get_access_history(self, 
                          person_id: Optional[int] = None,
                          hours: int = 24,
                          access_type: Optional[str] = None) -> List[Dict]:
        """Get access history"""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT al.*, p.name, p.department 
                FROM access_logs al
                LEFT JOIN persons p ON al.person_id = p.id
                WHERE al.access_time > datetime('now', '-{} hours')
            '''.format(hours)
            
            params = []
            
            if person_id:
                query += ' AND al.person_id = ?'
                params.append(person_id)
            
            if access_type:
                query += ' AND al.access_type = ?'
                params.append(access_type)
            
            query += ' ORDER BY al.access_time DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            history = []
            for row in rows:
                record = dict(row)
                if record['additional_data']:
                    record['additional_data'] = json.loads(record['additional_data'])
                history.append(record)
            
            return history
    
    def get_system_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total persons
            cursor.execute('SELECT COUNT(*) FROM persons WHERE is_active = 1')
            total_persons = cursor.fetchone()[0]
            
            # Access attempts today
            cursor.execute('''
                SELECT COUNT(*) FROM access_logs 
                WHERE date(access_time) = date('now')
            ''')
            today_attempts = cursor.fetchone()[0]
            
            # Successful accesses today
            cursor.execute('''
                SELECT COUNT(*) FROM access_logs 
                WHERE date(access_time) = date('now') AND access_granted = 1
            ''')
            today_success = cursor.fetchone()[0]
            
            # Votes today
            cursor.execute('''
                SELECT COUNT(*) FROM voting_records 
                WHERE date(vote_time) = date('now')
            ''')
            today_votes = cursor.fetchone()[0]
            
            # Average confidence score
            cursor.execute('''
                SELECT AVG(confidence_score) FROM access_logs 
                WHERE access_granted = 1 AND access_time > datetime('now', '-24 hours')
            ''')
            avg_confidence = cursor.fetchone()[0] or 0
            
            return {
                'total_persons': total_persons,
                'today_attempts': today_attempts,
                'today_success': today_success,
                'today_votes': today_votes,
                'success_rate': (today_success / today_attempts * 100) if today_attempts > 0 else 0,
                'average_confidence': round(avg_confidence, 3)
            }
    
    def get_setting(self, setting_name: str, default_value: str = None) -> str:
        """Get system setting"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT setting_value FROM system_settings WHERE setting_name = ?',
                (setting_name,)
            )
            row = cursor.fetchone()
            return row[0] if row else default_value
    
    def set_setting(self, setting_name: str, setting_value: str, 
                   setting_type: str = 'string', description: str = None):
        """Set system setting"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO system_settings 
                (setting_name, setting_value, setting_type, description, last_modified)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (setting_name, setting_value, setting_type, description))
            conn.commit()
    
    def cleanup_old_logs(self, days: int = 90):
        """Clean up old access logs"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM access_logs 
                WHERE access_time < datetime('now', '-{} days')
            '''.format(days))
            
            deleted_count = cursor.rowcount
            conn.commit()
            
            logger.info("Cleaned up {} old access logs".format(deleted_count))
            return deleted_count
    
    def backup_database(self, backup_path: str):
        """Create database backup"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
        logger.info("Database backed up to: {}".format(backup_path))
    
    def export_data(self, table_name: str, output_path: str):
        """Export table data to JSON"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM {}'.format(table_name))
            rows = cursor.fetchall()
            
            data = [dict(row) for row in rows]
            
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info("Exported {} records from {} to {}".format(len(data), table_name, output_path))

# Global database instance
db = IrisDatabase()

if __name__ == "__main__":
    # Test database functionality
    print("Testing database functionality...")
    
    # Test person enrollment
    test_template = np.random.rand(256).astype(np.float32)
    person_id = db.enroll_person(
        name="Test User",
        iris_template=test_template,
        email="test@example.com",
        department="IT"
    )
    print("Enrolled person with ID: {}".format(person_id))
    
    # Test access logging
    log_id = db.log_access(
        person_id=person_id,
        access_type="authentication",
        confidence_score=0.95,
        access_granted=True,
        location="Main Entrance"
    )
    print("Logged access with ID: {}".format(log_id))

    # Test statistics
    stats = db.get_system_statistics()
    print("System statistics: {}".format(stats))
    
    print("Database test completed successfully!")
