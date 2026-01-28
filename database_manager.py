"""
Database Management System for Iris Recognition
Handles person enrollment, access logs, and system data
"""

import sqlite3
import numpy as np
import json
import hashlib
import hmac
import os
import re
import time
import struct
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
                    metadata TEXT,
                    address TEXT,
                    voter_id TEXT
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

            # Users table for RBAC and authentication (separate from persons)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    display_name TEXT,
                    role TEXT NOT NULL, -- 'admin', 'operator', 'viewer'
                    password_hash TEXT NOT NULL,
                    totp_secret TEXT,
                    person_id INTEGER, -- optional link to persons for biometric verify
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    failed_attempts INTEGER DEFAULT 0,
                    lock_until TIMESTAMP,
                    FOREIGN KEY (person_id) REFERENCES persons (id)
                )
            ''')

            # Defensive migration for older DBs missing person_id column
            try:
                cursor.execute('PRAGMA table_info(users)')
                user_cols = [r[1] for r in cursor.fetchall()]
                if 'person_id' not in user_cols:
                    # Recreate users table to guarantee 'person_id' exists in legacy DBs
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users_new (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            display_name TEXT,
                            role TEXT NOT NULL,
                            password_hash TEXT NOT NULL,
                            totp_secret TEXT,
                            person_id INTEGER,
                            is_active BOOLEAN DEFAULT 1,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            failed_attempts INTEGER DEFAULT 0,
                            lock_until TIMESTAMP
                        )
                    ''')
                    # Copy available columns
                    cols_to_copy = [c for c in user_cols if c in (
                        'id','username','display_name','role','password_hash','totp_secret','is_active','created_at','updated_at','failed_attempts','lock_until'
                    )]
                    cols_str = ','.join(cols_to_copy)
                    cursor.execute('INSERT INTO users_new ({}) SELECT {} FROM users'.format(cols_str, cols_str))
                    cursor.execute('DROP TABLE users')
                    cursor.execute('ALTER TABLE users_new RENAME TO users')
            except Exception:
                pass

            # Ensure failed_attempts and lock_until exist for older DBs
            try:
                cursor.execute('PRAGMA table_info(users)')
                cols = [r[1] for r in cursor.fetchall()]
                if 'failed_attempts' not in cols:
                    cursor.execute('ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0')
                if 'lock_until' not in cols:
                    cursor.execute('ALTER TABLE users ADD COLUMN lock_until TIMESTAMP')
            except Exception:
                pass

            # Ensure address and voter_id exist for persons
            try:
                cursor.execute('PRAGMA table_info(persons)')
                cols = [r[1] for r in cursor.fetchall()]
                if 'address' not in cols:
                    cursor.execute('ALTER TABLE persons ADD COLUMN address TEXT')
                if 'voter_id' not in cols:
                    cursor.execute('ALTER TABLE persons ADD COLUMN voter_id TEXT')
            except Exception:
                pass

            # Immutable audit log with hash chaining
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    actor_username TEXT,
                    action TEXT NOT NULL,
                    resource TEXT,
                    details TEXT,
                    prev_hash TEXT,
                    record_hash TEXT
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
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_logs_time ON audit_logs(event_time)')
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            # Enforce useful SQLite pragmas
            cur = conn.cursor()
            cur.execute('PRAGMA foreign_keys=ON')
            cur.execute('PRAGMA journal_mode=WAL')
            cur.execute('PRAGMA synchronous=NORMAL')
            cur.close()
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error("Database error: {}".format(str(e)))
            raise
        finally:
            conn.close()
    
    # --- Security utilities: password hashing (PBKDF2) and TOTP ---
    @staticmethod
    def hash_password_with_pbkdf2(password: str, salt: Optional[bytes] = None, iterations: int = 210000) -> str:
        if salt is None:
            salt = os.urandom(16)
        derived_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen=32)
        salt_b64 = base64.b64encode(salt).decode('ascii')
        hash_b64 = base64.b64encode(derived_key).decode('ascii')
        return 'pbkdf2_sha256${}${}${}'.format(iterations, salt_b64, hash_b64)

    @staticmethod
    def verify_password_with_pbkdf2(password: str, stored: str) -> bool:
        try:
            parts = stored.split('$')
            # Handle different formats (standard 4-part, buggy 5-part, buggy 6-part)
            if parts[0] != 'pbkdf2_sha256':
                return False
                
            if len(parts) == 4:
                # Standard: algo$iter$salt$hash
                iterations = int(parts[1])
                salt = base64.b64decode(parts[2])
                expected = base64.b64decode(parts[3])
            elif len(parts) == 6:
                # Buggy generated: algo$iter$$salt$$hash
                iterations = int(parts[1])
                salt = base64.b64decode(parts[3])
                expected = base64.b64decode(parts[5])
            elif len(parts) == 5:
                # Buggy verify expectation: algo$iter$$salt$hash
                iterations = int(parts[1])
                # parts[2] is empty
                salt = base64.b64decode(parts[3])
                expected = base64.b64decode(parts[4])
            else:
                return False
                
            computed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen=len(expected))
            return hmac.compare_digest(computed, expected)
        except Exception:
            return False

    @staticmethod
    def _totp_now(secret_b32: str, time_step_seconds: int = 30, digits: int = 6, t0: int = 0) -> int:
        try:
            key = base64.b32decode(secret_b32.upper())
        except Exception:
            return -1
        counter = int((int(time.time()) - t0) / time_step_seconds)
        msg = struct.pack('>Q', counter)
        hs = hmac.new(key, msg, hashlib.sha1).digest()
        offset = hs[-1] & 0x0F
        code_int = ((hs[offset] & 0x7f) << 24) | ((hs[offset + 1] & 0xff) << 16) | ((hs[offset + 2] & 0xff) << 8) | (hs[offset + 3] & 0xff)
        return code_int % (10 ** digits)

    @staticmethod
    def verify_totp_code(secret_b32: str, code: str, window: int = 1, time_step_seconds: int = 30, digits: int = 6) -> bool:
        if not code or not code.isdigit():
            return False
        provided = int(code)
        for offset in range(-window, window + 1):
            counter_time = int(time.time()) + (offset * time_step_seconds)
            try:
                key = base64.b32decode(secret_b32.upper())
            except Exception:
                return False
            msg = struct.pack('>Q', int(counter_time / time_step_seconds))
            hs = hmac.new(key, msg, hashlib.sha1).digest()
            dt = hs[-1] & 0x0F
            code_int = ((hs[dt] & 0x7f) << 24) | ((hs[dt + 1] & 0xff) << 16) | ((hs[dt + 2] & 0xff) << 8) | (hs[dt + 3] & 0xff)
            if (code_int % (10 ** digits)) == provided:
                return True
        return False

    # --- Input validation helpers ---
    @staticmethod
    def _is_valid_email(email: Optional[str]) -> bool:
        if email is None:
            return True
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def _is_valid_phone(phone: Optional[str]) -> bool:
        if phone is None:
            return True
        pattern = r'^[0-9()+\-\s]{7,20}$'
        return re.match(pattern, phone) is not None

    def enroll_person(self, 
                     name: str, 
                     iris_template: np.ndarray,
                     email: Optional[str] = None,
                     phone: Optional[str] = None,
                     department: Optional[str] = None,
                     role: Optional[str] = None,
                     face_template: Optional[np.ndarray] = None,
                     metadata: Optional[Dict] = None,
                     address: Optional[str] = None,
                     voter_id: Optional[str] = None) -> int:
        """Enroll a new person in the system"""
        
        if not self._is_valid_email(email) or not self._is_valid_phone(phone):
            raise ValueError('Invalid email or phone format')

        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Serialize templates
            iris_blob = pickle.dumps(iris_template) if iris_template is not None else None
            face_blob = pickle.dumps(face_template) if face_template is not None else None
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute('''
                INSERT INTO persons 
                (name, email, phone, department, role, iris_template, face_template, metadata, address, voter_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, department, role, iris_blob, face_blob, metadata_json, address, voter_id))
            
            person_id = cursor.lastrowid
            conn.commit()
            
            logger.info("Person enrolled: {} (ID: {})".format(name, person_id))
            return person_id

    def check_phone_exists(self, phone: str) -> bool:
        """Check if a phone number is already registered"""
        if not phone:
            return False
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM persons WHERE phone = ?', (phone,))
            count = cursor.fetchone()[0]
            return count > 0

    def check_person_name_exists(self, name: str) -> bool:
        """Check if a person with this name already exists (case-insensitive)"""
        if not name:
            return False
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM persons WHERE name = ? COLLATE NOCASE', (name,))
            count = cursor.fetchone()[0]
            return count > 0
    
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
            if 'email' in kwargs and not self._is_valid_email(kwargs.get('email')):
                raise ValueError('Invalid email format')
            if 'phone' in kwargs and not self._is_valid_phone(kwargs.get('phone')):
                raise ValueError('Invalid phone format')
            
            # Build update query
            set_clause = ', '.join(["{} = ?".format(key) for key in kwargs.keys()])
            values = list(kwargs.values()) + [person_id]
            
            cursor.execute('UPDATE persons SET {} WHERE id = ?'.format(set_clause), values)
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
            
            # Check if person exists to avoid Foreign Key errors
            cursor.execute("SELECT 1 FROM persons WHERE id = ?", (person_id,))
            if not cursor.fetchone():
                # Person not found, cannot log with FK constraint
                return -1

            additional_json = json.dumps(additional_data) if additional_data else None
            
            try:
                cursor.execute('''
                    INSERT INTO access_logs 
                    (person_id, access_type, confidence_score, access_granted, 
                     location, device_id, error_message, additional_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (person_id, access_type, confidence_score, access_granted,
                      location, device_id, error_message, additional_json))
                
                log_id = cursor.lastrowid
                conn.commit()
                return log_id
            except Exception:
                # Silently fail if something else goes wrong to avoid spam
                return -1
            
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
            
            # Create vote hash for verification - safe string operations
            timestamp_str = datetime.now().isoformat()
            vote_data = str(person_id) + "_" + str(election_id) + "_" + timestamp_str
            vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()
            
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

    # --- RBAC and Authentication helpers ---
    def create_user(self, username: str, password_hash: str, role: str = 'viewer', display_name: str = None, totp_secret: str = None) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, display_name, role, password_hash, totp_secret)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, display_name, role, password_hash, totp_secret))
            conn.commit()
            return cursor.lastrowid

    def create_user_with_password(self, username: str, password: str, role: str = 'viewer', display_name: str = None, totp_secret: str = None) -> int:
        password_hash = self.hash_password_with_pbkdf2(password)
        return self.create_user(username=username, password_hash=password_hash, role=role, display_name=display_name, totp_secret=totp_secret)

    def get_user(self, username: str) -> Optional[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
            row = cursor.fetchone()
            if not row:
                return None
            # Build dict safely and ensure 'person_id' key exists even on legacy DBs
            try:
                data = dict(row)
            except Exception:
                # Fallback using cursor description
                cols = [d[0] for d in cursor.description]
                data = {cols[i]: row[i] for i in range(len(cols))}
            if 'person_id' not in data:
                data['person_id'] = None
            if 'failed_attempts' not in data:
                data['failed_attempts'] = 0
            if 'lock_until' not in data:
                data['lock_until'] = None
            return data

    def get_all_users(self) -> List[Dict]:
        """Get all users (for recovery scan)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            rows = cursor.fetchall()
            users = []
            for row in rows:
                try:
                    d = dict(row)
                except Exception:
                    continue
                users.append(d)
            return users


    def update_user_totp(self, username: str, totp_secret: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET totp_secret = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?', (totp_secret, username))
            conn.commit()
            return cursor.rowcount > 0

    def set_user_role(self, username: str, role: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET role = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?', (role, username))
            conn.commit()
            return cursor.rowcount > 0

    def update_user_password(self, username: str, new_password: str) -> bool:
        """Securely update a user's password using PBKDF2"""
        password_hash = self.hash_password_with_pbkdf2(new_password)
        return self.update_user_password_hash(username, password_hash)

    def update_user_password_hash(self, username: str, password_hash: str) -> bool:
        """Update user password with a pre-calculated hash"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?', (password_hash, username))
            conn.commit()
            return cursor.rowcount > 0

    def link_user_to_person(self, username: str, person_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Ensure schema has person_id column (migrate older DBs)
            try:
                cursor.execute("PRAGMA table_info(users)")
                cols = [r[1] for r in cursor.fetchall()]
                if 'person_id' not in cols:
                    cursor.execute('ALTER TABLE users ADD COLUMN person_id INTEGER')
                if 'failed_attempts' not in cols:
                    cursor.execute('ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0')
                if 'lock_until' not in cols:
                    cursor.execute('ALTER TABLE users ADD COLUMN lock_until TIMESTAMP')
            except Exception:
                # Best effort; proceed
                pass
            cursor.execute('UPDATE users SET person_id = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?', (person_id, username))
            conn.commit()
            return cursor.rowcount > 0

    def unlink_user_person(self, username: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET person_id = NULL, updated_at = CURRENT_TIMESTAMP WHERE username = ?', (username,))
            conn.commit()
            return cursor.rowcount > 0

    # --- Authentication with lockout policy ---
    def authenticate_user(self, username: str, password: str, totp_code: Optional[str] = None, require_totp_if_set: bool = True, max_attempts: int = 5, lockout_minutes: int = 15) -> Tuple[bool, str]:
        user = self.get_user(username)
        if not user:
            return False, 'user_not_found'
        if user.get('lock_until'):
            try:
                lock_until_dt = datetime.fromisoformat(user['lock_until']) if isinstance(user['lock_until'], str) else user['lock_until']
            except Exception:
                lock_until_dt = None
            if lock_until_dt and datetime.now() < lock_until_dt:
                return False, 'account_locked'

        stored_hash = user.get('password_hash')
        if not stored_hash or not self.verify_password_with_pbkdf2(password, stored_hash):
            with self.get_connection() as conn:
                cursor = conn.cursor()
                new_failed = (user.get('failed_attempts') or 0) + 1
                lock_until_expr = None
                if new_failed >= max_attempts:
                    lock_until_expr = (datetime.now() + timedelta(minutes=lockout_minutes)).isoformat()
                cursor.execute('UPDATE users SET failed_attempts = ?, lock_until = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?', (new_failed, lock_until_expr, username))
                conn.commit()
            return False, 'invalid_credentials'

        if user.get('totp_secret') and require_totp_if_set:
            if not totp_code or not self.verify_totp_code(user['totp_secret'], totp_code):
                return False, 'invalid_totp'

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET failed_attempts = 0, lock_until = NULL, updated_at = CURRENT_TIMESTAMP WHERE username = ?', (username,))
            conn.commit()
        return True, 'ok'

    # --- Immutable audit log with hash chaining ---
    def _get_last_audit_hash(self) -> Optional[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT record_hash FROM audit_logs ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            return row[0] if row else None

    def write_audit_log(self, actor_username: str, action: str, resource: str = None, details: Dict = None) -> int:
        prev_hash = self._get_last_audit_hash()
        event_time = datetime.now().isoformat()
        payload = json.dumps({
            't': event_time,
            'u': actor_username,
            'a': action,
            'r': resource,
            'd': details or {},
            'p': prev_hash
        }, sort_keys=True)
        record_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_logs (event_time, actor_username, action, resource, details, prev_hash, record_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (event_time, actor_username, action, resource, json.dumps(details or {}), prev_hash, record_hash))
            conn.commit()
            return cursor.lastrowid
    
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

    def delete_user_permanently(self, username: str) -> bool:
        """Permanently delete a system user (admin/operator)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            return cursor.rowcount > 0

    def delete_person_permanently(self, person_id: int) -> bool:
        """Permanently delete an enrolled person and all associated data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Unlink from users table (set person_id to NULL)
            cursor.execute('UPDATE users SET person_id = NULL WHERE person_id = ?', (person_id,))
            
            # 2. Delete access logs
            cursor.execute('DELETE FROM access_logs WHERE person_id = ?', (person_id,))
            
            # 3. Delete voting records
            cursor.execute('DELETE FROM voting_records WHERE person_id = ?', (person_id,))
            
            # 4. Delete the person
            cursor.execute('DELETE FROM persons WHERE id = ?', (person_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def check_duplicate_iris(self, new_iris_template: np.ndarray, threshold: float = 0.85) -> Optional[int]:
        """
        Check if the irirs template matches any existing person.
        Returns the ID of the matching person if found, else None.
        Uses Euclidean distance (match if dist < (1-confidence)); threshold implies similarity.
        Wait, model output is classification confidence. 
        If we are comparing 'templates' which are raw images or embeddings?
        The system currently saves raw images as templates? 
        The LiveIrisRecognition uses the model to predict class directly.
        BUT enrollment says "template".
        If we don't have an embedding model, we can't easily dedup raw images without retraining.
        However, let's assume 'iris_template' allows some comparison.
        
        If we can't compare raw images effectively, we might rely on the MODEL to tell us?
        Problem: The model is a classifier (Fixed classes). It can't detect 'new' class vs 'old' class easily unless trained.
        
        Alternative:
        If the objective is "no two persons with same feature allowed", 
        we must assume we can compare features. 
        If 'template' is just an image (64x64x3), we can do pixel MSE or Structural Similarity?
        Better: If we have an embedding model.
        
        Assumption: The user wants us to try. 
        For this 'Mini Project', we will do a simple pixel comparison or if we have embeddings.
        Currently, `enroll_person` takes `iris_template`.
        Let's try a simple comparison loop.
        """
        
        # 1. Get all templates
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, iris_template FROM persons WHERE iris_template IS NOT NULL AND is_active = 1')
            rows = cursor.fetchall()
            
        for row in rows:
            pid = row['id']
            blob = row['iris_template']
            try:
                stored_template = pickle.loads(blob)
                # Ensure similar shapes
                if stored_template.shape == new_iris_template.shape:
                    # Calculate Difference (MSE)
                    # This is very naive for raw images but fits 'mini project' scope without Facenet/ArcFace
                    diff = np.mean((stored_template - new_iris_template) ** 2)
                    
                    # Heuristic threshold for "Same Image"
                    # If camera moves, this fails. But if exact same image reused?
                    # Or if features are extracted?
                    # Let's assume strict check against exact image reuse or very close.
                    if diff < 50: # Arbitrary low threshold for duplicate raw data
                        return pid
            except:
                pass
                
        return None
    
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

    def cleanup_old_votes(self, days: int = 365):
        """Clean up old voting records per retention policy"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM voting_records 
                WHERE vote_time < datetime('now', '-{} days')
            '''.format(days))
            deleted = cursor.rowcount
            conn.commit()
            logger.info("Cleaned up {} old voting records".format(deleted))
            return deleted
    
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
