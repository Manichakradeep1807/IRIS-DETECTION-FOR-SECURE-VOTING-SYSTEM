#!/usr/bin/env python3
import os
import sqlite3

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
    print("Parties available:")
    for party in parties:
        print("  {} - {}".format(party[2], party[1]))

    print("\nDatabase file 'voting_system.db' created successfully!")
    print("You can now run 'python Main.py' and test the voting system.")

except Exception as e:
    print("ERROR: {}".format(str(e)))
    import traceback
    traceback.print_exc()
