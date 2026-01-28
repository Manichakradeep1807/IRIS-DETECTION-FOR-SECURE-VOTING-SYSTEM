"""
Advanced Data Augmentation for Iris Recognition
Includes specialized augmentations for biometric data
"""

import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import Sequence
import albumentations as A
from skimage import filters, exposure
import random

class IrisAugmentation:
    """
    Specialized augmentation for iris images
    """
    
    def __init__(self, 
                 rotation_range=15,
                 brightness_range=0.2,
                 contrast_range=0.2,
                 noise_factor=0.1,
                 blur_probability=0.3):
        
        self.rotation_range = rotation_range
        self.brightness_range = brightness_range
        self.contrast_range = contrast_range
        self.noise_factor = noise_factor
        self.blur_probability = blur_probability
        
        # Albumentations pipeline for advanced augmentations
        self.transform = A.Compose([
            A.Rotate(limit=rotation_range, p=0.7),
            A.RandomBrightnessContrast(
                brightness_limit=brightness_range,
                contrast_limit=contrast_range,
                p=0.8
            ),
            A.GaussNoise(var_limit=(10.0, 50.0), p=0.5),
            A.MotionBlur(blur_limit=3, p=blur_probability),
            A.GaussianBlur(blur_limit=3, p=blur_probability),
            A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.5),
            A.RandomGamma(gamma_limit=(80, 120), p=0.5),
            A.HueSaturationValue(
                hue_shift_limit=10,
                sat_shift_limit=20,
                val_shift_limit=20,
                p=0.3
            )
        ])
    
    def augment_image(self, image):
        """Apply augmentation to a single image"""
        if len(image.shape) == 3:
            # Convert to uint8 if needed
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)
            
            # Apply albumentations
            augmented = self.transform(image=image)
            return augmented['image'].astype(np.float32) / 255.0
        
        return image
    
    def augment_batch(self, images):
        """Apply augmentation to a batch of images"""
        augmented_images = []
        for image in images:
            augmented_images.append(self.augment_image(image))
        return np.array(augmented_images)

class AdvancedIrisGenerator(Sequence):
    """
    Advanced data generator for iris recognition with custom augmentations
    """
    
    def __init__(self, 
                 X, y, 
                 batch_size=32,
                 augmentation=True,
                 shuffle=True,
                 preprocessing_func=None):
        
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.augmentation = augmentation
        self.shuffle = shuffle
        self.preprocessing_func = preprocessing_func
        
        self.indices = np.arange(len(self.X))
        if self.shuffle:
            np.random.shuffle(self.indices)
        
        # Initialize augmentation
        if self.augmentation:
            self.augmenter = IrisAugmentation()
    
    def __len__(self):
        return int(np.ceil(len(self.X) / self.batch_size))
    
    def __getitem__(self, idx):
        # Get batch indices
        start_idx = idx * self.batch_size
        end_idx = min((idx + 1) * self.batch_size, len(self.X))
        batch_indices = self.indices[start_idx:end_idx]
        
        # Get batch data
        batch_X = self.X[batch_indices].copy()
        batch_y = self.y[batch_indices].copy()
        
        # Apply augmentation
        if self.augmentation:
            batch_X = self.augmenter.augment_batch(batch_X)
        
        # Apply preprocessing
        if self.preprocessing_func:
            batch_X = self.preprocessing_func(batch_X)
        
        return batch_X, batch_y
    
    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

def create_keras_augmentation():
    """
    Create Keras ImageDataGenerator with iris-specific augmentations
    """
    return ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=False,  # Don't flip iris images
        vertical_flip=False,
        brightness_range=[0.8, 1.2],
        channel_shift_range=0.1,
        fill_mode='nearest',
        preprocessing_function=preprocess_iris_image
    )

def preprocess_iris_image(image):
    """
    Preprocessing function for iris images
    """
    # Ensure image is in correct format
    if image.dtype != np.float32:
        image = image.astype(np.float32)
    
    # Normalize to [0, 1]
    if image.max() > 1.0:
        image = image / 255.0
    
    # Apply histogram equalization to enhance contrast
    if len(image.shape) == 3:
        # Convert to LAB color space for better contrast enhancement
        lab = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2LAB)
        lab[:, :, 0] = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(lab[:, :, 0])
        image = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB).astype(np.float32) / 255.0
    
    return image

