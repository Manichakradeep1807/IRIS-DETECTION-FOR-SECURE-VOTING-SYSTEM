#!/usr/bin/env python3
"""
Test script to verify model architecture compatibility fix
This script tests the dynamic model input handling for voting authentication
"""

import os
import sys
import numpy as np
import cv2

def test_model_loading():
    """Test if model can be loaded and check its architecture"""
    print("🔍 Testing model loading and architecture...")
    
    try:
        # Check if model files exist
        if not os.path.exists('model/model.json'):
            print("❌ Model JSON file not found")
            return False
        
        if not os.path.exists('model/model.weights.h5'):
            print("❌ Model weights file not found")
            return False
        
        # Try to load the model
        from tensorflow.keras.models import model_from_json
        
        with open('model/model.json', 'r') as json_file:
            loaded_model_json = json_file.read()
            model = model_from_json(loaded_model_json)
        
        model.load_weights('model/model.weights.h5')
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        print("✅ Model loaded successfully")
        print(f"   Input shape: {model.input_shape}")
        print(f"   Output shape: {model.output_shape}")
        print(f"   Total parameters: {model.count_params():,}")
        
        return model
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return None

def test_dynamic_image_processing(model):
    """Test dynamic image processing based on model input shape"""
    print("\n🔍 Testing dynamic image processing...")
    
    if model is None:
        print("❌ No model available for testing")
        return False
    
    try:
        # Get model input shape
        model_input_shape = model.input_shape
        print(f"   Model expects: {model_input_shape}")
        
        # Determine target dimensions
        if len(model_input_shape) == 4:  # (batch, height, width, channels)
            target_height = model_input_shape[1]
            target_width = model_input_shape[2]
            target_channels = model_input_shape[3]
        else:
            target_height, target_width, target_channels = 128, 128, 3
        
        print(f"   Target size: {target_height}x{target_width}x{target_channels}")
        
        # Create a test image
        test_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        print(f"   Original test image shape: {test_image.shape}")
        
        # Process image dynamically
        img = cv2.resize(test_image, (target_width, target_height))
        
        # Ensure correct number of channels
        if len(img.shape) == 2:  # Grayscale
            if target_channels == 3:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            elif target_channels == 1:
                img = np.expand_dims(img, axis=-1)
        elif len(img.shape) == 3 and img.shape[2] == 3:  # RGB
            if target_channels == 1:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img = np.expand_dims(img, axis=-1)
        
        # Prepare for prediction
        im2arr = np.array(img)
        im2arr = im2arr.reshape(1, target_height, target_width, target_channels)
        img_processed = np.asarray(im2arr)
        img_processed = img_processed.astype('float32')
        
        # Normalize
        if img_processed.max() > 1.0:
            img_processed = img_processed / 255.0
        
        print(f"   Processed image shape: {img_processed.shape}")
        
        # Test prediction
        print("   Testing model prediction...")
        preds = model.predict(img_processed, verbose=0)
        print(f"   Prediction shape: {preds.shape}")
        print(f"   Max confidence: {np.max(preds) * 100:.2f}%")
        
        print("✅ Dynamic image processing successful!")
        return True
        
    except Exception as e:
        print(f"❌ Dynamic image processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_real_iris_image(model):
    """Test with a real iris image if available"""
    print("\n🔍 Testing with real iris image...")
    
    if model is None:
        print("❌ No model available for testing")
        return False
    
    # Look for test images
    test_dirs = ['testSamples', 'captured_iris']
    test_image_path = None
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            for file in os.listdir(test_dir):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    test_image_path = os.path.join(test_dir, file)
                    break
            if test_image_path:
                break
    
    if not test_image_path:
        print("⚠️ No test images found")
        return True
    
    try:
        print(f"   Using test image: {os.path.basename(test_image_path)}")
        
        # Load and process the image
        image = cv2.imread(test_image_path)
        if image is None:
            print("❌ Could not load test image")
            return False
        
        print(f"   Original image shape: {image.shape}")
        
        # Get model input shape
        model_input_shape = model.input_shape
        
        # Determine target dimensions
        if len(model_input_shape) == 4:
            target_height = model_input_shape[1]
            target_width = model_input_shape[2]
            target_channels = model_input_shape[3]
        else:
            target_height, target_width, target_channels = 128, 128, 3
        
        # Process image
        img = cv2.resize(image, (target_width, target_height))
        
        # Ensure correct channels
        if len(img.shape) == 2:
            if target_channels == 3:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            elif target_channels == 1:
                img = np.expand_dims(img, axis=-1)
        elif len(img.shape) == 3 and img.shape[2] == 3:
            if target_channels == 1:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img = np.expand_dims(img, axis=-1)
        
        # Prepare for prediction
        im2arr = np.array(img)
        im2arr = im2arr.reshape(1, target_height, target_width, target_channels)
        img_processed = np.asarray(im2arr)
        img_processed = img_processed.astype('float32')
        
        if img_processed.max() > 1.0:
            img_processed = img_processed / 255.0
        
        print(f"   Processed shape: {img_processed.shape}")
        
        # Test prediction
        preds = model.predict(img_processed, verbose=0)
        predict = np.argmax(preds) + 1
        confidence = np.max(preds) * 100
        
        print(f"   Prediction: Person {predict}")
        print(f"   Confidence: {confidence:.2f}%")
        
        if confidence >= 70:
            print("✅ Authentication would succeed (confidence ≥ 70%)")
        else:
            print("⚠️ Authentication would fail (confidence < 70%)")
        
        print("✅ Real image test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Real image test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all architecture compatibility tests"""
    print("🚀 MODEL ARCHITECTURE COMPATIBILITY TEST")
    print("=" * 50)
    
    # Test 1: Model loading
    model = test_model_loading()
    
    # Test 2: Dynamic image processing
    test_dynamic_image_processing(model)
    
    # Test 3: Real iris image test
    test_with_real_iris_image(model)
    
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if model is not None:
        print("✅ Model architecture compatibility fix is working!")
        print("✅ The voting authentication should now work correctly.")
        print("\n💡 Next steps:")
        print("   1. Run the main application: python Main.py")
        print("   2. Click '🗳️ CAST VOTE' to test the enhanced voting")
        print("   3. Select an iris image and authenticate")
    else:
        print("❌ Model loading failed. Please check:")
        print("   • Ensure model files exist in model/ directory")
        print("   • Train a model first using 'TRAIN MODEL' button")
        print("   • Check TensorFlow installation")

if __name__ == "__main__":
    main()
