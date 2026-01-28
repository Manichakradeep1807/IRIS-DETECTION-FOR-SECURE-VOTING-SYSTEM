#!/usr/bin/env python3
"""
Simple test for vote casting functionality
"""

def test_basic_vote_casting():
    """Test basic vote casting without GUI"""
    print("🔍 Testing basic vote casting...")
    
    try:
        # Import voting system
        from voting_system import voting_system
        print("✅ Voting system imported")
        
        # Check if parties exist
        parties = voting_system.get_parties()
        print("✅ Got {} parties".format(len(parties)))
        
        if len(parties) == 0:
            print("❌ No parties available! Database might not be initialized.")
            return False
        
        # Show available parties
        print("\n📋 Available parties:")
        for i, party in enumerate(parties[:5], 1):  # Show first 5
            print("  {}. {} {} - {}".format(
                i, party['symbol'], party['name'], party['description'][:50] + "..."
            ))
        
        # Test vote casting
        test_person_id = 997  # Use a different ID to avoid conflicts
        test_party_id = parties[0]['id']  # Vote for first party
        test_confidence = 0.85
        
        print("\n🗳️ Testing vote casting:")
        print("  Person ID: {}".format(test_person_id))
        print("  Party: {} {}".format(parties[0]['symbol'], parties[0]['name']))
        print("  Confidence: {:.1%}".format(test_confidence))
        
        # Check if already voted
        if voting_system.has_voted(test_person_id):
            print("⚠️ Person {} has already voted. Checking existing vote...".format(test_person_id))
            existing_vote = voting_system.get_vote_by_person(test_person_id)
            if existing_vote:
                print("   Existing vote: {} {} at {}".format(
                    existing_vote['symbol'],
                    existing_vote['party'],
                    existing_vote['timestamp']
                ))
            return True  # Already voted is not an error
        
        # Cast the vote
        print("🗳️ Casting vote...")
        success = voting_system.cast_vote(test_person_id, test_party_id, test_confidence)
        
        if success:
            print("✅ Vote cast successfully!")
            
            # Verify the vote
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
        print("❌ Error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_voting_results():
    """Test getting voting results"""
    print("\n🔍 Testing voting results...")
    
    try:
        from voting_system import voting_system
        
        results = voting_system.get_voting_results()
        print("✅ Got voting results:")
        print("   Total votes: {}".format(results['total_votes']))
        print("   Total voters: {}".format(results['total_voters']))
        
        if results['total_votes'] > 0:
            print("\n📊 Current standings:")
            for result in results['results']:
                if result['votes'] > 0:
                    print("   {} {}: {} votes ({:.1f}%)".format(
                        result['symbol'],
                        result['party'],
                        result['votes'],
                        result['percentage']
                    ))
        else:
            print("   No votes cast yet")
        
        return True
        
    except Exception as e:
        print("❌ Results error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_gui_voting_interface():
    """Test if GUI voting interface can be opened"""
    print("\n🔍 Testing GUI voting interface...")
    
    try:
        import tkinter as tk
        from voting_system import show_voting_interface
        
        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()
        
        print("✅ Tkinter initialized")
        print("✅ Voting interface function available")
        
        # Note: We won't actually open the interface in this test
        # as it would require user interaction
        print("💡 GUI interface is available (not opened in test)")
        
        root.destroy()
        return True
        
    except Exception as e:
        print("❌ GUI error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 VOTE CASTING FUNCTIONALITY TEST")
    print("=" * 45)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Basic vote casting
    if test_basic_vote_casting():
        tests_passed += 1
        print("✅ Test 1 PASSED: Basic vote casting")
    else:
        print("❌ Test 1 FAILED: Basic vote casting")
    
    # Test 2: Voting results
    if test_voting_results():
        tests_passed += 1
        print("✅ Test 2 PASSED: Voting results")
    else:
        print("❌ Test 2 FAILED: Voting results")
    
    # Test 3: GUI interface
    if test_gui_voting_interface():
        tests_passed += 1
        print("✅ Test 3 PASSED: GUI interface")
    else:
        print("❌ Test 3 FAILED: GUI interface")
    
    # Summary
    print("\n" + "=" * 45)
    print("SUMMARY: {}/{} tests passed".format(tests_passed, total_tests))
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Vote casting should work in the main application")
        print("\nNext steps:")
        print("1. Run 'python Main.py'")
        print("2. Click 'VOTING SYSTEM' → 'CAST VOTE (DIRECT)'")
        print("3. Select an iris image for authentication")
        print("4. Choose a party and cast your vote")
    else:
        print("❌ Some tests failed")
        print("💡 Check the error messages above for details")
        
        if tests_passed == 0:
            print("\n🔧 POSSIBLE FIXES:")
            print("• Run: python create_sample_votes.py")
            print("• Check if voting_system.db exists")
            print("• Verify all dependencies are installed")

if __name__ == "__main__":
    main()
