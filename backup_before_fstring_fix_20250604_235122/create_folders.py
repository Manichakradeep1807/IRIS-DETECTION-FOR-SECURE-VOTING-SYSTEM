"""
Create and verify all required folders for the iris recognition system
This script ensures all directories are properly created and visible
"""

import os
import sys

def create_required_folders():
    """Create all required folders for the iris recognition system"""
    
    print("📁 CREATING REQUIRED FOLDERS FOR IRIS RECOGNITION SYSTEM")
    print("=" * 60)
    
    # List of required directories
    required_folders = [
        'model',
        'captured_iris',
        'testSamples', 
        'sample_dataset',
        'logs',
        'screenshots',
        'temp'
    ]
    
    created_folders = []
    existing_folders = []
    
    for folder in required_folders:
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
                created_folders.append(folder)
                print(f"✅ Created: {folder}/")
            else:
                existing_folders.append(folder)
                print(f"📁 Already exists: {folder}/")
                
        except Exception as e:
            print(f"❌ Error creating {folder}: {e}")
    
    print("\n" + "=" * 60)
    print("📊 FOLDER CREATION SUMMARY:")
    print(f"   ✅ Created: {len(created_folders)} folders")
    print(f"   📁 Already existed: {len(existing_folders)} folders")
    
    if created_folders:
        print(f"\n🆕 NEW FOLDERS CREATED:")
        for folder in created_folders:
            print(f"   • {folder}/")
    
    if existing_folders:
        print(f"\n📂 EXISTING FOLDERS:")
        for folder in existing_folders:
            print(f"   • {folder}/")
    
    return True

def verify_folders():
    """Verify all folders are accessible and show their contents"""
    
    print("\n🔍 VERIFYING FOLDER ACCESS AND CONTENTS")
    print("=" * 60)
    
    folders_to_check = [
        'captured_iris',
        'testSamples',
        'model',
        'sample_dataset'
    ]
    
    for folder in folders_to_check:
        print(f"\n📁 {folder}/")
        try:
            if os.path.exists(folder):
                files = os.listdir(folder)
                if files:
                    print(f"   📄 Contains {len(files)} items:")
                    # Show first 5 files
                    for i, file in enumerate(files[:5]):
                        print(f"      • {file}")
                    if len(files) > 5:
                        print(f"      ... and {len(files) - 5} more items")
                else:
                    print("   📭 Empty folder")
            else:
                print("   ❌ Folder does not exist!")
        except Exception as e:
            print(f"   ❌ Error accessing folder: {e}")

def create_test_image():
    """Create a test image in captured_iris folder to verify it works"""
    
    print("\n🖼️ CREATING TEST IMAGE IN captured_iris FOLDER")
    print("=" * 60)
    
    try:
        import cv2
        import numpy as np
        from datetime import datetime
        
        # Create a simple test image
        test_image = np.zeros((200, 200, 3), dtype=np.uint8)
        
        # Add some content to the image
        cv2.circle(test_image, (100, 100), 80, (100, 150, 200), -1)
        cv2.circle(test_image, (100, 100), 30, (50, 50, 50), -1)
        cv2.putText(test_image, 'TEST', (70, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Save test image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_filename = f"captured_iris/test_image_{timestamp}.jpg"
        
        cv2.imwrite(test_filename, test_image)
        print(f"✅ Test image created: {test_filename}")
        
        # Verify the image was created
        if os.path.exists(test_filename):
            file_size = os.path.getsize(test_filename)
            print(f"   📏 File size: {file_size} bytes")
            print(f"   📍 Full path: {os.path.abspath(test_filename)}")
        else:
            print("❌ Test image was not created successfully")
            
    except ImportError:
        print("⚠️ OpenCV not available - skipping test image creation")
    except Exception as e:
        print(f"❌ Error creating test image: {e}")

def show_folder_paths():
    """Show full paths to all important folders"""
    
    print("\n🗺️ FULL FOLDER PATHS")
    print("=" * 60)
    
    current_dir = os.path.abspath(".")
    print(f"📍 Current directory: {current_dir}")
    
    important_folders = [
        'captured_iris',
        'testSamples',
        'model',
        'sample_dataset'
    ]
    
    for folder in important_folders:
        full_path = os.path.abspath(folder)
        exists = "✅" if os.path.exists(folder) else "❌"
        print(f"   {exists} {folder}: {full_path}")

def main():
    """Main function to create and verify all folders"""
    
    print("🚀 IRIS RECOGNITION SYSTEM - FOLDER SETUP")
    print("This script will create and verify all required folders")
    print("=" * 60)
    
    # Create required folders
    create_required_folders()
    
    # Verify folders
    verify_folders()
    
    # Show full paths
    show_folder_paths()
    
    # Create test image
    create_test_image()
    
    print("\n🎉 FOLDER SETUP COMPLETED!")
    print("=" * 60)
    print("📁 All required folders have been created and verified")
    print("🔍 You should now be able to see the 'captured_iris' folder")
    print("📍 Location: " + os.path.abspath("captured_iris"))
    
    print("\n💡 NEXT STEPS:")
    print("1. Run the iris recognition system: python Main.py")
    print("2. Use live recognition to capture images")
    print("3. Check the captured_iris folder for saved images")
    print("4. Use the gallery feature to view captured images")

if __name__ == "__main__":
    main()
