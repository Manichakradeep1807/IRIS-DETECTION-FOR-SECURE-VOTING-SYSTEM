"""
SUPER-FAST IRIS RECOGNITION MODEL TRAINER
Target: High Accuracy in 2-3 Minutes

This script implements optimized techniques for fast training:
- Efficient CNN architecture
- Optimized batch sizes
- Reduced epochs with smart early stopping
- Lightweight data augmentation
- Fast convergence techniques
"""

import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Dense, Dropout, Flatten, 
    BatchNormalization, GlobalAveragePooling2D
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import pickle
from datetime import datetime

def create_fast_efficient_model(input_shape=(64, 64, 3), num_classes=108):
    """Create fast and efficient CNN model optimized for speed"""
    
    model = Sequential([
        # First block - efficient feature extraction
        Conv2D(32, (5, 5), activation='relu', input_shape=input_shape),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Second block - deeper features
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Third block - high-level features
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Fourth block - final features
        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(),
        
        # Global pooling for efficiency
        GlobalAveragePooling2D(),
        
        # Dense layers with dropout
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    
    # Compile with optimized settings
    model.compile(
        optimizer=Adam(learning_rate=0.002),  # Higher learning rate for faster convergence
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_fast_augmentation(X_train, Y_train, X_val, Y_val, batch_size=64):
    """Create lightweight data augmentation for fast training"""
    
    # Minimal augmentation for speed
    train_datagen = ImageDataGenerator(
        rotation_range=5,
        width_shift_range=0.05,
        height_shift_range=0.05,
        zoom_range=0.05,
        brightness_range=[0.95, 1.05],
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator()
    
    train_generator = train_datagen.flow(
        X_train, Y_train,
        batch_size=batch_size,
        shuffle=True
    )
    
    val_generator = val_datagen.flow(
        X_val, Y_val,
        batch_size=batch_size,
        shuffle=False
    )
    
    return train_generator, val_generator

def get_fast_callbacks():
    """Get callbacks optimized for fast training"""
    
    callbacks = [
        # Aggressive early stopping for speed
        EarlyStopping(
            monitor='val_accuracy',
            patience=3,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Quick learning rate reduction
        ReduceLROnPlateau(
            monitor='val_accuracy',
            factor=0.5,
            patience=2,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    return callbacks

def train_fast_model():
    """Main function for super-fast training"""
    
    print("⚡ SUPER-FAST IRIS RECOGNITION TRAINING")
    print("🎯 TARGET: High Accuracy in 2-3 Minutes")
    print("=" * 50)
    
    # Load training data
    print("📊 Loading training data...")
    if not os.path.exists('model/X.txt.npy') or not os.path.exists('model/Y.txt.npy'):
        print("❌ No training data found!")
        print("Creating fast dataset...")
        
        # Create quick dataset if none exists
        import subprocess
        result = subprocess.run(['python', 'create_sample_dataset.py'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Failed to create dataset")
            return False
    
    X_train = np.load('model/X.txt.npy')
    Y_train = np.load('model/Y.txt.npy')
    
    print(f"   Dataset shape: {X_train.shape}")
    print(f"   Labels shape: {Y_train.shape}")
    
    # Fast preprocessing
    print("🔄 Fast preprocessing...")
    X_train = X_train.astype('float32')
    if X_train.max() > 1.0:
        X_train = X_train / 255.0
    
    # Quick data split
    X_train_split, X_val, Y_train_split, Y_val = train_test_split(
        X_train, Y_train, test_size=0.2, random_state=42
    )
    
    print(f"   Training samples: {X_train_split.shape[0]}")
    print(f"   Validation samples: {X_val.shape[0]}")
    
    # Create fast model
    print("🏗️ Creating fast efficient model...")
    model = create_fast_efficient_model(
        input_shape=X_train.shape[1:], 
        num_classes=Y_train.shape[1]
    )
    
    print(f"   Model parameters: {model.count_params():,}")
    
    # Create fast data generators
    print("🔄 Creating fast data generators...")
    train_generator, val_generator = create_fast_augmentation(
        X_train_split, Y_train_split, X_val, Y_val, batch_size=64
    )
    
    # Get fast callbacks
    callbacks = get_fast_callbacks()
    
    # Fast training
    print("🚀 SUPER-FAST TRAINING STARTING...")
    print("   ⚡ 10 epochs maximum (with early stopping)")
    print("   📦 Large batch size (64) for speed")
    print("   🔄 Minimal augmentation")
    print("   ⏰ Expected time: 2-3 minutes")
    
    start_time = datetime.now()
    
    history = model.fit(
        train_generator,
        steps_per_epoch=len(X_train_split) // 64,
        epochs=10,  # Few epochs for speed
        validation_data=val_generator,
        validation_steps=len(X_val) // 64,
        callbacks=callbacks,
        verbose=1
    )
    
    end_time = datetime.now()
    training_time = (end_time - start_time).total_seconds()
    
    # Save fast model
    print("💾 Saving fast model...")
    model.save_weights('model/fast_model.weights.h5')
    model_json = model.to_json()
    with open('model/fast_model.json', 'w') as json_file:
        json_file.write(model_json)
    
    with open('model/fast_history.pckl', 'wb') as f:
        pickle.dump(history.history, f)
    
    # Show results
    final_accuracy = max(history.history['accuracy']) * 100
    final_val_accuracy = max(history.history['val_accuracy']) * 100
    epochs_trained = len(history.history['accuracy'])
    
    print(f"\n⚡ SUPER-FAST TRAINING COMPLETED!")
    print(f"⏰ Training time: {training_time:.1f} seconds ({training_time/60:.1f} minutes)")
    print(f"🏆 Best Training Accuracy: {final_accuracy:.2f}%")
    print(f"🎯 Best Validation Accuracy: {final_val_accuracy:.2f}%")
    print(f"📊 Epochs completed: {epochs_trained}")
    
    if final_val_accuracy >= 95.0:
        print("🎉 EXCELLENT! 95%+ accuracy achieved in record time!")
    elif final_val_accuracy >= 90.0:
        print("✅ GREAT! 90%+ accuracy achieved quickly!")
    elif final_val_accuracy >= 85.0:
        print("👍 GOOD! 85%+ accuracy achieved fast!")
    else:
        print("📈 Model trained quickly - consider more epochs for higher accuracy")
    
    print(f"\n💡 Speed vs Accuracy Trade-off:")
    print(f"   ⚡ Training time: {training_time/60:.1f} minutes")
    print(f"   🎯 Accuracy achieved: {final_val_accuracy:.1f}%")
    print(f"   📈 Efficiency: {final_val_accuracy/training_time*60:.1f} accuracy points per minute")
    
    return final_val_accuracy >= 85.0

if __name__ == "__main__":
    success = train_fast_model()
    if success:
        print("\n✅ Fast model ready for use!")
        print("🚀 You can now test it with the main application!")
    else:
        print("\n📈 Training completed - check results above")
