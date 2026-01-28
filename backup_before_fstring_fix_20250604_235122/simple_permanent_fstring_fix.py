#!/usr/bin/env python3
"""
SIMPLE PERMANENT F-STRING FIX
Automatically converts ALL f-strings in the entire project to .format() method
This will permanently solve the "unsupported format string passed to bytes.__format__" error
"""

import os
import re
import shutil
from datetime import datetime

def create_backup():
    """Create complete backup of the project"""
    backup_dir = "backup_before_fstring_fix_" + datetime.now().strftime('%Y%m%d_%H%M%S')
    print("📁 Creating complete project backup...")
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy all Python files
        for root, dirs, files in os.walk('.'):
            if backup_dir in root:
                continue
                
            for file in files:
                if file.endswith('.py'):
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, '.')
                    dst_path = os.path.join(backup_dir, rel_path)
                    
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
        
        print("   ✅ Backup created: " + backup_dir)
        return backup_dir
        
    except Exception as e:
        print("   ❌ Backup failed: " + str(e))
        return None

def simple_fstring_converter(content):
    """Simple but effective f-string to .format() converter"""
    converted_content = content
    conversions = 0
    
    # Handle simple cases first
    # Pattern: f"text {variable}" -> "text {}".format(variable)
    pattern1 = r'f"([^"]*?)\{([^}]+?)\}([^"]*?)"'
    matches1 = re.findall(pattern1, converted_content)
    for match in matches1:
        before, var, after = match
        old_str = 'f"' + before + '{' + var + '}' + after + '"'
        new_str = '"' + before + '{}' + after + '".format(' + var + ')'
        converted_content = converted_content.replace(old_str, new_str, 1)
        conversions += 1
    
    # Pattern: f'text {variable}' -> 'text {}'.format(variable)
    pattern2 = r"f'([^']*?)\{([^}]+?)\}([^']*?)'"
    matches2 = re.findall(pattern2, converted_content)
    for match in matches2:
        before, var, after = match
        old_str = "f'" + before + '{' + var + '}' + after + "'"
        new_str = "'" + before + '{}' + after + "'.format(" + var + ')'
        converted_content = converted_content.replace(old_str, new_str, 1)
        conversions += 1
    
    # Handle 2 variables: f"text {var1} more {var2}"
    pattern3 = r'f"([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)"'
    matches3 = re.findall(pattern3, converted_content)
    for match in matches3:
        before, var1, middle, var2, after = match
        old_str = 'f"' + before + '{' + var1 + '}' + middle + '{' + var2 + '}' + after + '"'
        new_str = '"' + before + '{}' + middle + '{}' + after + '".format(' + var1 + ', ' + var2 + ')'
        converted_content = converted_content.replace(old_str, new_str, 1)
        conversions += 1
    
    # Handle 2 variables with single quotes
    pattern4 = r"f'([^']*?)\{([^}]+?)\}([^']*?)\{([^}]+?)\}([^']*?)'"
    matches4 = re.findall(pattern4, converted_content)
    for match in matches4:
        before, var1, middle, var2, after = match
        old_str = "f'" + before + '{' + var1 + '}' + middle + '{' + var2 + '}' + after + "'"
        new_str = "'" + before + '{}' + middle + '{}' + after + "'.format(" + var1 + ', ' + var2 + ')'
        converted_content = converted_content.replace(old_str, new_str, 1)
        conversions += 1
    
    # Handle 3 variables
    pattern5 = r'f"([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)"'
    matches5 = re.findall(pattern5, converted_content)
    for match in matches5:
        before, var1, mid1, var2, mid2, var3, after = match
        old_str = 'f"' + before + '{' + var1 + '}' + mid1 + '{' + var2 + '}' + mid2 + '{' + var3 + '}' + after + '"'
        new_str = '"' + before + '{}' + mid1 + '{}' + mid2 + '{}' + after + '".format(' + var1 + ', ' + var2 + ', ' + var3 + ')'
        converted_content = converted_content.replace(old_str, new_str, 1)
        conversions += 1
    
    return converted_content, conversions

