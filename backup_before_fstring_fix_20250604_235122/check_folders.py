"""
Quick script to check if captured_iris folder exists and show its contents
"""

import os
from datetime import datetime

def check_captured_iris_folder():
    """Check the captured_iris folder status"""
    
    print("🔍 CHECKING captured_iris FOLDER STATUS")
    print("=" * 50)
    
    folder_path = "captured_iris"
    full_path = os.path.abspath(folder_path)
    
    print(f"📍 Looking for folder: {folder_path}")
    print(f"📍 Full path: {full_path}")
    
    if os.path.exists(folder_path):
        print("✅ captured_iris folder EXISTS!")
        
        try:
            files = os.listdir(folder_path)
            print(f"📄 Contains {len(files)} files:")
            
            if files:
                for i, file in enumerate(files):
                    file_path = os.path.join(folder_path, file)
                    file_size = os.path.getsize(file_path)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    print(f"   {i+1}. {file}")
                    print(f"      Size: {file_size} bytes")
                    print(f"      Modified: {mod_time}")
                    print()
            else:
                print("   📭 Folder is empty")
                
        except Exception as e:
            print(f"❌ Error reading folder contents: {e}")
            
    else:
        print("❌ captured_iris folder DOES NOT EXIST!")
        print("🛠️ Creating the folder now...")
        
        try:
            os.makedirs(folder_path)
            print("✅ captured_iris folder created successfully!")
        except Exception as e:
            print(f"❌ Error creating folder: {e}")

def check_all_folders():
    """Check all important folders"""
    
    print("\n📁 CHECKING ALL IMPORTANT FOLDERS")
    print("=" * 50)
    
    folders = [
        "captured_iris",
        "testSamples", 
        "model",
        "sample_dataset"
    ]
    
    for folder in folders:
        if os.path.exists(folder):
            try:
                file_count = len(os.listdir(folder))
                print(f"✅ {folder}/ - {file_count} items")
            except:
                print(f"✅ {folder}/ - exists but can't read contents")
        else:
            print(f"❌ {folder}/ - does not exist")

def show_windows_explorer_command():
    """Show command to open folder in Windows Explorer"""
    
    print("\n🖥️ OPEN FOLDER IN WINDOWS EXPLORER")
    print("=" * 50)
    
    current_dir = os.path.abspath(".")
    captured_iris_path = os.path.join(current_dir, "captured_iris")
    
    print("To open the captured_iris folder in Windows Explorer:")
    print(f"1. Press Windows + R")
    print(f"2. Type: explorer \"{captured_iris_path}\"")
    print(f"3. Press Enter")
    print()
    print("Or copy this path and paste in File Explorer address bar:")
    print(f"{captured_iris_path}")

if __name__ == "__main__":
    check_captured_iris_folder()
    check_all_folders()
    show_windows_explorer_command()
    
    print("\n🎯 SUMMARY")
    print("=" * 50)
    print("If the captured_iris folder exists but you can't see it:")
    print("1. Make sure to show hidden files in Windows Explorer")
    print("2. Refresh the folder view (F5)")
    print("3. Check the exact path shown above")
    print("4. Run: python create_folders.py to ensure all folders exist")
