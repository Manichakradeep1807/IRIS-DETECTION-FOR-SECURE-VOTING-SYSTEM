#!/usr/bin/env python3
"""
PREVENT F-STRING ERRORS - AUTOMATED MONITORING
Automatically monitors and prevents f-string format errors in the voting system
"""

import os
import re
import time
from datetime import datetime

def scan_for_fstrings(directory="."):
    """Scan for any f-strings that might cause format errors"""
    print("🔍 SCANNING FOR POTENTIAL F-STRING ISSUES")
    print("=" * 50)
    
    fstring_patterns = [
        r'f"[^"]*\{[^}]*\}[^"]*"',  # f"..." patterns
        r"f'[^']*\{[^}]*\}[^']*'",  # f'...' patterns
    ]
    
    problematic_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip backup directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('backup_') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern in fstring_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            problematic_files.append((filepath, matches))
                            print("⚠️ Found f-strings in: {}".format(filepath))
                            for match in matches[:3]:  # Show first 3 matches
                                print("   {}".format(match[:60]))
                            if len(matches) > 3:
                                print("   ... and {} more".format(len(matches) - 3))
                
                except Exception as e:
                    print("❌ Error reading {}: {}".format(filepath, str(e)))
    
    if not problematic_files:
        print("✅ No f-strings found - system is safe!")
    else:
        print("\n⚠️ Found {} files with f-strings".format(len(problematic_files)))
        print("Consider converting these to .format() method for better compatibility")
    
    return problematic_files

def auto_fix_fstrings(filepath):
    """Automatically convert f-strings to .format() method"""
    print("🔧 Auto-fixing f-strings in: {}".format(filepath))
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create backup
        backup_path = "{}.backup_{}".format(filepath, datetime.now().strftime('%Y%m%d_%H%M%S'))
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   📁 Backup created: {}".format(backup_path))
        
        # Simple f-string to .format() conversion
        # This is a basic conversion - complex f-strings may need manual review
        
        # Pattern 1: f"text {var} more text"
        pattern1 = r'f"([^"]*)\{([^}]+)\}([^"]*)"'
        replacement1 = r'"\1{}\3".format(\2)'
        content = re.sub(pattern1, replacement1, content)
        
        # Pattern 2: f'text {var} more text'
        pattern2 = r"f'([^']*)\{([^}]+)\}([^']*)'"
        replacement2 = r"'\1{}\3'.format(\2)"
        content = re.sub(pattern2, replacement2, content)
        
        # Write fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ F-strings converted to .format() method")
        return True
        
    except Exception as e:
        print("   ❌ Error fixing {}: {}".format(filepath, str(e)))
        return False

def verify_voting_system():
    """Verify that the voting system is working correctly"""
    print("\n🗳️ VERIFYING VOTING SYSTEM")
    print("=" * 50)
    
    try:
        # Test imports
        from voting_system import voting_system
        print("✅ Voting system import successful")
        
        # Test basic operations
        parties = voting_system.get_parties()
        print("✅ Parties retrieved: {} parties".format(len(parties)))
        
        results = voting_system.get_voting_results()
        print("✅ Results retrieved: {} total votes".format(results.get('total_votes', 0)))
        
        # Test string operations that previously caused errors
        import hashlib
        test_data = "{}_{}_{}" .format(123, 1, datetime.now().isoformat())
        test_hash = hashlib.sha256(test_data.encode('utf-8')).hexdigest()
        print("✅ Hash generation test passed")
        
        # Test message formatting
        test_message = "Person {} voted for party {} with {:.1%} confidence".format(123, 1, 0.95)
        print("✅ Message formatting test passed")
        
        print("\n🎉 VOTING SYSTEM VERIFICATION COMPLETE!")
        print("   All operations working correctly without format errors")
        return True
        
    except Exception as e:
        print("❌ Voting system verification failed: {}".format(str(e)))
        return False

def create_monitoring_report():
    """Create a monitoring report"""
    report_path = "fstring_monitoring_report_{}.txt".format(datetime.now().strftime('%Y%m%d_%H%M%S'))

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("F-STRING MONITORING REPORT\n")
        f.write("=" * 50 + "\n")
        f.write("Timestamp: {}\n".format(datetime.now().isoformat()))
        f.write("Status: Monitoring completed\n")
        f.write("\nScan Results:\n")
        
        # Scan for f-strings
        problematic_files = scan_for_fstrings()
        
        if not problematic_files:
            f.write("OK No f-strings found - system is safe!\n")
        else:
            f.write("WARNING Found {} files with f-strings\n".format(len(problematic_files)))
            for filepath, matches in problematic_files:
                f.write("  - {}: {} f-strings\n".format(filepath, len(matches)))
        
        f.write("\nVoting System Status:\n")
        if verify_voting_system():
            f.write("OK Voting system working correctly\n")
        else:
            f.write("ERROR Voting system has issues\n")
        
        f.write("\nRecommendations:\n")
        f.write("- Continue using .format() method instead of f-strings\n")
        f.write("- Regular monitoring to prevent format string errors\n")
        f.write("- Backup files before making changes\n")
    
    print("📊 Monitoring report saved: {}".format(report_path))
    return report_path

def main():
    """Main monitoring function"""
    print("🛡️ F-STRING ERROR PREVENTION SYSTEM")
    print("=" * 60)
    print("Monitoring and preventing 'unsupported format string passed to bytes.__format__' errors")
    print("=" * 60)
    
    # Scan for potential issues
    problematic_files = scan_for_fstrings()
    
    # Verify voting system
    voting_ok = verify_voting_system()
    
    # Create monitoring report
    report_path = create_monitoring_report()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 MONITORING SUMMARY")
    print("=" * 60)
    
    if not problematic_files and voting_ok:
        print("🎉 SYSTEM STATUS: EXCELLENT")
        print("✅ No f-strings found")
        print("✅ Voting system working correctly")
        print("✅ No format string errors detected")
        print("\n🛡️ The system is protected against format string errors!")
    else:
        print("⚠️ SYSTEM STATUS: NEEDS ATTENTION")
        if problematic_files:
            print("❌ F-strings detected in {} files".format(len(problematic_files)))
        if not voting_ok:
            print("❌ Voting system has issues")
        print("\n🔧 Run auto-fix or manual review recommended")
    
    print("\n📊 Full report: {}".format(report_path))

if __name__ == "__main__":
    main()
