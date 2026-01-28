#!/usr/bin/env python3
"""
COMPREHENSIVE VOTING ERROR TEST
Tests all voting system components to identify the exact source of the 
"unsupported format string passed to bytes.__format__" error
"""

import sys
import traceback
import os
from datetime import datetime

def test_imports():
    """Test all imports to identify problematic modules"""
    print("🔍 TESTING IMPORTS")
    print("=" * 50)
    
    try:
        print("1. Testing basic imports...")
        import sqlite3
        import hashlib
        import json
        print("   ✅ Basic imports successful")
        
        print("2. Testing tkinter imports...")
        import tkinter as tk
        from tkinter import messagebox
        print("   ✅ Tkinter imports successful")
        
        print("3. Testing voting system import...")
        from voting_system import voting_system
        print("   ✅ Voting system import successful")
        
        print("4. Testing voting results import...")
        from voting_results import show_voting_results
        print("   ✅ Voting results import successful")
        
        return True
        
    except Exception as e:
        print("   ❌ Import error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_voting_system_basic():
    """Test basic voting system operations"""
    print("\n🗳️ TESTING VOTING SYSTEM BASIC OPERATIONS")
    print("=" * 50)
    
    try:
        from voting_system import voting_system
        
        print("1. Testing get_parties()...")
        parties = voting_system.get_parties()
        print("   ✅ Parties retrieved: {} parties".format(len(parties)))
        
        print("2. Testing has_voted()...")
        has_voted = voting_system.has_voted(999)
        print("   ✅ Has voted check: {}".format(has_voted))
        
        print("3. Testing get_voting_results()...")
        results = voting_system.get_voting_results()
        print("   ✅ Results retrieved: {} total votes".format(results.get('total_votes', 0)))
        
        return True
        
    except Exception as e:
        print("   ❌ Basic operations error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_vote_casting():
    """Test vote casting operation that might cause the error"""
    print("\n🎯 TESTING VOTE CASTING")
    print("=" * 50)
    
    try:
        from voting_system import voting_system
        
        print("1. Testing vote casting with test person...")
        person_id = 9999  # Use a test ID
        party_id = 1
        confidence = 0.95
        
        # First, remove any existing vote for this test person
        print("   Cleaning up any existing test vote...")
        try:
            import sqlite3
            with sqlite3.connect(voting_system.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM votes WHERE person_id = ?', (person_id,))
                conn.commit()
            print("   ✅ Test cleanup completed")
        except:
            print("   ⚠️ Cleanup not needed or failed (non-critical)")
        
        print("2. Attempting to cast vote...")
        result = voting_system.cast_vote(person_id, party_id, confidence)
        print("   ✅ Vote casting result: {}".format('Success' if result else 'Failed'))
        
        if result:
            print("3. Verifying vote was recorded...")
            has_voted = voting_system.has_voted(person_id)
            print("   ✅ Vote verification: {}".format('Recorded' if has_voted else 'Not found'))
            
            print("4. Getting vote details...")
            vote_details = voting_system.get_vote_by_person(person_id)
            if vote_details:
                print("   ✅ Vote details retrieved successfully")
                print("   Party: {}".format(vote_details.get('party', 'Unknown')))
                print("   Confidence: {}".format(vote_details.get('confidence', 'Unknown')))
            else:
                print("   ⚠️ Vote details not found")
        
        return True
        
    except Exception as e:
        print("   ❌ Vote casting error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_string_operations():
    """Test string operations that might cause format errors"""
    print("\n📝 TESTING STRING OPERATIONS")
    print("=" * 50)
    
    try:
        import hashlib
        from datetime import datetime
        
        print("1. Testing vote data formatting...")
        person_id = 123
        party_id = 2
        
        # Test the exact pattern used in voting system
        vote_data = "{}_{}_{}" .format(person_id, party_id, datetime.now().isoformat())
        print("   ✅ Vote data format: {}...".format(vote_data[:50]))
        
        print("2. Testing hash generation...")
        vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()
        print("   ✅ Hash generation: {}...".format(vote_hash[:20]))
        
        print("3. Testing message formatting...")
        message = "Person {} voted for party {} with {:.1%} confidence".format(person_id, party_id, 0.95)
        print("   ✅ Message format: {}".format(message))
        
        print("4. Testing error message formatting...")
        error_msg = "Error: {}".format("Test error message")
        print("   ✅ Error format: {}".format(error_msg))
        
        return True
        
    except Exception as e:
        print("   ❌ String operations error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_gui_components():
    """Test GUI components that might cause the error"""
    print("\n🖥️ TESTING GUI COMPONENTS")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        print("1. Testing tkinter root creation...")
        root = tk.Tk()
        root.withdraw()  # Hide the window
        print("   ✅ Tkinter root created")
        
        print("2. Testing message box formatting...")
        # Test without actually showing the message box
        message = "Person {} voted for {}".format(123, "Test Party")
        print("   ✅ Message box format: {}".format(message))
        
        print("3. Testing voting interface components...")
        # Import and test voting interface functions
        try:
            from voting_system import show_enhanced_voting_interface
            print("   ✅ Voting interface import successful")
        except ImportError:
            print("   ⚠️ Voting interface not available (non-critical)")
        
        root.destroy()
        return True
        
    except Exception as e:
        print("   ❌ GUI components error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_database_operations():
    """Test database operations that might cause the error"""
    print("\n🗄️ TESTING DATABASE OPERATIONS")
    print("=" * 50)
    
    try:
        import sqlite3
        from voting_system import voting_system
        
        print("1. Testing database connection...")
        with sqlite3.connect(voting_system.db_path) as conn:
            cursor = conn.cursor()
            print("   ✅ Database connection successful")
            
            print("2. Testing table queries...")
            cursor.execute('SELECT COUNT(*) FROM parties')
            party_count = cursor.fetchone()[0]
            print("   ✅ Parties table: {} entries".format(party_count))
            
            cursor.execute('SELECT COUNT(*) FROM votes')
            vote_count = cursor.fetchone()[0]
            print("   ✅ Votes table: {} entries".format(vote_count))
        
        return True
        
    except Exception as e:
        print("   ❌ Database operations error: {}".format(str(e)))
        traceback.print_exc()
        return False

def main():
    """Run comprehensive voting error test"""
    print("🔧 COMPREHENSIVE VOTING ERROR TEST")
    print("=" * 60)
    print("Testing all components to identify the source of:")
    print("'unsupported format string passed to bytes.__format__' error")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Voting System Basic", test_voting_system_basic),
        ("Vote Casting", test_vote_casting),
        ("String Operations", test_string_operations),
        ("GUI Components", test_gui_components),
        ("Database Operations", test_database_operations)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print("\n❌ CRITICAL ERROR in {}: {}".format(test_name, str(e)))
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print("{}: {}".format(test_name, status))
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\nTotal: {} passed, {} failed".format(passed, failed))
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("The voting system appears to be working correctly.")
        print("If you're still experiencing errors, they might be:")
        print("1. Intermittent issues")
        print("2. Specific to certain user interactions")
        print("3. Related to specific data combinations")
    else:
        print("\n⚠️ ISSUES DETECTED!")
        print("The failed tests indicate where the problem might be.")
        print("Check the error messages above for specific details.")

if __name__ == "__main__":
    main()
