import numpy as np
import cv2
import os
from keras.utils import to_categorical

def create_sample_iris_dataset():
    """
    Creates a sample iris dataset for testing the deep learning model
    """
    print("Creating sample iris dataset...")
    
    # Create directories
    os.makedirs('model', exist_ok=True)
    os.makedirs('sample_dataset', exist_ok=True)
    
    # Parameters
    num_classes = 108  # Number of different people
    samples_per_class = 5  # Images per person
    img_size = 64
    
    X_data = []
    y_data = []
    
    for person_id in range(num_classes):
        print(f"Generating samples for person {person_id + 1}/{num_classes}")
        
        for sample in range(samples_per_class):
            # Create a unique iris pattern for each person
            img = create_unique_iris(person_id, sample, img_size)
            
            # Save sample image
            person_dir = f'sample_dataset/person_{person_id+1:03d}'
            os.makedirs(person_dir, exist_ok=True)
            cv2.imwrite(f'{person_dir}/sample_{sample+1}.jpg', img)
            
            # Add to dataset
            X_data.append(img)
            y_data.append(person_id)
    
    # Convert to numpy arrays
    X_data = np.array(X_data, dtype=np.float32) / 255.0  # Normalize
    y_data = to_categorical(y_data, num_classes)
    
    # Save dataset
    np.save('model/X.txt.npy', X_data)
    np.save('model/Y.txt.npy', y_data)
    
    print(f"Dataset created successfully!")
    print(f"Shape: X={X_data.shape}, Y={y_data.shape}")
    print(f"Saved to: model/X.txt.npy and model/Y.txt.npy")

def create_unique_iris(person_id, sample_id, size):
    """
    Creates a unique iris pattern based on person_id and sample_id
    """
    # Create base image
    img = np.zeros((size, size, 3), dtype=np.uint8)
    center = size // 2
    
    # Use person_id to create unique patterns
    np.random.seed(person_id * 100 + sample_id)
    
    # Outer iris boundary
    outer_radius = int(size * 0.35)
    inner_radius = int(size * 0.15)
    
    # Create iris texture
    for r in range(inner_radius, outer_radius):
        for angle in range(0, 360, 2):
            # Create unique pattern based on person_id
            pattern_value = int(100 + 50 * np.sin(angle * person_id * 0.1) + 
                              30 * np.cos(r * person_id * 0.05))
            pattern_value = max(50, min(200, pattern_value))
            
            x = int(center + r * np.cos(np.radians(angle)))
            y = int(center + r * np.sin(np.radians(angle)))
            
            if 0 <= x < size and 0 <= y < size:
                img[y, x] = [pattern_value, pattern_value, pattern_value]
    
    # Add pupil
    cv2.circle(img, (center, center), inner_radius, (0, 0, 0), -1)
    
    # Add some noise for variation
    noise = np.random.normal(0, 10, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return img

if __name__ == "__main__":
    try:
        create_sample_iris_dataset()
        print("\nSample dataset creation completed!")
        print("You can now train the model using the 'Generate & Load CNN Model' button")
    except ImportError as e:
        print(f"Error: {e}")
        print("Please make sure TensorFlow and Keras are installed.")
        print("Run setup_python311.bat first to install all dependencies.")
    except Exception as e:
        print(f"Error creating dataset: {e}")
