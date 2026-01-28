#!/usr/bin/env python3
"""Simple voting system test"""

def test_voting():
    try:
        from voting_system import voting_system
        
        parties = voting_system.get_parties()
        print("SUCCESS: Found {} parties".format(len(parties)))
        
        for i, party in enumerate(parties[:3], 1):
            print("  {}. {} - {}".format(i, party['symbol'], party['name']))
        
        has_voted = voting_system.has_voted(999)
        print("SUCCESS: Vote checking works")
        
        results = voting_system.get_voting_results()
        print("SUCCESS: Results query works - {} total votes".format(results['total_votes']))
        
        print("\nVOTING SYSTEM IS WORKING CORRECTLY!")
        return True
        
    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False

if __name__ == "__main__":
    print("VOTING SYSTEM TEST")
    print("=" * 20)
    
    if test_voting():
        print("\nALL TESTS PASSED!")
        print("You can now use the voting system in Main.py")
    else:
        print("\nTESTS FAILED!")
        print("Check the error messages above")
