"""
Quick test to verify CNN model training works without errors
"""

import sys
import os

def test_cnn_training():
    """Test CNN model training functionality"""
    print("🧪 Quick CNN Training Test")
    print("=" * 30)
    
    try:
        # Import required modules
        import numpy as np
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
        from sklearn.model_selection import train_test_split
        
        print("✅ All imports successful")
        
        # Check if training data exists
        if not os.path.exists('model/X.txt.npy'):
            print("❌ No training data found!")
            print("Creating sample dataset...")
            os.system('py -3.12 create_sample_dataset.py')
        
        # Load data
        print("📂 Loading data...")
        X_train = np.load('model/X.txt.npy')
        Y_train = np.load('model/Y.txt.npy')
        
        print(f"   Data shape: {X_train.shape}")
        print(f"   Labels shape: {Y_train.shape}")
        
        # Preprocess
        X_train = X_train.astype('float32') / 255.0
        
        # Split data
        X_train_split, X_val, Y_train_split, Y_val = train_test_split(
            X_train, Y_train, test_size=0.2, random_state=42, 
            stratify=np.argmax(Y_train, axis=1)
        )
        
        print(f"   Training samples: {X_train_split.shape[0]}")
        print(f"   Validation samples: {X_val.shape[0]}")
        
        # Create model
        print("🏗️ Creating model...")
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
        
        # Quick training test (1 epoch)
        print("🚀 Quick training test (1 epoch)...")
        history = model.fit(
            X_train_split, Y_train_split,
            batch_size=32,
            epochs=1,
            validation_data=(X_val, Y_val),
            verbose=1
        )
        
        # Check results
        train_acc = history.history['accuracy'][0]
        val_acc = history.history['val_accuracy'][0]
        
        print(f"\n📊 Results:")
        print(f"   Training Accuracy: {train_acc:.4f}")
        print(f"   Validation Accuracy: {val_acc:.4f}")
        
        # Test prediction
        print("🔍 Testing prediction...")
        test_batch = X_train_split[:5]
        predictions = model.predict(test_batch, verbose=0)
        
        print(f"   Prediction shape: {predictions.shape}")
        print(f"   Prediction range: [{predictions.min():.3f}, {predictions.max():.3f}]")
        
        print("\n✅ CNN model test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_cnn_training()
    if success:
        print("\n🎉 CNN model is working correctly!")
        print("You can now use the main application.")
    else:
        print("\n⚠️ CNN model test failed. Please check the errors above.")
