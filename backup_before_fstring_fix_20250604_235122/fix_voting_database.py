#!/usr/bin/env python3
"""
Fix and initialize voting database
"""

import os
import sqlite3

def create_voting_database():
    """Create and initialize the voting database"""
    print("🔧 Creating voting database...")
    
    try:
        db_path = "voting_system.db"
        
        # Remove existing database if corrupted
        if os.path.exists(db_path):
            print("⚠️ Removing existing database...")
            os.remove(db_path)
        
        # Create new database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Create parties table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS parties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    color TEXT NOT NULL,
                    description TEXT NOT NULL
                )
            ''')
            
            # Create votes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS votes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER NOT NULL,
                    party_id INTEGER NOT NULL,
                    confidence_score REAL NOT NULL,
                    vote_hash TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (party_id) REFERENCES parties (id)
                )
            ''')
            
            # Insert sample parties
            parties_data = [
                ("Democratic Party", "🔵", "#2196F3", "Progressive policies focusing on social equality, healthcare reform, and environmental protection."),
                ("Republican Party", "🔴", "#f44336", "Conservative values emphasizing free market economics, traditional values, and strong national defense."),
                ("Green Party", "🟢", "#4CAF50", "Environmental sustainability, renewable energy, and ecological responsibility as core principles."),
                ("Libertarian Party", "🟡", "#FF9800", "Maximum individual freedom, minimal government intervention, and free market capitalism."),
                ("Independent", "⚪", "#9E9E9E", "Non-partisan approach focusing on practical solutions and bipartisan cooperation."),
                ("Socialist Party", "🟠", "#FF5722", "Economic equality, workers' rights, and public ownership of key industries."),
                ("Constitution Party", "🟤", "#795548", "Strict constitutional interpretation, limited federal government, and traditional moral values."),
                ("Reform Party", "🟣", "#9C27B0", "Political reform, campaign finance reform, and government accountability."),
            ]
            
            cursor.executemany('''
                INSERT INTO parties (name, symbol, color, description)
                VALUES (?, ?, ?, ?)
            ''', parties_data)
            
            conn.commit()
            
            # Verify creation
            cursor.execute("SELECT COUNT(*) FROM parties")
            party_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM votes")
            vote_count = cursor.fetchone()[0]
            
            print("✅ Database created successfully!")
            print("   Parties: {}".format(party_count))
            print("   Votes: {}".format(vote_count))
            
            return True
            
    except Exception as e:
        print("❌ Database creation error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """Test the created database"""
    print("\n🔍 Testing database...")
    
    try:
        from voting_system import VotingSystem
        
        # Create voting system instance
        vs = VotingSystem()
        
        # Test getting parties
        parties = vs.get_parties()
        print("✅ Got {} parties".format(len(parties)))
        
        if len(parties) > 0:
            print("   Sample parties:")
            for party in parties[:3]:
                print("     {} {} - {}".format(
                    party['symbol'], 
                    party['name'], 
                    party['description'][:40] + "..."
                ))
        
        # Test vote checking
        has_voted = vs.has_voted(999)
        print("✅ Vote checking works: {}".format(has_voted))
        
        # Test getting results
        results = vs.get_voting_results()
        print("✅ Results query works: {} total votes".format(results['total_votes']))
        
        return True
        
    except Exception as e:
        print("❌ Database test error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🔧 VOTING DATABASE FIX")
    print("=" * 30)
    
    # Step 1: Create database
    if not create_voting_database():
        print("\n❌ Failed to create database")
        return
    
    # Step 2: Test database
    if not test_database():
        print("\n❌ Database test failed")
        return
    
    print("\n🎉 VOTING DATABASE FIXED!")
    print("✅ Database created and tested successfully")
    print("\nNext steps:")
    print("1. Run 'python test_vote_casting_simple.py' to test voting")
    print("2. Run 'python Main.py' to use the full application")
    print("3. Try the voting system in the main application")

if __name__ == "__main__":
    main()
