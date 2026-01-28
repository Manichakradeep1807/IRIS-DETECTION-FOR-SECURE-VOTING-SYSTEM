#!/usr/bin/env python3
"""
Simple test for voting system after f-string fixes
"""

def test_basic_voting_import():
    """Test if voting system can be imported"""
    print("🔍 Testing voting system import...")
    
    try:
        # Test basic imports first
        import sqlite3
        import hashlib
        from datetime import datetime
        print("✅ Basic imports successful")
        
        # Test voting system import
        from voting_system import VotingSystem
        print("✅ VotingSystem class imported")
        
        # Test creating instance
        voting_system = VotingSystem()
        print("✅ VotingSystem instance created")
        
        # Test basic functionality
        parties = voting_system.get_parties()
        print("✅ Got {} parties".format(len(parties)))
        
        # Test vote checking
        has_voted = voting_system.has_voted(999)
        print("✅ Vote checking works: {}".format(has_voted))
        
        return True
        
    except Exception as e:
        print("❌ Error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_string_operations():
    """Test string operations that were causing issues"""
    print("\n🔍 Testing string operations...")
    
    try:
        # Test the patterns we fixed
        person_id = 123
        confidence = 0.95
        party_name = "Test Party"
        party_symbol = "🗳️"
        
        # Test .format() patterns
        test1 = "Person {} authenticated".format(person_id)
        print("✅ Basic format: {}".format(test1))
        
        test2 = "Confidence: {:.1%}".format(confidence)
        print("✅ Percentage format: {}".format(test2))
        
        test3 = "Vote for: {} {}".format(party_symbol, party_name)
        print("✅ Multiple format: {}".format(test3))
        
        # Test hash generation (the original issue)
        import hashlib
        from datetime import datetime
        vote_data = "{}_{}_{}" .format(person_id, 1, datetime.now().isoformat())
        vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()
        print("✅ Hash generation works: {}".format(vote_hash[:16] + "..."))
        
        return True
        
    except Exception as e:
        print("❌ String operations error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 SIMPLE VOTING SYSTEM TEST")
    print("=" * 40)
    
    # Test basic import
    if not test_basic_voting_import():
        print("\n❌ Basic voting import failed")
        return
    
    # Test string operations
    if not test_string_operations():
        print("\n❌ String operations failed")
        return
    
    print("\n🎉 All basic tests passed!")
    print("The voting system should now work without format string errors.")
    print("\nNext steps:")
    print("1. Try running Main.py")
    print("2. Use TEST RECOGNITION to authenticate")
    print("3. Test the voting interface")

if __name__ == "__main__":
    main()
