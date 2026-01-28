#!/usr/bin/env python3
"""
Fix all f-strings in voting_system.py to use .format() for compatibility
"""

import re
import os

def fix_fstrings_in_file(filepath):
    """Fix f-strings in a file by converting them to .format()"""
    print("🔧 Fixing f-strings in: {}".format(filepath))
    
    if not os.path.exists(filepath):
        print("❌ File not found: {}".format(filepath))
        return False
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Keep track of changes
        changes_made = 0
        
        # Simple f-string patterns to fix
        patterns = [
            # f"text {var}" -> "text {}".format(var)
            (r'f"([^"]*?)\{([^}]+?)\}([^"]*?)"', r'"\1{}\3".format(\2)'),
            # f'text {var}' -> 'text {}'.format(var)
            (r"f'([^']*?)\{([^}]+?)\}([^']*?)'", r"'\1{}\3'.format(\2)"),
        ]
        
        # Apply simple patterns first
        for pattern, replacement in patterns:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                changes_made += len(matches)
                print("  ✅ Fixed {} simple f-string patterns".format(len(matches)))
        
        # Manual fixes for complex cases
        manual_fixes = [
            # Debug prints
            ('print(f"DEBUG: Regular interface - Direct vote button clicked for party {party_data[\'id\']}")',
             'print("DEBUG: Regular interface - Direct vote button clicked for party {}".format(party_data[\'id\']))'),
            
            ('print(f"DEBUG: Party selection changed to ID: {party_id}")',
             'print("DEBUG: Party selection changed to ID: {}".format(party_id))'),
            
            ('print(f"DEBUG: Party selected: {selected_party_info[\'name\']}")',
             'print("DEBUG: Party selected: {}".format(selected_party_info[\'name\']))'),
            
            ('print(f"ERROR: Failed to update selection: {e}")',
             'print("ERROR: Failed to update selection: {}".format(str(e)))'),
            
            ('print(f"DEBUG: Radio button clicked for party {party[\'id\']}")',
             'print("DEBUG: Radio button clicked for party {}".format(party[\'id\']))'),
            
            ('print(f"DEBUG: Direct vote button clicked for party {party_data[\'id\']}")',
             'print("DEBUG: Direct vote button clicked for party {}".format(party_data[\'id\']))'),
            
            ('print(f"DEBUG: Updating button appearance, selected party ID: {party_id}")',
             'print("DEBUG: Updating button appearance, selected party ID: {}".format(party_id))'),
            
            ('print(f"DEBUG: Button set to enabled state for party {party_id}")',
             'print("DEBUG: Button set to enabled state for party {}".format(party_id))'),
            
            ('print(f"ERROR: Failed to update button appearance: {e}")',
             'print("ERROR: Failed to update button appearance: {}".format(str(e)))'),
        ]
        
        for old, new in manual_fixes:
            if old in content:
                content = content.replace(old, new)
                changes_made += 1
                print("  ✅ Fixed manual pattern")
        
        # Write the fixed content back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fixed {} f-string patterns in {}".format(changes_made, filepath))
        return True
        
    except Exception as e:
        print("❌ Error fixing f-strings: {}".format(str(e)))
        return False

def main():
    """Main function"""
    print("🔧 F-STRING COMPATIBILITY FIX")
    print("=" * 40)
    
    # Fix voting_system.py
    if fix_fstrings_in_file('voting_system.py'):
        print("\n✅ voting_system.py fixed successfully!")
    else:
        print("\n❌ Failed to fix voting_system.py")
        return
    
    # Also fix voting_results.py if it exists
    if os.path.exists('voting_results.py'):
        if fix_fstrings_in_file('voting_results.py'):
            print("✅ voting_results.py fixed successfully!")
        else:
            print("❌ Failed to fix voting_results.py")
    
    print("\n🎉 F-string compatibility fix completed!")
    print("The voting system should now work without format string errors.")
    print("\nTry running Main.py to test the application.")

if __name__ == "__main__":
    main()
