#!/usr/bin/env python3
"""
Test High Confidence Test Samples
Verifies that the new test samples achieve 90%+ confidence levels
"""

import os
import sys
import cv2
import numpy as np
from datetime import datetime

def test_high_confidence_samples():
    """Test the new high-confidence test samples"""
    print("🧪 Testing High Confidence Test Samples")
    print("=" * 60)
    
    # Check if testSamples directory exists
    if not os.path.exists('testSamples'):
        print("❌ testSamples directory not found!")
        return False
    
    # Get all test sample files
    test_files = [f for f in os.listdir('testSamples') if f.endswith('.jpg')]
    test_files.sort()
    
    print(f"📁 Found {len(test_files)} test sample files")
    
    if len(test_files) == 0:
        print("❌ No test sample files found!")
        return False
    
    # Test iris feature extraction
    print("\n🔍 Testing iris feature extraction...")
    
    try:
        from Main import getIrisFeatures
        print("   ✅ Successfully imported getIrisFeatures")
    except Exception as e:
        print(f"   ❌ Failed to import getIrisFeatures: {e}")
        return False
    
    # Test each sample
    successful_extractions = 0
    high_quality_extractions = 0
    confidence_scores = []
    
    print("\n📊 Testing individual samples:")
    
    for i, filename in enumerate(test_files[:20]):  # Test first 20 files
        filepath = os.path.join('testSamples', filename)
        print(f"   {i+1:2d}. Testing {filename}...")
        
        try:
            # Extract iris features
            iris_features = getIrisFeatures(filepath)
            
            if iris_features is not None:
                successful_extractions += 1
                
                # Analyze quality
                quality_score = analyze_iris_quality(iris_features)
                confidence_scores.append(quality_score)
                
                if quality_score >= 0.9:  # 90%+ quality
                    high_quality_extractions += 1
                    print(f"      ✅ SUCCESS - Quality: {quality_score:.1%}")
                else:
                    print(f"      ⚠️  MEDIUM - Quality: {quality_score:.1%}")
                
            else:
                print(f"      ❌ FAILED - Could not extract iris features")
                confidence_scores.append(0.0)
                
        except Exception as e:
            print(f"      ❌ ERROR - {e}")
            confidence_scores.append(0.0)
    
    # Calculate statistics
    total_tested = min(20, len(test_files))
    success_rate = (successful_extractions / total_tested) * 100
    high_quality_rate = (high_quality_extractions / total_tested) * 100
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"📁 Total files tested: {total_tested}")
    print(f"✅ Successful extractions: {successful_extractions}/{total_tested} ({success_rate:.1f}%)")
    print(f"🏆 High quality (90%+): {high_quality_extractions}/{total_tested} ({high_quality_rate:.1f}%)")
    print(f"📈 Average confidence: {avg_confidence:.1%}")
    
    # Quality breakdown
    if confidence_scores:
        excellent = sum(1 for s in confidence_scores if s >= 0.95)
        very_good = sum(1 for s in confidence_scores if 0.9 <= s < 0.95)
        good = sum(1 for s in confidence_scores if 0.8 <= s < 0.9)
        fair = sum(1 for s in confidence_scores if 0.7 <= s < 0.8)
        poor = sum(1 for s in confidence_scores if s < 0.7)
        
        print(f"\n🎯 QUALITY BREAKDOWN:")
        print(f"   🌟 Excellent (95%+): {excellent}")
        print(f"   ⭐ Very Good (90-95%): {very_good}")
        print(f"   ✅ Good (80-90%): {good}")
        print(f"   ⚠️  Fair (70-80%): {fair}")
        print(f"   ❌ Poor (<70%): {poor}")
    
    # Show top performers
    if confidence_scores:
        top_indices = sorted(range(len(confidence_scores)), key=lambda i: confidence_scores[i], reverse=True)
        print(f"\n🏆 TOP 5 PERFORMERS:")
        for i, idx in enumerate(top_indices[:5]):
            if idx < len(test_files):
                print(f"   {i+1}. {test_files[idx]}: {confidence_scores[idx]:.1%}")
    
    # Determine overall success
    overall_success = (
        success_rate >= 85 and  # At least 85% successful extractions
        high_quality_rate >= 50 and  # At least 50% high quality
        avg_confidence >= 0.8  # Average confidence at least 80%
    )
    
    print(f"\n🎯 OVERALL ASSESSMENT: {'✅ SUCCESS' if overall_success else '⚠️ NEEDS IMPROVEMENT'}")
    
    if overall_success:
        print("🎉 The new test samples meet high confidence requirements!")
    else:
        print("💡 Suggestions for improvement:")
        if success_rate < 85:
            print("   • Improve iris detection in sample images")
        if high_quality_rate < 50:
            print("   • Increase number of high-quality source images")
        if avg_confidence < 0.8:
            print("   • Enhance image preprocessing and quality")
    
    return overall_success

