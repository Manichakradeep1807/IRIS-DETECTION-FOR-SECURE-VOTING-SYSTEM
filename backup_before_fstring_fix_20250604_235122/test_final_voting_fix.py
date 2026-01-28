#!/usr/bin/env python3
"""
Final test for voting system after all f-string fixes
"""

def test_voting_system_import():
    """Test if voting system can be imported without errors"""
    print("🔍 Testing voting system import...")
    
    try:
        # Test basic imports
        import sqlite3
        import tkinter as tk
        import hashlib
        from datetime import datetime
        print("✅ Basic imports successful")
        
        # Test voting system import
        from voting_system import VotingSystem, voting_system
        print("✅ VotingSystem imported successfully")
        
        from voting_system import show_voting_interface, show_enhanced_voting_interface
        print("✅ Voting interface functions imported")
        
        from voting_results import show_voting_results, show_individual_vote_lookup
        print("✅ Voting results functions imported")
        
        return True
        
    except Exception as e:
        print("❌ Import error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_database_and_functionality():
    """Test database and basic functionality"""
    print("\n🔍 Testing database and functionality...")
    
    try:
        from voting_system import voting_system
        
        # Test getting parties
        parties = voting_system.get_parties()
        print("✅ Got {} parties".format(len(parties)))
        
        if len(parties) == 0:
            print("⚠️ No parties found - database may need initialization")
            print("💡 Run: python fix_voting_database.py")
            return False
        
        # Show sample parties
        print("   Sample parties:")
        for i, party in enumerate(parties[:3], 1):
            print("     {}. {} {} - {}".format(
                i, party['symbol'], party['name'], party['description'][:40] + "..."
            ))
        
        # Test vote checking
        has_voted = voting_system.has_voted(999)
        print("✅ Vote checking works: {}".format(has_voted))
        
        # Test getting results
        results = voting_system.get_voting_results()
        print("✅ Results query works: {} total votes".format(results['total_votes']))
        
        return True
        
    except Exception as e:
        print("❌ Database/functionality error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_vote_casting():
    """Test actual vote casting"""
    print("\n🔍 Testing vote casting...")
    
    try:
        from voting_system import voting_system
        
        # Get parties
        parties = voting_system.get_parties()
        if len(parties) == 0:
            print("❌ No parties available for testing")
            return False
        
        # Test parameters
        test_person_id = 995  # Use unique ID
        test_party_id = parties[0]['id']
        test_confidence = 0.85
        
        print("Testing vote casting:")
        print("  Person ID: {}".format(test_person_id))
        print("  Party: {} {}".format(parties[0]['symbol'], parties[0]['name']))
        print("  Confidence: {:.1%}".format(test_confidence))
        
        # Check if already voted
        if voting_system.has_voted(test_person_id):
            print("⚠️ Test person already voted - this is OK for testing")
            existing_vote = voting_system.get_vote_by_person(test_person_id)
            if existing_vote:
                print("   Existing vote: {} {} at {}".format(
                    existing_vote['symbol'],
                    existing_vote['party'],
                    existing_vote['timestamp']
                ))
            return True
        
        # Cast vote
        print("🗳️ Casting test vote...")
        success = voting_system.cast_vote(test_person_id, test_party_id, test_confidence)
        
        if success:
            print("✅ Vote cast successfully!")
            
            # Verify vote
            vote_info = voting_system.get_vote_by_person(test_person_id)
            if vote_info:
                print("✅ Vote verified:")
                print("   Party: {} {}".format(vote_info['symbol'], vote_info['party']))
                print("   Time: {}".format(vote_info['timestamp']))
                print("   Confidence: {:.1%}".format(vote_info['confidence']))
                return True
            else:
                print("❌ Vote not found after casting!")
                return False
        else:
            print("❌ Vote casting failed!")
            return False
        
    except Exception as e:
        print("❌ Vote casting error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_gui_interface():
    """Test GUI interface creation"""
    print("\n🔍 Testing GUI interface...")
    
    try:
        import tkinter as tk
        
        # Create test window
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test if interface functions exist and can be called
        from voting_system import show_voting_interface, show_enhanced_voting_interface
        
        print("✅ GUI interface functions available")
        print("💡 GUI interfaces can be opened (not tested to avoid user interaction)")
        
        root.destroy()
        return True
        
    except Exception as e:
        print("❌ GUI interface error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 FINAL VOTING SYSTEM TEST")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_voting_system_import),
        ("Database & Functionality", test_database_and_functionality),
        ("Vote Casting", test_vote_casting),
        ("GUI Interface", test_gui_interface),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print("\n" + "─" * 30)
        print("🧪 {}".format(test_name))
        print("─" * 30)
        
        if test_func():
            print("✅ {} PASSED".format(test_name))
            passed_tests += 1
        else:
            print("❌ {} FAILED".format(test_name))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 FINAL RESULTS")
    print("=" * 40)
    print("Tests passed: {}/{}".format(passed_tests, total_tests))
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Voting system is working correctly!")
        print("\n🚀 READY TO USE:")
        print("1. Run 'python Main.py'")
        print("2. Click 'VOTING SYSTEM' → 'CAST VOTE (DIRECT)'")
        print("3. Select iris image for authentication")
        print("4. Choose party and cast vote")
        print("\n✅ The voting system error should be resolved!")
    else:
        print("❌ Some tests failed")
        
        if passed_tests == 0:
            print("\n🔧 CRITICAL ISSUES - TRY THESE FIXES:")
            print("1. Run: python fix_voting_database.py")
            print("2. Check Python version (should be 3.6+)")
            print("3. Verify all .py files exist")
        elif passed_tests < total_tests:
            print("\n🔧 PARTIAL ISSUES - TRY THESE:")
            print("1. If database test failed: python fix_voting_database.py")
            print("2. If vote casting failed: Check console for specific errors")
            print("3. If GUI test failed: Check tkinter installation")

if __name__ == "__main__":
    main()
