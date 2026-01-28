#!/usr/bin/env python3
"""
Comprehensive diagnosis for vote casting issues
"""

import os
import sqlite3
import traceback

def check_database_status():
    """Check if voting database exists and is properly initialized"""
    print("🔍 Checking database status...")
    
    try:
        db_path = "voting_system.db"
        
        if not os.path.exists(db_path):
            print("❌ Database file does not exist: {}".format(db_path))
            return False
        
        print("✅ Database file exists: {}".format(db_path))
        
        # Check database structure
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("📊 Tables found: {}".format([table[0] for table in tables]))
            
            # Check parties table
            if ('parties',) in tables:
                cursor.execute("SELECT COUNT(*) FROM parties")
                party_count = cursor.fetchone()[0]
                print("✅ Parties table has {} entries".format(party_count))
                
                if party_count > 0:
                    cursor.execute("SELECT id, name, symbol FROM parties LIMIT 3")
                    sample_parties = cursor.fetchall()
                    print("   Sample parties:")
                    for party in sample_parties:
                        print("     ID: {}, Name: {}, Symbol: {}".format(party[0], party[1], party[2]))
                else:
                    print("⚠️ Parties table is empty!")
                    return False
            else:
                print("❌ Parties table does not exist!")
                return False
            
            # Check votes table
            if ('votes',) in tables:
                cursor.execute("SELECT COUNT(*) FROM votes")
                vote_count = cursor.fetchone()[0]
                print("✅ Votes table has {} entries".format(vote_count))
            else:
                print("❌ Votes table does not exist!")
                return False
        
        return True
        
    except Exception as e:
        print("❌ Database check error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_voting_system_import():
    """Test if voting system can be imported and initialized"""
    print("\n🔍 Testing voting system import...")
    
    try:
        from voting_system import VotingSystem, voting_system
        print("✅ VotingSystem imported successfully")
        
        # Test getting parties
        parties = voting_system.get_parties()
        print("✅ Got {} parties from voting system".format(len(parties)))
        
        if len(parties) == 0:
            print("❌ No parties available for voting!")
            return False
        
        # Show sample party
        sample_party = parties[0]
        print("   Sample party: {} {} - {}".format(
            sample_party['symbol'], 
            sample_party['name'], 
            sample_party['description'][:50] + "..."
        ))
        
        return True
        
    except Exception as e:
        print("❌ Import error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_vote_casting():
    """Test the actual vote casting functionality"""
    print("\n🔍 Testing vote casting functionality...")
    
    try:
        from voting_system import voting_system
        
        # Test parameters
        test_person_id = 999
        test_party_id = 1
        test_confidence = 0.95
        
        print("Testing with:")
        print("  Person ID: {}".format(test_person_id))
        print("  Party ID: {}".format(test_party_id))
        print("  Confidence: {:.1%}".format(test_confidence))
        
        # Check if person has already voted
        has_voted_before = voting_system.has_voted(test_person_id)
        print("  Already voted: {}".format(has_voted_before))
        
        if has_voted_before:
            print("⚠️ Test person has already voted. Checking existing vote...")
            existing_vote = voting_system.get_vote_by_person(test_person_id)
            if existing_vote:
                print("   Existing vote: {} {} at {}".format(
                    existing_vote['symbol'],
                    existing_vote['party'],
                    existing_vote['timestamp']
                ))
            
            # For testing, let's try a different person ID
            test_person_id = 998
            print("  Trying different person ID: {}".format(test_person_id))
            has_voted_before = voting_system.has_voted(test_person_id)
            print("  Already voted: {}".format(has_voted_before))
        
        if not has_voted_before:
            print("🗳️ Attempting to cast vote...")
            success = voting_system.cast_vote(test_person_id, test_party_id, test_confidence)
            
            if success:
                print("✅ Vote cast successfully!")
                
                # Verify the vote was recorded
                vote_info = voting_system.get_vote_by_person(test_person_id)
                if vote_info:
                    print("✅ Vote verified in database:")
                    print("   Party: {} {}".format(vote_info['symbol'], vote_info['party']))
                    print("   Time: {}".format(vote_info['timestamp']))
                    print("   Confidence: {:.1%}".format(vote_info['confidence']))
                else:
                    print("❌ Vote not found in database after casting!")
                    return False
            else:
                print("❌ Vote casting failed!")
                return False
        
        return True
        
    except Exception as e:
        print("❌ Vote casting error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_gui_components():
    """Test if GUI components can be created"""
    print("\n🔍 Testing GUI components...")
    
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Test basic tkinter
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        print("✅ Tkinter initialized successfully")
        
        # Test if voting interface functions exist
        from voting_system import show_voting_interface, show_enhanced_voting_interface
        print("✅ Voting interface functions imported")
        
        root.destroy()
        return True
        
    except Exception as e:
        print("❌ GUI component error: {}".format(str(e)))
        traceback.print_exc()
        return False

def initialize_database_if_needed():
    """Initialize database if it's missing or corrupted"""
    print("\n🔧 Checking if database needs initialization...")
    
    try:
        from voting_system import VotingSystem
        
        # Create a new instance to trigger initialization
        vs = VotingSystem()
        parties = vs.get_parties()
        
        if len(parties) == 0:
            print("⚠️ Database appears to be empty. This might be the issue.")
            print("💡 The voting system needs parties to be initialized.")
            return False
        
        print("✅ Database appears to be properly initialized")
        return True
        
    except Exception as e:
        print("❌ Database initialization error: {}".format(str(e)))
        traceback.print_exc()
        return False

def main():
    """Main diagnostic function"""
    print("🔧 VOTE CASTING DIAGNOSTIC")
    print("=" * 50)
    
    issues_found = []
    
    # Check 1: Database status
    if not check_database_status():
        issues_found.append("Database issues")
    
    # Check 2: Voting system import
    if not test_voting_system_import():
        issues_found.append("Import issues")
    
    # Check 3: GUI components
    if not test_gui_components():
        issues_found.append("GUI issues")
    
    # Check 4: Database initialization
    if not initialize_database_if_needed():
        issues_found.append("Database initialization")
    
    # Check 5: Vote casting
    if not test_vote_casting():
        issues_found.append("Vote casting functionality")
    
    # Summary
    print("\n" + "=" * 50)
    if len(issues_found) == 0:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Vote casting should work properly")
        print("\nTry running Main.py and testing the voting system")
    else:
        print("❌ ISSUES FOUND:")
        for issue in issues_found:
            print("  • {}".format(issue))
        
        print("\n💡 SUGGESTED FIXES:")
        if "Database issues" in issues_found:
            print("  • Run: python create_sample_votes.py")
        if "Import issues" in issues_found:
            print("  • Check Python dependencies")
        if "Vote casting functionality" in issues_found:
            print("  • Check console output for specific errors")

if __name__ == "__main__":
    main()
