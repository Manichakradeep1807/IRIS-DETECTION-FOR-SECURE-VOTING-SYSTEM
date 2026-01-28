#!/usr/bin/env python3
"""
Test Gallery to Dataset Sync Functionality
Tests the automatic syncing of iris gallery images to sample dataset folder
"""

import os
import cv2
import numpy as np
import shutil
from datetime import datetime
import sys

def create_test_captured_images():
    """Create test captured iris images for testing sync functionality"""
    print("🧪 Creating test captured iris images...")
    
    capture_folder = "captured_iris"
    os.makedirs(capture_folder, exist_ok=True)
    
    # Create test images for different persons
    test_persons = [1, 2, 29, 70, 99]
    created_files = []
    
    for person_id in test_persons:
        for i in range(2):  # Create 2 images per person
            # Create a test composite image
            composite = np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8)
            
            # Add some visual elements to make it look like an iris capture
            cv2.rectangle(composite, (10, 30), (140, 160), (0, 255, 0), 2)  # Eye region
            cv2.rectangle(composite, (160, 30), (290, 160), (255, 0, 0), 2)  # Iris region
            
            # Add text labels
            cv2.putText(composite, f"Person {person_id} - Test", (10, 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(composite, "Eye Region", (10, 180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(composite, "Extracted Iris", (160, 180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            # Create filename with proper format
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            filename = f"iris_person{person_id}_{timestamp}_test{i+1}.jpg"
            filepath = os.path.join(capture_folder, filename)
            
            # Save the image
            cv2.imwrite(filepath, composite)
            created_files.append(filename)
            print(f"   ✅ Created: {filename}")
    
    print(f"📊 Created {len(created_files)} test images")
    return created_files

def test_sync_function():
    """Test the sync_gallery_to_dataset function"""
    print("\n🔄 Testing sync functionality...")
    
    try:
        # Import the sync function from Main.py
        sys.path.append('.')
        from Main import sync_gallery_to_dataset
        
        # Test the sync function
        synced_count, new_persons = sync_gallery_to_dataset()
        
        print(f"✅ Sync function executed successfully")
        print(f"   📊 Synced images: {synced_count}")
        print(f"   👤 New persons: {new_persons}")
        
        return True, synced_count, new_persons
        
    except Exception as e:
        print(f"❌ Error testing sync function: {e}")
        return False, 0, 0

def verify_dataset_structure():
    """Verify that the dataset structure is correct"""
    print("\n🔍 Verifying dataset structure...")
    
    dataset_folder = "sample_dataset"
    if not os.path.exists(dataset_folder):
        print("❌ Dataset folder not found")
        return False
    
    # Check for person folders
    person_folders = [f for f in os.listdir(dataset_folder) 
                     if os.path.isdir(os.path.join(dataset_folder, f)) and f.startswith('person_')]
    
    if not person_folders:
        print("❌ No person folders found in dataset")
        return False
    
    print(f"✅ Found {len(person_folders)} person folders")
    
    total_samples = 0
    for person_folder in sorted(person_folders):
        person_path = os.path.join(dataset_folder, person_folder)
        samples = [f for f in os.listdir(person_path) if f.startswith('sample_') and f.endswith('.jpg')]
        total_samples += len(samples)
        print(f"   👤 {person_folder}: {len(samples)} samples")
    
    print(f"📊 Total samples in dataset: {total_samples}")
    return True

def test_live_recognition_sync():
    """Test the live recognition auto-sync functionality"""
    print("\n🎥 Testing live recognition auto-sync...")
    
    try:
        # Import live recognition
        from live_recognition import LiveIrisRecognition
        
        # Create instance
        live_system = LiveIrisRecognition()
        
        # Create test iris and eye images
        iris_image = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        eye_roi = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Create test prediction
        prediction = {
            'person_id': 123,
            'confidence': 0.95
        }
        
        print("   🧪 Testing capture with auto-sync...")
        
        # Count existing files before
        capture_folder = "captured_iris"
        before_files = []
        if os.path.exists(capture_folder):
            before_files = [f for f in os.listdir(capture_folder) if f.endswith('.jpg')]
        
        # Test the capture method (which should auto-sync)
        live_system._capture_iris_image(iris_image, eye_roi, prediction)
        
        # Count files after
        after_files = []
        if os.path.exists(capture_folder):
            after_files = [f for f in os.listdir(capture_folder) if f.endswith('.jpg')]
        
        new_files = len(after_files) - len(before_files)
        
        if new_files > 0:
            print(f"   ✅ Captured {new_files} new image(s)")
            
            # Check if it was synced to dataset
            dataset_folder = "sample_dataset"
            person_folder = f"{dataset_folder}/person_123"
            if os.path.exists(person_folder):
                samples = [f for f in os.listdir(person_folder) if f.startswith('sample_')]
                print(f"   ✅ Auto-synced to dataset: {len(samples)} samples for person 123")
                return True
            else:
                print("   ⚠️ Image captured but not auto-synced to dataset")
                return False
        else:
            print("   ❌ No new images captured")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing live recognition sync: {e}")
        return False

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        # Remove test images from captured_iris
        capture_folder = "captured_iris"
        if os.path.exists(capture_folder):
            test_files = [f for f in os.listdir(capture_folder) if 'test' in f]
            for test_file in test_files:
                os.remove(os.path.join(capture_folder, test_file))
                print(f"   🗑️ Removed: {test_file}")
        
        # Remove test person folders from dataset
        dataset_folder = "sample_dataset"
        if os.path.exists(dataset_folder):
            test_persons = ['person_123']  # From live recognition test
            for person_folder in test_persons:
                person_path = os.path.join(dataset_folder, person_folder)
                if os.path.exists(person_path):
                    shutil.rmtree(person_path)
                    print(f"   🗑️ Removed: {person_folder}")
        
        print("✅ Cleanup completed")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

def main():
    """Main test function"""
    print("🧪 IRIS GALLERY TO DATASET SYNC - COMPREHENSIVE TEST")
    print("=" * 70)
    print("This test verifies that iris gallery images are properly linked")
    print("to the sample dataset folder structure.")
    print()
    
    # Step 1: Create test data
    test_files = create_test_captured_images()
    
    # Step 2: Test sync function
    sync_success, synced_count, new_persons = test_sync_function()
    
    # Step 3: Verify dataset structure
    structure_ok = verify_dataset_structure()
    
    # Step 4: Test live recognition auto-sync
    live_sync_ok = test_live_recognition_sync()
    
    # Step 5: Show results
    print("\n" + "=" * 70)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 70)
    print(f"✅ Test data creation: {'PASS' if test_files else 'FAIL'}")
    print(f"✅ Sync function: {'PASS' if sync_success else 'FAIL'}")
    print(f"✅ Dataset structure: {'PASS' if structure_ok else 'FAIL'}")
    print(f"✅ Live recognition auto-sync: {'PASS' if live_sync_ok else 'FAIL'}")
    
    if synced_count > 0:
        print(f"\n📊 Sync Statistics:")
        print(f"   🔄 Images synced: {synced_count}")
        print(f"   👤 New persons: {new_persons}")
    
    # Overall result
    all_tests_passed = all([test_files, sync_success, structure_ok, live_sync_ok])
    
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if all_tests_passed else '❌ SOME TESTS FAILED'}")
    
    if all_tests_passed:
        print("\n🎉 Gallery to Dataset sync is working correctly!")
        print("   • Captured iris images are automatically synced to sample_dataset/")
        print("   • Person folders are created automatically")
        print("   • Live recognition includes auto-sync functionality")
        print("   • Manual sync function works properly")
    
    # Ask about cleanup
    print(f"\n🧹 Cleanup test data? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            cleanup_test_data()
        else:
            print("   Test data preserved for manual inspection")
    except:
        print("   Skipping cleanup (no input)")

if __name__ == "__main__":
    main()
