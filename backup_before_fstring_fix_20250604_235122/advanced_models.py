"""
Advanced CNN Models for Iris Recognition
Includes ResNet-inspired architecture and modern deep learning techniques
"""

import tensorflow as tf
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import (
    Conv2D, BatchNormalization, Activation, MaxPooling2D, 
    GlobalAveragePooling2D, Dense, Dropout, Add, Input,
    DepthwiseConv2D, GlobalMaxPooling2D, Concatenate
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
import numpy as np

class ResidualBlock(tf.keras.layers.Layer):
    """Residual block for ResNet-inspired architecture"""
    
    def __init__(self, filters, stride=1, **kwargs):
        super(ResidualBlock, self).__init__(**kwargs)
        self.filters = filters
        self.stride = stride
        
        self.conv1 = Conv2D(filters, (3, 3), strides=stride, padding='same', use_bias=False)
        self.bn1 = BatchNormalization()
        self.conv2 = Conv2D(filters, (3, 3), strides=1, padding='same', use_bias=False)
        self.bn2 = BatchNormalization()
        
        # Shortcut connection
        if stride != 1:
            self.shortcut = Sequential([
                Conv2D(filters, (1, 1), strides=stride, padding='same', use_bias=False),
                BatchNormalization()
            ])
        else:
            self.shortcut = lambda x: x
    
    def call(self, inputs, training=None):
        x = self.conv1(inputs)
        x = self.bn1(x, training=training)
        x = Activation('relu')(x)
        
        x = self.conv2(x)
        x = self.bn2(x, training=training)
        
        shortcut = self.shortcut(inputs)
        x = Add()([x, shortcut])
        x = Activation('relu')(x)
        
        return x

def create_advanced_iris_model(input_shape=(64, 64, 3), num_classes=108):
    """
    Create advanced ResNet-inspired model for iris recognition
    """
    inputs = Input(shape=input_shape)
    
    # Initial convolution
    x = Conv2D(64, (7, 7), strides=2, padding='same', use_bias=False)(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((3, 3), strides=2, padding='same')(x)
    
    # Residual blocks
    x = ResidualBlock(64)(x)
    x = ResidualBlock(64)(x)
    
    x = ResidualBlock(128, stride=2)(x)
    x = ResidualBlock(128)(x)
    
    x = ResidualBlock(256, stride=2)(x)
    x = ResidualBlock(256)(x)
    
    # Global pooling and classification
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs, outputs, name='AdvancedIrisModel')
    return model

def create_efficient_iris_model(input_shape=(64, 64, 3), num_classes=108):
    """
    Create efficient model using depthwise separable convolutions
    """
    inputs = Input(shape=input_shape)
    
    # Initial convolution
    x = Conv2D(32, (3, 3), strides=2, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    
    # Depthwise separable convolutions
    for filters in [64, 128, 256]:
        x = DepthwiseConv2D((3, 3), padding='same')(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        
        x = Conv2D(filters, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        
        x = MaxPooling2D((2, 2))(x)
    
    # Global pooling and classification
    gap = GlobalAveragePooling2D()(x)
    gmp = GlobalMaxPooling2D()(x)
    x = Concatenate()([gap, gmp])
    
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs, outputs, name='EfficientIrisModel')
    return model

def compile_advanced_model(model, learning_rate=0.001):
    """
    Compile model with advanced optimizer and metrics
    """
    optimizer = Adam(
        learning_rate=learning_rate,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-7
    )
    
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_k_categorical_accuracy']
    )
    
    return model

def get_advanced_callbacks(model_path='model/best_model.h5'):
    """
    Get advanced training callbacks
    """
    callbacks = [
        ReduceLROnPlateau(
            monitor='val_accuracy',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            model_path,
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            verbose=1
        )
    ]
    
    return callbacks

def create_ensemble_model(models, input_shape=(64, 64, 3), num_classes=108):
    """
    Create ensemble of multiple models for better accuracy
    """
    inputs = Input(shape=input_shape)
    
    # Get predictions from each model
    predictions = []
    for i, model in enumerate(models):
        # Make each model non-trainable for ensemble
        for layer in model.layers:
            layer.trainable = False
            layer._name = f"{layer.name}_{i}"
        
        pred = model(inputs)
        predictions.append(pred)
    
    # Average predictions
    if len(predictions) > 1:
        averaged = tf.keras.layers.Average()(predictions)
    else:
        averaged = predictions[0]
    
    ensemble_model = Model(inputs, averaged, name='EnsembleIrisModel')
    return ensemble_model

# Loss functions for advanced training
def focal_loss(gamma=2.0, alpha=0.25):
    """
    Focal loss for handling class imbalance
    """
    def focal_loss_fixed(y_true, y_pred):
        epsilon = tf.keras.backend.epsilon()
        y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
        
        # Calculate focal loss
        alpha_t = y_true * alpha + (1 - y_true) * (1 - alpha)
        p_t = y_true * y_pred + (1 - y_true) * (1 - y_pred)
        focal_loss = -alpha_t * tf.pow((1 - p_t), gamma) * tf.math.log(p_t)
        
        return tf.reduce_mean(focal_loss)
    
    return focal_loss_fixed

def center_loss(alpha=0.5, num_classes=108, feature_dim=256):
    """
    Center loss for better feature learning
    """
    def center_loss_func(y_true, y_pred):
        # This is a simplified version - full implementation would require
        # custom training loop to update centers
        return tf.keras.losses.categorical_crossentropy(y_true, y_pred)
    
    return center_loss_func

if __name__ == "__main__":
    # Test model creation
    print("Creating advanced iris recognition models...")
    
    # Create models
    advanced_model = create_advanced_iris_model()
    efficient_model = create_efficient_iris_model()
    
    # Compile models
    advanced_model = compile_advanced_model(advanced_model)
    efficient_model = compile_advanced_model(efficient_model)
    
    print(f"Advanced model parameters: {advanced_model.count_params():,}")
    print(f"Efficient model parameters: {efficient_model.count_params():,}")
    
    # Print model summaries
    print("\nAdvanced Model Summary:")
    advanced_model.summary()
    
    print("\nEfficient Model Summary:")
    efficient_model.summary()
