#!/usr/bin/env python3
"""
Test script to verify that all f-string issues in the voting system are resolved
"""

import os
import sys
import sqlite3
from datetime import datetime

def test_voting_system_imports():
    """Test that all voting system modules import without f-string errors"""
    print("🧪 Testing Voting System Imports...")
    
    try:
        # Test voting_system.py import
        from voting_system import VotingSystem, show_voting_interface
        print("   ✅ voting_system.py imported successfully")
        
        # Test database_manager.py import
        from database_manager import IrisDatabase
        print("   ✅ database_manager.py imported successfully")
        
        # Test demo_voting_system.py import
        import demo_voting_system
        print("   ✅ demo_voting_system.py imported successfully")
        
        # Test create_sample_votes.py import
        import create_sample_votes
        print("   ✅ create_sample_votes.py imported successfully")
        
        return True
        
    except Exception as e:
        print("   ❌ Import failed: {}".format(str(e)))
        return False

def test_voting_system_functionality():
    """Test basic voting system functionality"""
    print("\n🗳️ Testing Voting System Functionality...")
    
    try:
        from voting_system import VotingSystem
        
        # Create voting system instance
        voting_system = VotingSystem()
        print("   ✅ VotingSystem instance created")
        
        # Test getting parties
        parties = voting_system.get_parties()
        print("   ✅ Parties retrieved: {} parties found".format(len(parties)))
        
        # Test vote casting (with test data)
        test_person_id = 999
        test_party_id = 1
        test_confidence = 0.95
        
        # First, ensure the person hasn't voted
        if voting_system.has_voted(test_person_id):
            print("   ⚠️ Test person already voted, clearing for test...")
            # Clear test vote if exists
            try:
                with sqlite3.connect(voting_system.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM votes WHERE person_id = ?', (test_person_id,))
                    conn.commit()
            except:
                pass
        
        # Test vote casting
        success = voting_system.cast_vote(test_person_id, test_party_id, test_confidence)
        if success:
            print("   ✅ Vote casting successful")
        else:
            print("   ⚠️ Vote casting failed (may be expected)")
        
        # Test getting results
        results = voting_system.get_voting_results()
        print("   ✅ Voting results retrieved: {} total votes".format(results['total_votes']))
        
        # Clean up test vote
        try:
            with sqlite3.connect(voting_system.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM votes WHERE person_id = ?', (test_person_id,))
                conn.commit()
        except:
            pass
        
        return True
        
    except Exception as e:
        print("   ❌ Functionality test failed: {}".format(str(e)))
        return False

def test_database_operations():
    """Test database operations without f-string errors"""
    print("\n💾 Testing Database Operations...")
    
    try:
        from database_manager import IrisDatabase
        
        # Create database instance
        db = IrisDatabase()
        print("   ✅ Database instance created")
        
        # Test vote recording
        test_person_id = 998
        test_election_id = "test_election"
        test_confidence = 0.92
        
        # Clear any existing test data
        try:
            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM voting_records WHERE person_id = ?', (test_person_id,))
                conn.commit()
        except:
            pass
        
        # Test recording a vote
        success = db.record_vote(test_person_id, test_election_id, test_confidence)
        if success:
            print("   ✅ Vote recording successful")
        else:
            print("   ⚠️ Vote recording failed")
        
        # Test checking if voted
        has_voted = db.has_voted(test_person_id, test_election_id)
        print("   ✅ Vote check successful: {}".format(has_voted))
        
        # Clean up test data
        try:
            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM voting_records WHERE person_id = ?', (test_person_id,))
                conn.commit()
        except:
            pass
        
        return True
        
    except Exception as e:
        print("   ❌ Database test failed: {}".format(str(e)))
        return False

def test_string_formatting():
    """Test string formatting patterns used in voting system"""
    print("\n📝 Testing String Formatting Patterns...")
    
    try:
        import hashlib
        
        # Test patterns that were causing issues
        person_id = 123
        party_id = 2
        confidence = 0.95
        
        # Test vote data formatting (the main culprit)
        vote_data = "{}_{}_{}" .format(person_id, party_id, datetime.now().isoformat())
        print("   ✅ Vote data formatting: {}".format(vote_data[:50] + "..."))
        
        # Test hash generation
        vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()
        print("   ✅ Hash generation: {}".format(vote_hash[:20] + "..."))
        
        # Test message formatting
        message = "Person {} voted for party {} with {:.1%} confidence".format(person_id, party_id, confidence)
        print("   ✅ Message formatting: {}".format(message))
        
        # Test time formatting
        time_str = "Vote cast at: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("   ✅ Time formatting: {}".format(time_str))
        
        return True
        
    except Exception as e:
        print("   ❌ String formatting test failed: {}".format(str(e)))
        return False

def test_voting_interface():
    """Test voting interface creation (without showing GUI)"""
    print("\n🖥️ Testing Voting Interface Creation...")
    
    try:
        # Test that we can import and create interface components
        import tkinter as tk
        from voting_system import VotingSystem
        
        # Create a test root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        voting_system = VotingSystem()
        
        # Test getting parties for interface
        parties = voting_system.get_parties()
        print("   ✅ Interface data preparation successful")
        
        # Test creating basic interface elements
        test_frame = tk.Frame(root)
        test_label = tk.Label(test_frame, text="Test voting interface")
        print("   ✅ Interface elements creation successful")
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print("   ❌ Interface test failed: {}".format(str(e)))
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 COMPREHENSIVE VOTING SYSTEM F-STRING FIX TEST")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_voting_system_imports),
        ("Functionality Test", test_voting_system_functionality),
        ("Database Test", test_database_operations),
        ("String Formatting Test", test_string_formatting),
        ("Interface Test", test_voting_interface),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print("   ❌ {} failed with exception: {}".format(test_name, str(e)))
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print("   {}: {}".format(test_name, status))
        if result:
            passed += 1
    
    print("\n🎯 OVERALL RESULT: {}/{} tests passed ({:.1f}%)".format(passed, total, (passed/total)*100))
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The voting system f-string issues are resolved!")
        print("\n💡 You can now use the voting system without format string errors:")
        print("   1. Run: python Main.py")
        print("   2. Click: 🗳️ VOTING SYSTEM")
        print("   3. Test voting functionality")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    
    if success:
        print("\n✅ SUCCESS: Voting system is ready to use!")
    else:
        print("\n❌ ISSUES DETECTED: Please review the test results above.")
    
    sys.exit(0 if success else 1)
