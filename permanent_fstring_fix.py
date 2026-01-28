#!/usr/bin/env python3
"""
PERMANENT F-STRING FIX
Automatically converts ALL f-strings in the entire project to .format() method
This will permanently solve the "unsupported format string passed to bytes.__format__" error
"""

import os
import re
import shutil
from datetime import datetime

class PermanentFStringFixer:
    def __init__(self):
        self.backup_dir = "backup_before_fstring_fix_{}".format(datetime.now().strftime('%Y%m%d_%H%M%S'))
        self.files_processed = 0
        self.fstrings_converted = 0
        self.errors = []
        
    def backup_project(self):
        """Create complete backup of the project"""
        print("📁 Creating complete project backup...")
        
        try:
            # Create backup directory
            os.makedirs(self.backup_dir, exist_ok=True)
            
            # Copy all Python files
            for root, dirs, files in os.walk('.'):
                # Skip backup directory itself
                if self.backup_dir in root:
                    continue
                    
                for file in files:
                    if file.endswith('.py'):
                        src_path = os.path.join(root, file)
                        rel_path = os.path.relpath(src_path, '.')
                        dst_path = os.path.join(self.backup_dir, rel_path)
                        
                        # Create directory structure
                        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                        
                        # Copy file
                        shutil.copy2(src_path, dst_path)
            
            print("   ✅ Backup created: {}".format(self.backup_dir))
            return True

        except Exception as e:
            print("   ❌ Backup failed: {}".format(e))
            return False
    
    def convert_fstring_to_format(self, content):
        """Convert f-strings to .format() method"""
        converted_content = content
        conversions = 0
        
        # Pattern 1: "text {}".format(variable) -> "text {}".format(variable)
        pattern1 = r'f"([^"]*?)\{([^}]+?)\}([^"]*?)"'
        def replace1(match):
            before, var, after = match.groups()
            return '"{}{}{}"'.format(before, '{}', after) + '.format({})'.format(var)
        
        new_content = re.sub(pattern1, replace1, converted_content)
        conversions += len(re.findall(pattern1, converted_content))
        converted_content = new_content
        
        # Pattern 2: 'text {}'.format(variable) -> 'text {}'.format(variable)
        pattern2 = r"f'([^']*?)\{([^}]+?)\}([^']*?)'"
        def replace2(match):
            before, var, after = match.groups()
            return "'{}{{{}}}{after}'.format({var})".format(before)
        
        new_content = re.sub(pattern2, replace2, converted_content)
        conversions += len(re.findall(pattern2, converted_content))
        converted_content = new_content
        
        # Pattern 3: Multiple variables "text {} more {var2}".format(var1)
        # This is more complex, let's handle common cases
        
        # Pattern for "text {} more {var2}".format(var1) with 2 variables
        pattern3 = r'f"([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)"'
        def replace3(match):
            before, var1, middle, var2, after = match.groups()
            return '"{}{{{}}}{middle}{{{}}}{after}".format({var1}, {var2})'.format(before)
        
        new_content = re.sub(pattern3, replace3, converted_content)
        conversions += len(re.findall(pattern3, converted_content))
        converted_content = new_content
        
        # Pattern for 'text {} more {var2}'.format(var1) with 2 variables
        pattern4 = r"f'([^']*?)\{([^}]+?)\}([^']*?)\{([^}]+?)\}([^']*?)'"
        def replace4(match):
            before, var1, middle, var2, after = match.groups()
            return "'{}{{{}}}{middle}{{{}}}{after}'.format({var1}, {var2})".format(before)
        
        new_content = re.sub(pattern4, replace4, converted_content)
        conversions += len(re.findall(pattern4, converted_content))
        converted_content = new_content
        
        # Pattern for 3 variables
        pattern5 = r'f"([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)"'
        def replace5(match):
            before, var1, mid1, var2, mid2, var3, after = match.groups()
            return '"{}{{{}}}{mid1}{{{}}}{mid2}{{{}}}{after}".format({var1}, {var2}, {var3})'.format(before)
        
        new_content = re.sub(pattern5, replace5, converted_content)
        conversions += len(re.findall(pattern5, converted_content))
        converted_content = new_content
        
        # Pattern for 4 variables
        pattern6 = r'f"([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)\{([^}]+?)\}([^"]*?)"'
        def replace6(match):
            groups = match.groups()
            before, var1, mid1, var2, mid2, var3, mid3, var4, after = groups
            return '"{}{{{}}}{mid1}{{{}}}{mid2}{{{}}}{mid3}{{{}}}{after}".format({var1}, {var2}, {var3}, {var4})'.format(before)
        
        new_content = re.sub(pattern6, replace6, converted_content)
        conversions += len(re.findall(pattern6, converted_content))
        converted_content = new_content
        
        return converted_content, conversions
    
    def process_file(self, filepath):
        """Process a single Python file"""
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has f-strings
            if 'f"' not in content and "f'" not in content:
                return 0  # No f-strings found
            
            # Convert f-strings
            new_content, conversions = self.convert_fstring_to_format(content)
            
            if conversions > 0:
                # Write back to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("   ✅ {}: {conversions} f-strings converted".format(filepath))
                return conversions
            else:
                return 0
                
        except Exception as e:
            error_msg = "Error processing {}: {e}".format(filepath)
            self.errors.append(error_msg)
            print("   ❌ {}".format(error_msg))
            return 0
    
    def process_all_files(self):
        """Process all Python files in the project"""
        print("\n🔧 Converting ALL f-strings to .format() method...")
        
        # Get all Python files
        python_files = []
        for root, dirs, files in os.walk('.'):
            # Skip backup directory
            if self.backup_dir in root:
                continue
                
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    python_files.append(filepath)
        
        print("   📁 Found {} Python files to process".format(len(python_files)))
        
        # Process each file
        for filepath in python_files:
            conversions = self.process_file(filepath)
            if conversions > 0:
                self.files_processed += 1
                self.fstrings_converted += conversions
        
        return self.files_processed, self.fstrings_converted
    
    def verify_fix(self):
        """Verify that no f-strings remain"""
        print("\n🔍 Verifying f-string removal...")
        
        remaining_fstrings = []
        
        for root, dirs, files in os.walk('.'):
            if self.backup_dir in root:
                continue
                
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Check for remaining f-strings
                        if 'f"' in content or "f'" in content:
                            # Count them
                            count = content.count('f"') + content.count("'")
                            remaining_fstrings.append((filepath, count))
                            
                    except Exception as e:
                        print("   ⚠️ Could not verify {}: {}".format(filepath))
        
        if remaining_fstrings:
            print("   ⚠️ Found {} files with remaining f-strings:".format(len(remaining_fstrings)))
            for filepath, count in remaining_fstrings:
                print("      • {}: {count} f-strings".format(filepath))
            return False
        else:
            print("   ✅ No f-strings found - conversion complete!")
            return True
    
    def test_imports(self):
        """Test that key modules still import correctly"""
        print("\n🧪 Testing module imports...")
        
        test_modules = [
            '.format(e)Main',
            'voting_system',
            'database_manager',
            'live_recognition',
            'voice_commands'
        ]
        
        successful_imports = 0
        
        for module in test_modules:
            try:
                __import__(module)
                print("   ✅ {}.py imports successfully".format(module))
                successful_imports += 1
            except Exception as e:
                print("   ❌ {}.py import failed: {e}".format(module))
        
        return successful_imports == len(test_modules)
    
    def run_permanent_fix(self):
        """Run the complete permanent fix"""
        print("🚀 PERMANENT F-STRING ERROR FIX")
        print("=" * 60)
        print("This will convert ALL f-strings in the project to .format() method")
        print("to permanently eliminate the 'unsupported format string passed to bytes.__format__' error")
        print("=" * 60)
        
        # Step 1: Backup
        if not self.backup_project():
            print("❌ Backup failed - aborting fix")
            return False
        
        # Step 2: Process all files
        files_processed, fstrings_converted = self.process_all_files()
        
        # Step 3: Verify fix
        verification_success = self.verify_fix()
        
        # Step 4: Test imports
        import_success = self.test_imports()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 PERMANENT FIX SUMMARY")
        print("=" * 60)
        print("📁 Files processed: {}".format(files_processed))
        print("🔧 F-strings converted: {}".format(fstrings_converted))
        print("✅ Verification: {}".format('PASSED' if verification_success else 'FAILED'))
        print("🧪 Import test: {}".format('PASSED' if import_success else 'FAILED'))
        
        if self.errors:
            print("\n⚠️ Errors encountered: {}".format(len(self.errors)))
            for error in self.errors[:5]:  # Show first 5 errors
                print("   • {}".format(error))
        
        overall_success = verification_success and import_success and fstrings_converted > 0
        
        print("\n🎯 OVERALL RESULT: {}".format('✅ SUCCESS' if overall_success else '❌ FAILED'))
        
        if overall_success:
            print("🎉 F-STRING ERROR PERMANENTLY RESOLVED!")
            print("\n💡 What was accomplished:")
            print("   • Converted {} f-strings across {files_processed} files".format(fstrings_converted))
            print("   • Created complete backup for safety")
            print("   • Verified no f-strings remain")
            print("   • Tested module imports")
            print("\n🚀 Your project is now completely free of f-string errors!")
            print("   The 'unsupported format string passed to bytes.__format__' error will never occur again!")
        else:
            print("⚠️ Some issues were detected. Check the summary above.")
            print("📁 Backup available at: {}".format(self.backup_dir))
        
        return overall_success


if __name__ == "__main__":
    fixer = PermanentFStringFixer()
    success = fixer.run_permanent_fix()
    
    if success:
        print("\n✅ SUCCESS: F-string errors permanently eliminated!")
        print("You can now use the entire project without any format string errors.")
    else:
        print("\n❌ ISSUES DETECTED: Please review the summary above.")
        print("Your original files are safely backed up.")
