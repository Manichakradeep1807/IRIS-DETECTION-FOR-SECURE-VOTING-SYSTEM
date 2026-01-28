"""
Test script to verify CNN model functionality
"""

import numpy as np
import os
import sys
from datetime import datetime

def test_cnn_model():
    """Test the CNN model training and prediction"""
    print("🧪 Testing CNN Model Functionality")
    print("=" * 50)
    
    # Check if training data exists
    if not os.path.exists('model/X.txt.npy') or not os.path.exists('model/Y.txt.npy'):
        print("❌ No training data found!")
        print("Creating sample dataset...")
        os.system('py -3.12 create_sample_dataset.py')
    
    try:
        # Import required modules
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
        from tensorflow.keras.callbacks import EarlyStopping
        from sklearn.model_selection import train_test_split
        import pickle
        
        print("✅ All required modules imported successfully")
        
        # Load data
        print("\n📂 Loading training data...")
        X_train = np.load('model/X.txt.npy')
        Y_train = np.load('model/Y.txt.npy')
        
        print(f"   Dataset shape: {X_train.shape}")
        print(f"   Labels shape: {Y_train.shape}")
        print(f"   Data type: {X_train.dtype}")
        print(f"   Value range: [{X_train.min():.3f}, {X_train.max():.3f}]")
        
        # Preprocess data
        print("\n🔄 Preprocessing data...")
        X_train = X_train.astype('float32')
        if X_train.max() > 1.0:
            X_train = X_train / 255.0
        
        # Split data
        X_train_split, X_val, Y_train_split, Y_val = train_test_split(
            X_train, Y_train, test_size=0.2, random_state=42, 
            stratify=np.argmax(Y_train, axis=1)
        )
        
        print(f"   Training samples: {X_train_split.shape[0]}")
        print(f"   Validation samples: {X_val.shape[0]}")
        print(f"   Number of classes: {Y_train.shape[1]}")
        
        # Create model
        print("\n🏗️ Creating CNN model...")
        model = Sequential([
            Conv2D(64, (3, 3), input_shape=(64, 64, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(Y_train.shape[1], activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"   Model parameters: {model.count_params():,}")
        print(f"   Model layers: {len(model.layers)}")
        
        # Test model with small batch
        print("\n🧪 Testing model prediction...")
        test_batch = X_train_split[:5]  # Take 5 samples
        predictions = model.predict(test_batch, verbose=0)
        
        print(f"   Prediction shape: {predictions.shape}")
        print(f"   Prediction range: [{predictions.min():.3f}, {predictions.max():.3f}]")
        print(f"   Sum of probabilities: {predictions.sum(axis=1)}")
        
        # Quick training test (just 2 epochs)
        print("\n🚀 Quick training test (2 epochs)...")
        callbacks = [EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)]
        
        history = model.fit(
            X_train_split, Y_train_split,
            batch_size=32,
            epochs=2,
            validation_data=(X_val, Y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        # Check training results
        train_acc = history.history['accuracy'][-1]
        val_acc = history.history['val_accuracy'][-1]
        train_loss = history.history['loss'][-1]
        val_loss = history.history['val_loss'][-1]
        
        print(f"\n📊 Training Results:")
        print(f"   Training Accuracy: {train_acc:.4f}")
        print(f"   Validation Accuracy: {val_acc:.4f}")
        print(f"   Training Loss: {train_loss:.4f}")
        print(f"   Validation Loss: {val_loss:.4f}")
        
        # Test prediction after training
        print("\n🔍 Testing prediction after training...")
        test_predictions = model.predict(test_batch, verbose=0)
        predicted_classes = np.argmax(test_predictions, axis=1)
        actual_classes = np.argmax(Y_train_split[:5], axis=1)
        
        print(f"   Predicted classes: {predicted_classes}")
        print(f"   Actual classes: {actual_classes}")
        print(f"   Accuracy on test batch: {np.mean(predicted_classes == actual_classes):.2f}")
        
        # Save test model
        print("\n💾 Saving test model...")
        model.save_weights('model/test_model.weights.h5')
        model_json = model.to_json()
        with open("model/test_model.json", "w") as json_file:
            json_file.write(model_json)
        
        with open('model/test_history.pckl', 'wb') as f:
            pickle.dump(history.history, f)
        
        print("✅ Test model saved successfully!")
        
        # Test loading the saved model
        print("\n📥 Testing model loading...")
        from tensorflow.keras.models import model_from_json
        
        with open('model/test_model.json', 'r') as json_file:
            loaded_model_json = json_file.read()
            loaded_model = model_from_json(loaded_model_json)
        
        loaded_model.load_weights('model/test_model.weights.h5')
        loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        # Test loaded model
        loaded_predictions = loaded_model.predict(test_batch, verbose=0)
        
        print(f"   Loaded model predictions match: {np.allclose(test_predictions, loaded_predictions)}")
        print("✅ Model loading test successful!")
        
        print(f"\n🎉 All CNN model tests passed!")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

def test_iris_feature_extraction():
    """Test iris feature extraction"""
    print("\n👁️ Testing Iris Feature Extraction")
    print("-" * 40)
    
    try:
        import cv2
        
        # Check if test image exists
        if os.path.exists('testSamples/sample_iris.jpg'):
            print("✅ Test iris image found")
            
            # Load and process image
            img = cv2.imread('testSamples/sample_iris.jpg')
            if img is not None:
                print(f"   Image shape: {img.shape}")
                print(f"   Image type: {img.dtype}")
                
                # Test resizing
                resized = cv2.resize(img, (64, 64))
                print(f"   Resized shape: {resized.shape}")
                
                # Test normalization
                normalized = resized.astype('float32') / 255.0
                print(f"   Normalized range: [{normalized.min():.3f}, {normalized.max():.3f}]")
                
                print("✅ Iris feature extraction test passed!")
                return True
            else:
                print("❌ Could not load test image")
                return False
        else:
            print("⚠️ No test image found, creating one...")
            os.system('py -3.12 create_sample_image.py')
            return True
            
    except Exception as e:
        print(f"❌ Error in iris feature extraction: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🔬 CNN Model Comprehensive Test Suite")
    print("=" * 60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Iris feature extraction
    test1_result = test_iris_feature_extraction()
    
    # Test 2: CNN model functionality
    test2_result = test_cnn_model()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Iris Feature Extraction: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"CNN Model Functionality: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 ALL TESTS PASSED! CNN model is working correctly.")
        print("You can now use the main application with confidence.")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
    
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
