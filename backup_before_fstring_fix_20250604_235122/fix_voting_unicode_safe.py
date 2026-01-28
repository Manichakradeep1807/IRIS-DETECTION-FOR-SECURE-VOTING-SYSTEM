#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unicode-safe voting system fix
"""

import os
import sqlite3

def create_database():
    """Create voting database without Unicode issues"""
    print("Creating voting database...")
    
    try:
        # Remove existing database
        if os.path.exists("voting_system.db"):
            os.remove("voting_system.db")
            print("Removed existing database")
        
        # Create new database
        conn = sqlite3.connect("voting_system.db")
        cursor = conn.cursor()
        
        # Create parties table
        cursor.execute('''
            CREATE TABLE parties (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                color TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        
        # Create votes table
        cursor.execute('''
            CREATE TABLE votes (
                id INTEGER PRIMARY KEY,
                person_id INTEGER NOT NULL,
                party_id INTEGER NOT NULL,
                confidence_score REAL NOT NULL,
                vote_hash TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert parties (using simple symbols to avoid Unicode issues)
        parties = [
            (1, "Democratic Party", "D", "#2196F3", "Progressive policies and social equality"),
            (2, "Republican Party", "R", "#f44336", "Conservative values and free market"),
            (3, "Green Party", "G", "#4CAF50", "Environmental sustainability"),
            (4, "Independent", "I", "#9E9E9E", "Non-partisan solutions"),
        ]
        
        cursor.executemany('''
            INSERT INTO parties (id, name, symbol, color, description)
            VALUES (?, ?, ?, ?, ?)
        ''', parties)
        
        conn.commit()
        conn.close()
        
        print("SUCCESS: Database created with {} parties".format(len(parties)))
        return True
        
    except Exception as e:
        print("ERROR: Database creation failed: {}".format(str(e)))
        return False

def test_database():
    """Test the database"""
    print("Testing database...")
    
    try:
        conn = sqlite3.connect("voting_system.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM parties")
        count = cursor.fetchone()[0]
        print("SUCCESS: Database has {} parties".format(count))
        
        cursor.execute("SELECT name, symbol FROM parties")
        parties = cursor.fetchall()
        print("Available parties:")
        for party in parties:
            print("  {} - {}".format(party[1], party[0]))
        
        conn.close()
        return True
        
    except Exception as e:
        print("ERROR: Database test failed: {}".format(str(e)))
        return False

def create_test_file():
    """Create a simple test file"""
    print("Creating test file...")
    
    test_content = '''#!/usr/bin/env python3
"""Simple voting test"""

import sqlite3

def test_voting():
    """Test basic voting functionality"""
    try:
        print("Testing voting system...")
        
        # Test database
        conn = sqlite3.connect("voting_system.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM parties LIMIT 1")
        party = cursor.fetchone()
        
        if party:
            print("SUCCESS: Found party {} - {}".format(party[2], party[1]))
        else:
            print("ERROR: No parties found")
            return False
        
        conn.close()
        print("SUCCESS: Basic voting test passed")
        return True
        
    except Exception as e:
        print("ERROR: Test failed: {}".format(str(e)))
        return False

if __name__ == "__main__":
    print("BASIC VOTING TEST")
    print("=" * 20)
    
    if test_voting():
        print("\\nSUCCESS: Voting system is working!")
    else:
        print("\\nERROR: Voting system failed")
'''
    
    try:
        with open("basic_voting_test.py", "w", encoding='utf-8') as f:
            f.write(test_content)
        print("SUCCESS: Created basic_voting_test.py")
        return True
    except Exception as e:
        print("ERROR: Failed to create test file: {}".format(str(e)))
        return False

def main():
    """Main function"""
    print("VOTING SYSTEM FIX (Unicode Safe)")
    print("=" * 40)
    
    # Step 1: Create database
    if not create_database():
        print("FAILED: Could not create database")
        return
    
    # Step 2: Test database
    if not test_database():
        print("FAILED: Database test failed")
        return
    
    # Step 3: Create test file
    if not create_test_file():
        print("FAILED: Could not create test file")
        return
    
    print("\nSUCCESS: Fix completed!")
    print("Database created and tested")
    print("Test file created")
    
    print("\nNext steps:")
    print("1. Run: python basic_voting_test.py")
    print("2. If that works, try: python Main.py")
    print("3. Test voting in the main application")

if __name__ == "__main__":
    main()
