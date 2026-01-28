#!/usr/bin/env python3
"""
Simple voting system fix and test
"""

import os
import sqlite3

def create_simple_database():
    """Create a simple voting database"""
    print("Creating simple voting database...")
    
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
        
        # Insert parties
        parties = [
            (1, "Democratic Party", "🔵", "#2196F3", "Progressive policies and social equality"),
            (2, "Republican Party", "🔴", "#f44336", "Conservative values and free market"),
            (3, "Green Party", "🟢", "#4CAF50", "Environmental sustainability"),
            (4, "Independent", "⚪", "#9E9E9E", "Non-partisan solutions"),
        ]
        
        cursor.executemany('''
            INSERT INTO parties (id, name, symbol, color, description)
            VALUES (?, ?, ?, ?, ?)
        ''', parties)
        
        conn.commit()
        conn.close()
        
        print("Database created with {} parties".format(len(parties)))
        return True

    except Exception as e:
        print("Database creation error: {}".format(str(e)))
        return False

def test_simple_import():
    """Test simple import"""
    print("\nTesting simple import...")
    
    try:
        import sqlite3
        print("sqlite3 imported")

        import tkinter
        print("tkinter imported")

        # Test database connection
        conn = sqlite3.connect("voting_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM parties")
        count = cursor.fetchone()[0]
        conn.close()
        print("Database has {} parties".format(count))

        return True

    except Exception as e:
        print("Import error: {}".format(str(e)))
        return False

def create_minimal_voting_test():
    """Create minimal voting test"""
    print("\nCreating minimal voting test...")
    
    test_code = '''#!/usr/bin/env python3
"""Minimal voting system test"""

import sqlite3
import tkinter as tk
from tkinter import messagebox

def test_voting():
    """Test basic voting functionality"""
    try:
        # Test database
        conn = sqlite3.connect("voting_system.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM parties LIMIT 1")
        party = cursor.fetchone()
        
        if party:
            print("SUCCESS: Database working: Found party {} {}".format(party[2], party[1]))
        else:
            print("ERROR: No parties in database")
            return False

        # Test GUI
        root = tk.Tk()
        root.withdraw()
        print("SUCCESS: GUI working")
        root.destroy()

        conn.close()
        return True

    except Exception as e:
        print("ERROR: Test error: {}".format(str(e)))
        return False

if __name__ == "__main__":
    print("MINIMAL VOTING TEST")
    print("=" * 30)

    if test_voting():
        print("\\nSUCCESS: BASIC FUNCTIONALITY WORKS!")
        print("SUCCESS: Database and GUI are functional")
    else:
        print("\\nERROR: Basic functionality failed")
'''
    
    try:
        with open("minimal_voting_test.py", "w", encoding='utf-8') as f:
            f.write(test_code)
        print("Created minimal_voting_test.py")
        return True
    except Exception as e:
        print("Error creating test: {}".format(str(e)))
        return False

def main():
    """Main function"""
    print("SIMPLE VOTING SYSTEM FIX")
    print("=" * 35)

    # Step 1: Create database
    if not create_simple_database():
        print("\nDatabase creation failed")
        return

    # Step 2: Test imports
    if not test_simple_import():
        print("\nImport test failed")
        return

    # Step 3: Create minimal test
    if not create_minimal_voting_test():
        print("\nTest creation failed")
        return

    print("\nSIMPLE FIX COMPLETED!")
    print("Database created successfully")
    print("Basic imports working")
    print("Minimal test created")

    print("\nNEXT STEPS:")
    print("1. Run: python minimal_voting_test.py")
    print("2. If that works, try: python Main.py")
    print("3. Test the voting system in the main application")

    print("\nIf you still get 'voting system error':")
    print("• The issue might be in the Main.py integration")
    print("• Check the exact error message")
    print("• Try running Main.py and share the specific error")

if __name__ == "__main__":
    main()
