"""
Registration staging database to decouple signup from main DB linking.
Stores registrations, OTPs, and pending person link tasks.
"""

import sqlite3
from typing import Optional, Dict
from datetime import datetime


class RegistrationDB:
    def __init__(self, db_path: str = 'registration.db'):
        self.db_path = db_path
        self._init()

    def _init(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    display_name TEXT,
                    phone TEXT,
                    gov_id TEXT,
                    id_type TEXT,
                    password_hash TEXT,
                    otp_code TEXT,
                    verified INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS pending_links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    person_id INTEGER NOT NULL,
                    status TEXT DEFAULT 'pending',
                    last_error TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def upsert_registration(self, username: str, display_name: str, phone: str, gov_id: str, id_type: str, password_hash: str, otp_code: str):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO registrations (username, display_name, phone, gov_id, id_type, password_hash, otp_code, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                ON CONFLICT(username) DO UPDATE SET
                    display_name=excluded.display_name,
                    phone=excluded.phone,
                    gov_id=excluded.gov_id,
                    id_type=excluded.id_type,
                    password_hash=excluded.password_hash,
                    otp_code=excluded.otp_code,
                    verified=0
            ''', (username, display_name, phone, gov_id, id_type, password_hash, otp_code))
            conn.commit()

    def get_registration(self, username: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM registrations WHERE username = ?', (username,))
            row = c.fetchone()
            return dict(row) if row else None

    def mark_verified(self, username: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE registrations SET verified = 1 WHERE username = ?', (username,))
            conn.commit()
            return c.rowcount > 0

    def add_pending_link(self, username: str, person_id: int, error: str = None):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO pending_links (username, person_id, status, last_error) VALUES (?, ?, ?, ?)', (username, person_id, 'pending', error))
            conn.commit()

    def list_pending(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM pending_links WHERE status = "pending" ORDER BY created_at ASC')
            return [dict(r) for r in c.fetchall()]

    def mark_linked(self, pending_id: int):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE pending_links SET status = "linked", last_error = NULL WHERE id = ?', (pending_id,))
            conn.commit()

    def mark_error(self, pending_id: int, error: str):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE pending_links SET last_error = ?, status = "pending" WHERE id = ?', (error, pending_id))
            conn.commit()


regdb = RegistrationDB()





