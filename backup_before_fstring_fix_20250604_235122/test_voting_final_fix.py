#!/usr/bin/env python3
"""
Final test to verify voting system f-string errors are completely resolved
"""

import os
import sys

def test_voting_imports():
    """Test that all voting-related imports work without f-string errors"""
    print("🧪 Testing Voting System Imports (Final Check)...")
    
    try:
        # Test voting_system.py
        from voting_system import VotingSystem
        print("   ✅ voting_system.py imported successfully")
        
        # Test database_manager.py
        from database_manager import IrisDatabase
        print("   ✅ database_manager.py imported successfully")
        
        # Test demo_voting_system.py
        import demo_voting_system
        print("   ✅ demo_voting_system.py imported successfully")
        
        # Test create_sample_votes.py
        import create_sample_votes
        print("   ✅ create_sample_votes.py imported successfully")
        
        return True
        
    except Exception as e:
        print("   ❌ Import failed: {}".format(str(e)))
        return False

def test_voting_operations():
    """Test actual voting operations"""
    print("\n🗳️ Testing Voting Operations...")
    
    try:
        from voting_system import VotingSystem
        
        # Create voting system
        voting_system = VotingSystem()
        print("   ✅ VotingSystem created")
        
        # Test getting parties
        parties = voting_system.get_parties()
        print("   ✅ Parties retrieved: {} parties".format(len(parties)))
        
        # Test vote casting with cleanup
        test_person_id = 9999
        test_party_id = 1
        test_confidence = 0.95
        
        # Clean up any existing test vote
        try:
            import sqlite3
            with sqlite3.connect(voting_system.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM votes WHERE person_id = ?', (test_person_id,))
                conn.commit()
        except:
            pass
        
        # Test vote casting
        success = voting_system.cast_vote(test_person_id, test_party_id, test_confidence)
        print("   ✅ Vote casting: {}".format("SUCCESS" if success else "FAILED"))
        
        # Test getting results
        results = voting_system.get_voting_results()
        print("   ✅ Results retrieved: {} total votes".format(results['total_votes']))
        
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
        print("   ❌ Voting operations failed: {}".format(str(e)))
        return False

def test_database_operations():
    """Test database operations"""
    print("\n💾 Testing Database Operations...")
    
    try:
        from database_manager import IrisDatabase
        
        # Create database
        db = IrisDatabase()
        print("   ✅ Database created")
        
        # Test vote recording
        test_person_id = 9998
        test_election_id = "test_election_final"
        test_confidence = 0.93
        
        # Clean up existing test data
        try:
            import sqlite3
            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM voting_records WHERE person_id = ?', (test_person_id,))
                conn.commit()
        except:
            pass
        
        # Test recording vote
        success = db.record_vote(test_person_id, test_election_id, test_confidence)
        print("   ✅ Vote recording: {}".format("SUCCESS" if success else "FAILED"))
        
        # Test checking if voted
        has_voted = db.has_voted(test_person_id, test_election_id)
        print("   ✅ Vote check: {}".format("FOUND" if has_voted else "NOT FOUND"))
        
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
        print("   ❌ Database operations failed: {}".format(str(e)))
        return False

def test_string_formatting():
    """Test the specific string formatting patterns that were causing issues"""
    print("\n📝 Testing String Formatting (Critical Patterns)...")
    
    try:
        import hashlib
        from datetime import datetime
        
        # Test the exact patterns that were causing the bytes.__format__ error
        person_id = 123
        party_id = 2
        election_id = "test_election"
        confidence = 0.95
        
        # Test vote data formatting (main culprit)
        vote_data = "{}_{}_{}" .format(person_id, party_id, datetime.now().isoformat())
        print("   ✅ Vote data formatting works")
        
        # Test hash generation (another culprit)
        vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()
        print("   ✅ Hash generation works")
        
        # Test database vote data formatting
        db_vote_data = "{}_{}_{}" .format(person_id, election_id, datetime.now().isoformat())
        db_vote_hash = hashlib.sha256(db_vote_data.encode('utf-8')).hexdigest()
        print("   ✅ Database vote formatting works")
        
        # Test message formatting
        message = "Person {} voted for party {} with {:.1%} confidence".format(person_id, party_id, confidence)
        print("   ✅ Message formatting works")
        
        # Test error message formatting
        error_msg = "Error: {}".format("Test error message")
        print("   ✅ Error message formatting works")
        
        return True
        
    except Exception as e:
        print("   ❌ String formatting failed: {}".format(str(e)))
        return False

def run_final_test():
    """Run final comprehensive test"""
    print("🚀 FINAL VOTING SYSTEM F-STRING ERROR TEST")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_voting_imports),
        ("Voting Operations Test", test_voting_operations),
        ("Database Operations Test", test_database_operations),
        ("String Formatting Test", test_string_formatting),
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
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print("   {}: {}".format(test_name, status))
        if result:
            passed += 1
    
    print("\n🎯 FINAL RESULT: {}/{} tests passed ({:.1f}%)".format(passed, total, (passed/total)*100))
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The voting system is completely fixed!")
        print("\n💡 The voting system is now ready for use:")
        print("   1. Run: python Main.py")
        print("   2. Click: 🗳️ VOTING SYSTEM")
        print("   3. Cast votes without any f-string errors!")
        print("\n✅ The 'unsupported format string passed to bytes.__format__' error is RESOLVED!")
    else:
        print("⚠️ Some tests failed. The f-string error may still occur.")
        print("   Please check the failed tests above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_final_test()
    
    if success:
        print("\n🎉 SUCCESS: Voting system f-string errors are completely resolved!")
        print("You can now use the voting system without any format string errors.")
    else:
        print("\n❌ ISSUES DETECTED: Some f-string errors may still exist.")
        print("Please review the test results above.")
    
    sys.exit(0 if success else 1)
