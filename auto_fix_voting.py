#!/usr/bin/env python3
import os
import sqlite3

def create_database():
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
            (1, "Democratic Party", "D", "#2196F3", "Progressive policies"),
            (2, "Republican Party", "R", "#f44336", "Conservative values"),
            (3, "Green Party", "G", "#4CAF50", "Environmental focus"),
            (4, "Independent", "I", "#9E9E9E", "Non-partisan approach"),
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
        print("ERROR: {}".format(str(e)))
        return False

def test_voting_import():
    try:
        from voting_system import voting_system
        parties = voting_system.get_parties()
        print("SUCCESS: Voting system imported, {} parties found".format(len(parties)))
        return True
    except Exception as e:
        print("ERROR importing voting system: {}".format(str(e)))
        return False

def main():
    print("AUTOMATIC VOTING SYSTEM FIX")
    print("=" * 30)
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if create_database():
        print("Database creation: SUCCESS")
    else:
        print("Database creation: FAILED")
        return
    
    # Step 2: Test voting system
    print("\nStep 2: Testing voting system...")
    if test_voting_import():
        print("Voting system test: SUCCESS")
    else:
        print("Voting system test: FAILED")
    
    print("\nFIX COMPLETED!")
    print("Try running: python Main.py")
    print("Then click VOTING SYSTEM -> CAST VOTE (DIRECT)")

if __name__ == "__main__":
    main()