def apply_gabor_filters(image, num_orientations=8):
    """
    Apply Gabor filters for texture enhancement
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    filtered_images = []
    for i in range(num_orientations):
        theta = i * np.pi / num_orientations
        kernel = cv2.getGaborKernel((21, 21), 5, theta, 2*np.pi*0.5, 0.5, 0, ktype=cv2.CV_32F)
        filtered = cv2.filter2D(gray, cv2.CV_8UC3, kernel)
        filtered_images.append(filtered)
    
    # Combine filtered images
    combined = np.stack(filtered_images, axis=-1)
    return combined

def enhance_iris_contrast(image):
    """
    Enhance iris image contrast using multiple techniques
    """
    if len(image.shape) == 3:
        # Convert to LAB color space
        lab = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2LAB)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        
        # Convert back to RGB
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB).astype(np.float32) / 255.0
    else:
        # For grayscale images
        enhanced = exposure.equalize_adapthist(image, clip_limit=0.03)
    
    return enhanced

def add_realistic_noise(image, noise_type='gaussian'):
    """
    Add realistic noise to iris images
    """
    if noise_type == 'gaussian':
        noise = np.random.normal(0, 0.05, image.shape)
        noisy_image = image + noise
    elif noise_type == 'salt_pepper':
        noisy_image = image.copy()
        # Salt noise
        salt_coords = tuple([np.random.randint(0, i - 1, int(0.01 * image.size)) 
                           for i in image.shape[:2]])
        noisy_image[salt_coords] = 1
        
        # Pepper noise
        pepper_coords = tuple([np.random.randint(0, i - 1, int(0.01 * image.size)) 
                             for i in image.shape[:2]])
        noisy_image[pepper_coords] = 0
    else:
        noisy_image = image
    
    return np.clip(noisy_image, 0, 1)

def simulate_lighting_variations(image):
    """
    Simulate different lighting conditions
    """
    # Random brightness adjustment
    brightness_factor = np.random.uniform(0.7, 1.3)
    adjusted = image * brightness_factor
    
    # Add gradient lighting effect
    h, w = image.shape[:2]
    gradient = np.linspace(0.8, 1.2, w)
    gradient = np.tile(gradient, (h, 1))
    
    if len(image.shape) == 3:
        gradient = np.expand_dims(gradient, axis=2)
        gradient = np.tile(gradient, (1, 1, 3))
    
    adjusted = adjusted * gradient
    
    return np.clip(adjusted, 0, 1)

class MixupGenerator:
    """
    Mixup data augmentation for iris recognition
    """
    
    def __init__(self, alpha=0.2):
        self.alpha = alpha
    
    def mixup(self, x1, y1, x2, y2):
        """Apply mixup to two samples"""
        lambda_param = np.random.beta(self.alpha, self.alpha)
        
        mixed_x = lambda_param * x1 + (1 - lambda_param) * x2
        mixed_y = lambda_param * y1 + (1 - lambda_param) * y2
        
        return mixed_x, mixed_y

def create_balanced_generator(X, y, batch_size=32, augmentation=True):
    """
    Create a balanced data generator that ensures equal representation of classes
    """
    unique_classes = np.unique(np.argmax(y, axis=1))
    class_indices = {}
    
    # Group indices by class
    for class_id in unique_classes:
        class_indices[class_id] = np.where(np.argmax(y, axis=1) == class_id)[0]
    
    def balanced_batch_generator():
        while True:
            batch_X = []
            batch_y = []
            
            samples_per_class = batch_size // len(unique_classes)
            
            for class_id in unique_classes:
                # Sample from this class
                indices = np.random.choice(
                    class_indices[class_id], 
                    size=samples_per_class, 
                    replace=True
                )
                
                for idx in indices:
                    image = X[idx].copy()
                    label = y[idx].copy()
                    
                    # Apply augmentation
                    if augmentation:
                        augmenter = IrisAugmentation()
                        image = augmenter.augment_image(image)
                    
                    batch_X.append(image)
                    batch_y.append(label)
            
            yield np.array(batch_X), np.array(batch_y)
    
    return balanced_batch_generator()

if __name__ == "__main__":
    # Test augmentation pipeline
    print("Testing iris augmentation pipeline...")
    
    # Create dummy data
    dummy_image = np.random.rand(64, 64, 3).astype(np.float32)
    
    # Test augmentation
    augmenter = IrisAugmentation()
    augmented = augmenter.augment_image(dummy_image)
    
    print("Original shape: {}".format(dummy_image.shape))
    print("Augmented shape: {}".format(augmented.shape))
    print("Augmentation pipeline test completed successfully!")
