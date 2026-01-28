#!/usr/bin/env python3
"""
Debug voting system error - capture exact error details
"""

import sys
import traceback
import os

def test_basic_imports():
    """Test basic imports step by step"""
    print("🔍 Testing basic imports...")
    
    try:
        print("  Testing sqlite3...")
        import sqlite3
        print("  ✅ sqlite3 OK")
        
        print("  Testing tkinter...")
        import tkinter as tk
        print("  ✅ tkinter OK")
        
        print("  Testing hashlib...")
        import hashlib
        print("  ✅ hashlib OK")
        
        print("  Testing datetime...")
        from datetime import datetime
        print("  ✅ datetime OK")
        
        return True
        
    except Exception as e:
        print("  ❌ Basic import error: {}".format(str(e)))
        traceback.print_exc()
        return False

def test_voting_system_import():
    """Test voting system import with detailed error capture"""
    print("\n🔍 Testing voting system import...")
    
    try:
        print("  Importing VotingSystem class...")
        from voting_system import VotingSystem
        print("  ✅ VotingSystem class imported")
        
        print("  Importing voting_system instance...")
        from voting_system import voting_system
        print("  ✅ voting_system instance imported")
        
        print("  Importing interface functions...")
        from voting_system import show_voting_interface, show_enhanced_voting_interface
        print("  ✅ Interface functions imported")
        
        return True
        
    except Exception as e:
        print("  ❌ Voting system import error: {}".format(str(e)))
        print("\n📋 DETAILED ERROR:")
        traceback.print_exc()
        return False

def test_voting_system_initialization():
    """Test voting system initialization"""
    print("\n🔍 Testing voting system initialization...")
    
    try:
        from voting_system import voting_system
        
        print("  Testing get_parties()...")
        parties = voting_system.get_parties()
        print("  ✅ get_parties() returned {} parties".format(len(parties)))
        
        if len(parties) == 0:
            print("  ⚠️ WARNING: No parties found in database!")
            return False
        
        print("  Testing has_voted()...")
        has_voted = voting_system.has_voted(999)
        print("  ✅ has_voted() returned: {}".format(has_voted))
        
        print("  Testing get_voting_results()...")
        results = voting_system.get_voting_results()
        print("  ✅ get_voting_results() returned {} total votes".format(results['total_votes']))
        
        return True
        
    except Exception as e:
        print("  ❌ Initialization error: {}".format(str(e)))
        print("\n📋 DETAILED ERROR:")
        traceback.print_exc()
        return False

def test_database_file():
    """Test database file existence and structure"""
    print("\n🔍 Testing database file...")
    
    try:
        db_path = "voting_system.db"
        
        if not os.path.exists(db_path):
            print("  ❌ Database file does not exist: {}".format(db_path))
            return False
        
        print("  ✅ Database file exists: {}".format(db_path))
        
        # Test database connection
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            print("  ✅ Tables found: {}".format(tables))
            
            if 'parties' not in tables:
                print("  ❌ 'parties' table missing!")
                return False
            
            if 'votes' not in tables:
                print("  ❌ 'votes' table missing!")
                return False
            
            # Check party count
            cursor.execute("SELECT COUNT(*) FROM parties")
            party_count = cursor.fetchone()[0]
            print("  ✅ Parties in database: {}".format(party_count))
            
            if party_count == 0:
                print("  ❌ No parties in database!")
                return False
        
        return True
        
    except Exception as e:
        print("  ❌ Database error: {}".format(str(e)))
        print("\n📋 DETAILED ERROR:")
        traceback.print_exc()
        return False

def test_main_py_integration():
    """Test Main.py integration"""
    print("\n🔍 Testing Main.py integration...")
    
    try:
        # Test the import pattern from Main.py
        print("  Testing Main.py style imports...")
        
        from voting_system import voting_system, show_voting_interface, show_enhanced_voting_interface
        from voting_results import show_voting_results, show_individual_vote_lookup
        
        print("  ✅ Main.py style imports successful")
        
        # Test VOTING_SYSTEM_SUPPORT flag logic
        VOTING_SYSTEM_SUPPORT = True
        print("  ✅ VOTING_SYSTEM_SUPPORT = {}".format(VOTING_SYSTEM_SUPPORT))
        
        return True
        
    except Exception as e:
        print("  ❌ Main.py integration error: {}".format(str(e)))
        print("\n📋 DETAILED ERROR:")
        traceback.print_exc()
        return False

def run_comprehensive_diagnosis():
    """Run comprehensive diagnosis"""
    print("🔧 COMPREHENSIVE VOTING SYSTEM ERROR DIAGNOSIS")
    print("=" * 60)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Voting System Import", test_voting_system_import),
        ("Database File", test_database_file),
        ("System Initialization", test_voting_system_initialization),
        ("Main.py Integration", test_main_py_integration),
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        print("\n" + "─" * 40)
        print("🧪 TEST: {}".format(test_name))
        print("─" * 40)
        
        if test_func():
            print("✅ {} PASSED".format(test_name))
        else:
            print("❌ {} FAILED".format(test_name))
            failed_tests.append(test_name)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    if len(failed_tests) == 0:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Voting system should work correctly")
        print("\n💡 If you're still getting errors, please:")
        print("   1. Run 'python Main.py' and try voting")
        print("   2. Share the exact error message you see")
    else:
        print("❌ FAILED TESTS: {}".format(len(failed_tests)))
        for test in failed_tests:
            print("   • {}".format(test))
        
        print("\n🔧 RECOMMENDED FIXES:")
        
        if "Database File" in failed_tests or "System Initialization" in failed_tests:
            print("   1. Run: python fix_voting_database.py")
        
        if "Voting System Import" in failed_tests:
            print("   2. Check for remaining f-string issues")
            print("   3. Verify all files are present")
        
        if "Basic Imports" in failed_tests:
            print("   4. Check Python installation and dependencies")

def main():
    """Main function"""
    try:
        run_comprehensive_diagnosis()
    except Exception as e:
        print("\n💥 CRITICAL ERROR IN DIAGNOSIS:")
        print("Error: {}".format(str(e)))
        print("\n📋 FULL TRACEBACK:")
        traceback.print_exc()
        
        print("\n🆘 EMERGENCY FIXES:")
        print("1. Try: python fix_voting_database.py")
        print("2. Check if all .py files exist in the directory")
        print("3. Restart your terminal/command prompt")
        print("4. Share this error output for further help")

if __name__ == "__main__":
    main()