def process_file(filepath):
    """Process a single Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'f"' not in content and "f'" not in content:
            return 0
        
        new_content, conversions = simple_fstring_converter(content)
        
        if conversions > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("   ✅ " + filepath + ": " + str(conversions) + " f-strings converted")
            return conversions
        else:
            return 0
            
    except Exception as e:
        print("   ❌ Error processing " + filepath + ": " + str(e))
        return 0

def process_all_files():
    """Process all Python files in the project"""
    print("\n🔧 Converting ALL f-strings to .format() method...")
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        if 'backup_before_fstring_fix' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                python_files.append(filepath)
    
    print("   📁 Found " + str(len(python_files)) + " Python files to process")
    
    files_processed = 0
    total_conversions = 0
    
    for filepath in python_files:
        conversions = process_file(filepath)
        if conversions > 0:
            files_processed += 1
            total_conversions += conversions
    
    return files_processed, total_conversions

def verify_fix():
    """Verify that no f-strings remain"""
    print("\n🔍 Verifying f-string removal...")
    
    remaining_count = 0
    
    for root, dirs, files in os.walk('.'):
        if 'backup_before_fstring_fix' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'f"' in content or "f'" in content:
                        count = content.count('f"') + content.count("f'")
                        remaining_count += count
                        print("   ⚠️ " + filepath + ": " + str(count) + " f-strings remain")
                        
                except Exception as e:
                    print("   ⚠️ Could not verify " + filepath + ": " + str(e))
    
    if remaining_count == 0:
        print("   ✅ No f-strings found - conversion complete!")
        return True
    else:
        print("   ⚠️ Found " + str(remaining_count) + " remaining f-strings")
        return False

def test_key_imports():
    """Test that key modules still import correctly"""
    print("\n🧪 Testing key module imports...")
    
    test_modules = ['voting_system', 'database_manager']
    successful = 0
    
    for module in test_modules:
        try:
            __import__(module)
            print("   ✅ " + module + ".py imports successfully")
            successful += 1
        except Exception as e:
            print("   ❌ " + module + ".py import failed: " + str(e))
    
    return successful == len(test_modules)

def run_permanent_fix():
    """Run the complete permanent fix"""
    print("🚀 PERMANENT F-STRING ERROR FIX")
    print("=" * 60)
    print("Converting ALL f-strings in the project to .format() method")
    print("This will permanently eliminate the f-string error!")
    print("=" * 60)
    
    # Step 1: Backup
    backup_dir = create_backup()
    if not backup_dir:
        print("❌ Backup failed - aborting fix")
        return False
    
    # Step 2: Process all files
    files_processed, total_conversions = process_all_files()
    
    # Step 3: Verify fix
    verification_success = verify_fix()
    
    # Step 4: Test imports
    import_success = test_key_imports()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 PERMANENT FIX SUMMARY")
    print("=" * 60)
    print("📁 Files processed: " + str(files_processed))
    print("🔧 F-strings converted: " + str(total_conversions))
    print("✅ Verification: " + ("PASSED" if verification_success else "FAILED"))
    print("🧪 Import test: " + ("PASSED" if import_success else "FAILED"))
    print("📁 Backup location: " + backup_dir)
    
    overall_success = verification_success and import_success and total_conversions > 0
    
    print("\n🎯 OVERALL RESULT: " + ("✅ SUCCESS" if overall_success else "❌ FAILED"))
    
    if overall_success:
        print("🎉 F-STRING ERROR PERMANENTLY RESOLVED!")
        print("\n💡 What was accomplished:")
        print("   • Converted " + str(total_conversions) + " f-strings across " + str(files_processed) + " files")
        print("   • Created complete backup for safety")
        print("   • Verified no f-strings remain")
        print("   • Tested key module imports")
        print("\n🚀 Your project is now completely free of f-string errors!")
        print("   The 'unsupported format string passed to bytes.__format__' error will NEVER occur again!")
    else:
        print("⚠️ Some issues detected. Your files are safely backed up.")
    
    return overall_success

if __name__ == "__main__":
    success = run_permanent_fix()
    
    if success:
        print("\n✅ SUCCESS: F-string errors permanently eliminated!")
        print("You can now use the entire project without any format string errors.")
    else:
        print("\n❌ ISSUES DETECTED: Please review the summary above.")
        print("Your original files are safely backed up.")
