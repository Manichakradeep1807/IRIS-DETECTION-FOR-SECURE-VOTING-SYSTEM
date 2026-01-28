#!/usr/bin/env python3
"""
Sync Gallery to Dataset Script
Automatically syncs captured iris images from gallery to sample dataset folder structure
"""

import os
import shutil
import sys
from datetime import datetime

def sync_gallery_to_dataset():
    """Sync captured iris images to sample dataset folder structure"""
    print("🔄 IRIS GALLERY TO DATASET SYNC")
    print("=" * 50)
    
    try:
        capture_folder = "captured_iris"
        dataset_folder = "sample_dataset"
        
        # Check if captured images folder exists
        if not os.path.exists(capture_folder):
            print("❌ No captured images folder found!")
            print("   To capture iris images:")
            print("   1. Run the main iris recognition system")
            print("   2. Click 'LIVE RECOGNITION'")
            print("   3. Let the system recognize iris patterns")
            print("   4. Images will be automatically captured")
            return False
            
        # Ensure dataset folder exists
        os.makedirs(dataset_folder, exist_ok=True)
        print("📁 Dataset folder: {}".format(dataset_folder))
        
        synced_count = 0
        new_persons = 0
        skipped_count = 0
        error_count = 0
        
        # Get all captured images
        image_files = [f for f in os.listdir(capture_folder) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print("📊 Found {} captured images".format(len(image_files)))
        print()
        
        if not image_files:
            print("ℹ️ No images to sync")
            return True
        
        for filename in image_files:
            print("Processing: {}".format(filename))
            
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Extract person ID from filename (iris_person[ID]_timestamp.jpg)
                try:
                    if filename.startswith('iris_person'):
                        # Extract person ID
                        parts = filename.split('_')
                        if len(parts) >= 2:
                            person_part = parts[1]  # person[ID]
                            person_id = person_part.replace('person', '')
                            
                            print("   👤 Person ID: {}".format(person_id))
                            
                            # Create person folder in dataset
                            person_folder = "{}/person_{person_id.zfill(3)}".format(dataset_folder)
                            if not os.path.exists(person_folder):
                                os.makedirs(person_folder, exist_ok=True)
                                new_persons += 1
                                print("   📁 Created new person folder: {}".format(person_folder))
                            
                            # Count existing samples in person folder
                            existing_samples = len([f for f in os.listdir(person_folder) 
                                                  if f.startswith('sample_') and f.endswith('.jpg')])
                            
                            # Copy image to dataset with sample naming
                            source_path = os.path.join(capture_folder, filename)
                            sample_filename = "sample_{}.jpg".format(existing_samples + 1)
                            dest_path = os.path.join(person_folder, sample_filename)
                            
                            # Only copy if not already exists
                            if not os.path.exists(dest_path):
                                shutil.copy2(source_path, dest_path)
                                synced_count += 1
                                print("   ✅ Synced to: {}".format(dest_path))
                            else:
                                skipped_count += 1
                                print("   ⏭️ Already exists: {}".format(dest_path))
                        else:
                            print(f"   ⚠️ Could not parse filename format")
                            error_count += 1
                    else:
                        print(f"   ⚠️ Not an iris image (doesn't start with 'iris_person')")
                        error_count += 1
                        
                except Exception as e:
                    print("   ❌ Error processing {}: {e}".format(filename))
                    error_count += 1
                    continue
            
            print()  # Empty line for readability
                    
        # Print summary
        print("=" * 50)
        print("📋 SYNC SUMMARY")
        print("=" * 50)
        print("✅ Successfully synced: {} images".format(synced_count))
        print("👤 New person folders created: {}".format(new_persons))
        print("⏭️ Already synced (skipped): {}".format(skipped_count))
        print("❌ Errors: {}".format(error_count))
        print()
        
        if synced_count > 0:
            print("🎉 Sync completed successfully!")
            print("📁 Images are now available in: {}/".format(dataset_folder))
            print("   You can now use these images for training the model")
        elif skipped_count > 0:
            print("ℹ️ All images were already synced to dataset")
        else:
            print("⚠️ No images were synced")
            
        return True
        
    except Exception as e:
        print("❌ Error in sync process: {}".format(e))
        return False

def show_dataset_structure():
    """Show the current dataset structure"""
    print("\n📁 CURRENT DATASET STRUCTURE")
    print("=" * 50)
    
    dataset_folder = "sample_dataset"
    if not os.path.exists(dataset_folder):
        print("❌ Dataset folder does not exist")
        return
    
    person_folders = [f for f in os.listdir(dataset_folder) 
                     if os.path.isdir(os.path.join(dataset_folder, f)) and f.startswith('person_')]
    
    if not person_folders:
        print("📂 Dataset folder is empty")
        return
    
    person_folders.sort()
    total_images = 0
    
    for person_folder in person_folders:
        person_path = os.path.join(dataset_folder, person_folder)
        images = [f for f in os.listdir(person_path) if f.endswith('.jpg')]
        total_images += len(images)
        print("👤 {}: {len(images)} images".format(person_folder))
    
    print("\n📊 Total: {} people, {total_images} images".format(len(person_folders)))

def main():
    """Main function"""
    print("🖼️ IRIS GALLERY TO DATASET SYNC TOOL")
    print("=" * 60)
    print("This tool syncs captured iris images to the sample dataset folder")
    print("for training and recognition purposes.")
    print()
    
    # Show current status
    capture_folder = "captured_iris"
    if os.path.exists(capture_folder):
        captured_files = [f for f in os.listdir(capture_folder) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print("📸 Captured images: {}".format(len(captured_files)))
    else:
        print("📸 Captured images: 0 (folder not found)")
    
    # Show dataset status
    dataset_folder = "sample_dataset"
    if os.path.exists(dataset_folder):
        person_folders = [f for f in os.listdir(dataset_folder) 
                         if os.path.isdir(os.path.join(dataset_folder, f))]
        print("📁 Dataset persons: {}".format(len(person_folders)))
    else:
        print("📁 Dataset persons: 0 (folder not found)")
    
    print()
    
    # Perform sync
    success = sync_gallery_to_dataset()
    
    if success:
        # Show updated structure
        show_dataset_structure()
    
    print("\n" + "=" * 60)
    print("🔧 USAGE TIPS")
    print("=" * 60)
    print("• Run this script after capturing iris images")
    print("• Images will be organized by person ID in sample_dataset/")
    print("• Each person folder contains sample_1.jpg, sample_2.jpg, etc.")
    print("• Use these organized images for model training")
    print("• The main application now auto-syncs new captures")

if __name__ == "__main__":
    main()
