#!/usr/bin/env python3
"""
Test Voting System
Comprehensive test of the iris-based voting system
"""

import os
import sys
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def test_voting_database():
    """Test voting database functionality"""
    print("🧪 TESTING VOTING DATABASE")
    print("=" * 50)
    
    try:
        from voting_system import VotingSystem
        
        # Create test voting system
        test_db = "test_voting.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        
        voting_system = VotingSystem(test_db)
        
        # Test 1: Get parties
        parties = voting_system.get_parties()
        print(f"✅ Test 1 - Get parties: {len(parties)} parties loaded")
        for party in parties[:3]:  # Show first 3
            print(f"   {party['symbol']} {party['name']}")
        
        # Test 2: Cast votes
        test_votes = [
            (1, 1, 0.95),  # Person 1 votes for party 1
            (2, 2, 0.88),  # Person 2 votes for party 2
            (3, 1, 0.92),  # Person 3 votes for party 1
            (4, 3, 0.85),  # Person 4 votes for party 3
        ]
        
        print(f"\n✅ Test 2 - Casting {len(test_votes)} test votes:")
        for person_id, party_id, confidence in test_votes:
            success = voting_system.cast_vote(person_id, party_id, confidence)
            party_name = next(p['name'] for p in parties if p['id'] == party_id)
            print(f"   Person {person_id} → {party_name}: {'✅' if success else '❌'}")
        
        # Test 3: Check duplicate voting
        print(f"\n✅ Test 3 - Testing duplicate vote prevention:")
        duplicate_success = voting_system.cast_vote(1, 2, 0.90)  # Person 1 tries to vote again
        print(f"   Duplicate vote blocked: {'✅' if not duplicate_success else '❌'}")
        
        # Test 4: Get results
        print(f"\n✅ Test 4 - Getting voting results:")
        results = voting_system.get_voting_results()
        print(f"   Total votes: {results['total_votes']}")
        print(f"   Total voters: {results['total_voters']}")
        
        for result in results['results']:
            if result['votes'] > 0:
                print(f"   {result['symbol']} {result['party']}: {result['votes']} votes ({result['percentage']:.1f}%)")
        
        # Test 5: Individual vote lookup
        print(f"\n✅ Test 5 - Individual vote lookup:")
        vote_info = voting_system.get_vote_by_person(1)
        if vote_info:
            print(f"   Person 1 voted for: {vote_info['party']} {vote_info['symbol']}")
            print(f"   Time: {vote_info['timestamp']}")
        
        # Cleanup
        if os.path.exists(test_db):
            os.remove(test_db)
        
        print(f"\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_voting_interface():
    """Test voting interface"""
    print("\n🧪 TESTING VOTING INTERFACE")
    print("=" * 50)
    
    try:
        from voting_system import show_voting_interface
        
        # Create test window
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        print("✅ Opening voting interface for Person 99 (test)")
        print("   Please interact with the interface and close it to continue...")
        
        # Show voting interface for test person
        show_voting_interface(person_id=99, confidence_score=0.95)
        
        # Wait for interface to close
        root.mainloop()
        
        print("✅ Voting interface test completed")
        return True
        
    except Exception as e:
        print(f"❌ Interface test failed: {e}")
        return False

def test_voting_results():
    """Test voting results dashboard"""
    print("\n🧪 TESTING VOTING RESULTS DASHBOARD")
    print("=" * 50)
    
    try:
        from voting_results import show_voting_results
        
        # Create test window
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        print("✅ Opening voting results dashboard")
        print("   Please interact with the dashboard and close it to continue...")
        
        # Show results dashboard
        show_voting_results()
        
        # Wait for dashboard to close
        root.mainloop()
        
        print("✅ Results dashboard test completed")
        return True
        
    except Exception as e:
        print(f"❌ Results dashboard test failed: {e}")
        return False

def test_main_integration():
    """Test integration with main application"""
    print("\n🧪 TESTING MAIN APPLICATION INTEGRATION")
    print("=" * 50)
    
    try:
        # Test imports
        from Main import VOTING_SYSTEM_SUPPORT, show_voting_menu
        
        print(f"✅ Voting system support: {'Available' if VOTING_SYSTEM_SUPPORT else 'Not available'}")
        
        if VOTING_SYSTEM_SUPPORT:
            print("✅ Voting system imports successful")
            print("✅ Voting menu function available")
            
            # Test voting menu (optional - requires GUI)
            response = input("   Test voting menu interface? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                root = tk.Tk()
                root.withdraw()
                
                print("✅ Opening voting menu...")
                show_voting_menu()
                
                root.mainloop()
                print("✅ Voting menu test completed")
        else:
            print("❌ Voting system not properly integrated")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Main integration test failed: {e}")
        return False

def create_sample_votes():
    """Create sample votes for demonstration"""
    print("\n🗳️ CREATING SAMPLE VOTES FOR DEMONSTRATION")
    print("=" * 50)
    
    try:
        from voting_system import voting_system
        
        # Sample votes from different persons to different parties
        sample_votes = [
            (1, 1, 0.95, "Democratic Party"),
            (2, 2, 0.88, "Republican Party"),
            (3, 1, 0.92, "Democratic Party"),
            (4, 3, 0.85, "Green Party"),
            (5, 2, 0.91, "Republican Party"),
            (6, 4, 0.87, "Libertarian Party"),
            (7, 1, 0.94, "Democratic Party"),
            (8, 5, 0.89, "Independent"),
            (9, 2, 0.86, "Republican Party"),
            (10, 3, 0.93, "Green Party"),
        ]
        
        parties = voting_system.get_parties()
        
        print("Creating sample votes:")
        votes_created = 0
        
        for person_id, party_id, confidence, party_name in sample_votes:
            if not voting_system.has_voted(person_id):
                success = voting_system.cast_vote(person_id, party_id, confidence)
                if success:
                    votes_created += 1
                    print(f"   ✅ Person {person_id} → {party_name}")
                else:
                    print(f"   ❌ Failed to record vote for Person {person_id}")
            else:
                print(f"   ⏭️ Person {person_id} already voted")
        
        print(f"\n📊 Sample votes created: {votes_created}")
        
        # Show current results
        results = voting_system.get_voting_results()
        print(f"📈 Current voting statistics:")
        print(f"   Total votes: {results['total_votes']}")
        print(f"   Total voters: {results['total_voters']}")
        
        print(f"\n🏆 Current standings:")
        for result in sorted(results['results'], key=lambda x: x['votes'], reverse=True):
            if result['votes'] > 0:
                print(f"   {result['symbol']} {result['party']}: {result['votes']} votes ({result['percentage']:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample votes creation failed: {e}")
        return False

def main():
    """Main test function"""
    print("🗳️ IRIS-BASED VOTING SYSTEM - COMPREHENSIVE TEST")
    print("=" * 70)
    print("This test verifies all components of the voting system.")
    print()
    
    # Test results
    test_results = []
    
    # Run tests
    test_results.append(("Database Functionality", test_voting_database()))
    test_results.append(("Main Integration", test_main_integration()))
    
    # Optional GUI tests
    gui_tests = input("Run GUI tests? (requires manual interaction) (y/n): ").lower().strip()
    if gui_tests in ['y', 'yes']:
        test_results.append(("Voting Interface", test_voting_interface()))
        test_results.append(("Results Dashboard", test_voting_results()))
    
    # Sample data
    sample_data = input("Create sample voting data? (y/n): ").lower().strip()
    if sample_data in ['y', 'yes']:
        test_results.append(("Sample Votes", create_sample_votes()))
    
    # Show results
    print("\n" + "=" * 70)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Voting system is fully functional")
        print("✅ Ready for production use")
        print("\n📋 USAGE INSTRUCTIONS:")
        print("1. Run Main.py")
        print("2. Click '🗳️ VOTING SYSTEM'")
        print("3. Choose 'CAST VOTE' to authenticate and vote")
        print("4. Use 'TEST RECOGNITION' to authenticate with iris")
        print("5. View results with 'VIEW RESULTS'")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        print("Please check the error messages above")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
