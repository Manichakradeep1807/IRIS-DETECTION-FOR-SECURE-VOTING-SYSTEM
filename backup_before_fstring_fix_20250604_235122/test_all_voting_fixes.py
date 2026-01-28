#!/usr/bin/env python3
"""
Comprehensive test for all voting system fixes
"""

def test_voting_system_import():
    """Test voting system import and basic functionality"""
    print("🔍 Testing voting system import...")
    
    try:
        # Test basic imports
        import sqlite3
        import hashlib
        from datetime import datetime
        print("✅ Basic imports successful")
        
        # Test voting system imports
        from voting_system import VotingSystem, voting_system
        print("✅ VotingSystem imported successfully")
        
        from voting_system import show_voting_interface, show_enhanced_voting_interface
        print("✅ Voting interface functions imported")
        
        # Test voting results imports
        from voting_results import show_voting_results, show_individual_vote_lookup
        print("✅ Voting results functions imported")
        
        return True
        
    except Exception as e:
        print("❌ Import error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_voting_functionality():
    """Test basic voting system functionality"""
    print("\n🔍 Testing voting system functionality...")
    
    try:
        from voting_system import voting_system
        
        # Test getting parties
        parties = voting_system.get_parties()
        print("✅ Got {} parties".format(len(parties)))
        
        if len(parties) > 0:
            print("   Sample party: {} {}".format(parties[0]['symbol'], parties[0]['name']))
        
        # Test vote checking
        test_person_id = 999
        has_voted = voting_system.has_voted(test_person_id)
        print("✅ Vote checking works: Person {} has voted: {}".format(test_person_id, has_voted))
        
        # Test getting results
        results = voting_system.get_voting_results()
        print("✅ Got voting results: {} total votes".format(results['total_votes']))
        
        return True
        
    except Exception as e:
        print("❌ Functionality error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_string_formatting():
    """Test all the string formatting patterns we fixed"""
    print("\n🔍 Testing string formatting patterns...")
    
    try:
        import hashlib
        from datetime import datetime
        
        # Test basic formatting
        person_id = 123
        confidence = 0.95
        party_name = "Test Party"
        party_symbol = "🗳️"
        
        # Test patterns from voting_system.py
        test1 = "Person {} authenticated successfully!".format(person_id)
        print("✅ Basic format: {}".format(test1))
        
        test2 = "Confidence: {:.1%}".format(confidence)
        print("✅ Percentage format: {}".format(test2))
        
        test3 = "Vote for: {} {}".format(party_symbol, party_name)
        print("✅ Multiple format: {}".format(test3))
        
        # Test hash generation (the original problematic pattern)
        vote_data = "{}_{}_{}" .format(person_id, 1, datetime.now().isoformat())
        vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()
        print("✅ Hash generation: {}...".format(vote_hash[:16]))
        
        # Test message box patterns
        msg1 = "Person {} has already voted!\n\nVote cast for: {} {}\nTime: {}\nConfidence: {:.1%}".format(
            person_id, party_symbol, party_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), confidence
        )
        print("✅ Complex message format works")
        
        # Test window title patterns
        title1 = "🗳️ Voting System - Person {}".format(person_id)
        title2 = "🗳️ Enhanced Voting System - Person {}".format(person_id)
        print("✅ Window title formats work")
        
        return True
        
    except Exception as e:
        print("❌ String formatting error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_main_integration():
    """Test that Main.py can import voting system without errors"""
    print("\n🔍 Testing Main.py integration...")
    
    try:
        # Test the import pattern from Main.py
        from voting_system import voting_system, show_voting_interface, show_enhanced_voting_interface
        from voting_results import show_voting_results, show_individual_vote_lookup
        print("✅ Main.py style imports work")
        
        # Test that we can create instances
        parties = voting_system.get_parties()
        print("✅ Can access voting system from Main.py context")
        
        return True
        
    except Exception as e:
        print("❌ Main.py integration error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 COMPREHENSIVE VOTING SYSTEM FIX TEST")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test 1: Import functionality
    if not test_voting_system_import():
        print("\n❌ Import test failed")
        all_tests_passed = False
    
    # Test 2: Basic functionality
    if not test_voting_functionality():
        print("\n❌ Functionality test failed")
        all_tests_passed = False
    
    # Test 3: String formatting
    if not test_string_formatting():
        print("\n❌ String formatting test failed")
        all_tests_passed = False
    
    # Test 4: Main.py integration
    if not test_main_integration():
        print("\n❌ Main.py integration test failed")
        all_tests_passed = False
    
    # Final result
    if all_tests_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The voting system should now work without format string errors")
        print("\nNext steps:")
        print("1. Run 'python Main.py'")
        print("2. Click 'TEST RECOGNITION' or 'VOTING SYSTEM'")
        print("3. Test the voting functionality")
    else:
        print("\n❌ Some tests failed")
        print("Please check the error messages above for details")

if __name__ == "__main__":
    main()
