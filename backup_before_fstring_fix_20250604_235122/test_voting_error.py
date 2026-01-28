#!/usr/bin/env python3
"""
Test script to identify the voting system error
"""

import sys
import traceback

def test_imports():
    """Test all imports to identify the issue"""
    print("🔍 Testing imports...")
    
    try:
        print("Testing basic imports...")
        import tkinter as tk
        print("✅ tkinter imported successfully")
        
        import sqlite3
        print("✅ sqlite3 imported successfully")
        
        import hashlib
        print("✅ hashlib imported successfully")
        
        from datetime import datetime
        print("✅ datetime imported successfully")
        
        print("\nTesting voting system imports...")
        from voting_system import VotingSystem
        print("✅ VotingSystem imported successfully")
        
        from voting_system import voting_system
        print("✅ voting_system instance imported successfully")
        
        from voting_system import show_voting_interface
        print("✅ show_voting_interface imported successfully")
        
        from voting_system import show_enhanced_voting_interface
        print("✅ show_enhanced_voting_interface imported successfully")
        
        from voting_results import show_voting_results
        print("✅ show_voting_results imported successfully")
        
        from voting_results import show_individual_vote_lookup
        print("✅ show_individual_vote_lookup imported successfully")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_voting_system_basic():
    """Test basic voting system functionality"""
    print("\n🔍 Testing basic voting system functionality...")
    
    try:
        from voting_system import voting_system
        
        # Test getting parties
        parties = voting_system.get_parties()
        print(f"✅ Got {len(parties)} parties")
        
        # Test checking if someone voted
        has_voted = voting_system.has_voted(999)
        print(f"✅ Vote check works: {has_voted}")
        
        print("✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality error: {e}")
        traceback.print_exc()
        return False

def test_string_formatting():
    """Test string formatting that might be causing the issue"""
    print("\n🔍 Testing string formatting...")
    
    try:
        import hashlib
        from datetime import datetime
        
        # Test f-string formatting
        person_id = 123
        confidence = 0.95
        party_name = "Test Party"
        
        # Test various f-string patterns used in the code
        test1 = f"Person {person_id} authenticated successfully!"
        print(f"✅ Test 1: {test1}")
        
        test2 = f"Confidence: {confidence:.1%}"
        print(f"✅ Test 2: {test2}")
        
        test3 = f"Vote cast for: {party_name}"
        print(f"✅ Test 3: {test3}")
        
        test4 = f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"✅ Test 4: {test4}")
        
        # Test the specific pattern that might be causing issues
        vote_data = f"{person_id}_{1}_{datetime.now().isoformat()}"
        vote_hash = hashlib.sha256(vote_data.encode()).hexdigest()
        print(f"✅ Test 5: Vote hash generation works")
        
        print("✅ String formatting test passed!")
        return True
        
    except Exception as e:
        print(f"❌ String formatting error: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 VOTING SYSTEM ERROR DIAGNOSIS")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed - this is likely the issue")
        return
    
    # Test basic functionality
    if not test_voting_system_basic():
        print("\n❌ Basic functionality test failed")
        return
    
    # Test string formatting
    if not test_string_formatting():
        print("\n❌ String formatting test failed")
        return
    
    print("\n🎉 All tests passed! The voting system should work correctly.")
    print("If you're still getting errors, please run Main.py and share the exact error message.")

if __name__ == "__main__":
    main()