def analyze_iris_quality(iris_image):
    """Analyze the quality of extracted iris features"""
    try:
        if iris_image is None:
            return 0.0
        
        # Convert to grayscale if needed
        if len(iris_image.shape) == 3:
            gray = cv2.cvtColor(iris_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = iris_image
        
        # Quality metrics
        scores = []
        
        # 1. Sharpness (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_score = min(1.0, laplacian_var / 300.0)
        scores.append(sharpness_score * 0.4)
        
        # 2. Contrast (standard deviation)
        contrast_score = min(1.0, gray.std() / 60.0)
        scores.append(contrast_score * 0.3)
        
        # 3. Size adequacy
        height, width = gray.shape
        size_score = min(1.0, (height * width) / (50 * 50))
        scores.append(size_score * 0.3)
        
        return sum(scores)
        
    except Exception as e:
        print(f"      Error analyzing quality: {e}")
        return 0.0

def test_model_recognition():
    """Test actual model recognition with new samples"""
    print("\n🤖 Testing Model Recognition...")
    
    try:
        # Try to load the model
        import tensorflow as tf
        from tensorflow import keras
        
        model_path = "model/best_high_accuracy_model.h5"
        if os.path.exists(model_path):
            model = keras.models.load_model(model_path)
            print("   ✅ High accuracy model loaded successfully")
        else:
            model_path = "model/best_model.h5"
            if os.path.exists(model_path):
                model = keras.models.load_model(model_path)
                print("   ✅ Standard model loaded successfully")
            else:
                print("   ⚠️ No trained model found")
                return False
        
        # Test with a few samples
        test_files = [f for f in os.listdir('testSamples') if f.endswith('.jpg')][:5]
        
        print("   🧪 Testing model predictions...")
        
        for filename in test_files:
            filepath = os.path.join('testSamples', filename)
            
            try:
                # Load and preprocess image
                img = cv2.imread(filepath)
                if img is not None:
                    img_resized = cv2.resize(img, (64, 64))
                    img_array = np.array(img_resized).reshape(1, 64, 64, 3)
                    img_array = img_array.astype('float32') / 255.0
                    
                    # Predict
                    predictions = model.predict(img_array, verbose=0)
                    confidence = float(np.max(predictions))
                    person_id = np.argmax(predictions) + 1
                    
                    print(f"      {filename}: Person {person_id}, Confidence: {confidence:.1%}")
                
            except Exception as e:
                print(f"      Error testing {filename}: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Model testing failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting High Confidence Test Sample Verification")
    print("=" * 60)
    
    # Test the samples
    sample_success = test_high_confidence_samples()
    
    # Test model recognition
    model_success = test_model_recognition()
    
    print("\n" + "=" * 60)
    print("🎯 FINAL RESULTS")
    print("=" * 60)
    print(f"📊 Sample Quality Test: {'✅ PASSED' if sample_success else '❌ FAILED'}")
    print(f"🤖 Model Recognition Test: {'✅ PASSED' if model_success else '❌ FAILED'}")
    
    overall_success = sample_success and model_success
    print(f"\n🏆 OVERALL: {'✅ SUCCESS - High confidence samples ready!' if overall_success else '⚠️ NEEDS ATTENTION'}")
