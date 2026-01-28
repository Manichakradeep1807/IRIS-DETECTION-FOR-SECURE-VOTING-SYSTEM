"""
Create Realistic Iris Sample Images
Generates synthetic but realistic-looking iris images for testing
"""

import cv2
import numpy as np
import os
import random
from datetime import datetime

def create_realistic_iris(size=(400, 400), person_id=1):
    """Create a realistic-looking iris image"""
    
    # Create base image
    img = np.zeros((size[0], size[1], 3), dtype=np.uint8)
    center = (size[0]//2, size[1]//2)
    
    # Generate unique iris patterns based on person_id
    np.random.seed(person_id * 42)  # Consistent patterns for same person
    
    # Eye background (sclera)
    cv2.circle(img, center, size[0]//2 - 10, (245, 245, 240), -1)
    
    # Iris outer boundary
    iris_radius = random.randint(80, 120)
    iris_colors = [
        (139, 69, 19),   # Brown
        (34, 139, 34),   # Green  
        (70, 130, 180),  # Blue
        (105, 105, 105), # Gray
        (160, 82, 45),   # Hazel
    ]
    
    base_color = iris_colors[person_id % len(iris_colors)]
    
    # Create iris with gradient
    for r in range(iris_radius, 0, -1):
        intensity = 0.3 + 0.7 * (r / iris_radius)
        color = tuple(int(c * intensity) for c in base_color)
        cv2.circle(img, center, r, color, -1)
    
    # Add iris texture patterns
    num_lines = random.randint(15, 25)
    for i in range(num_lines):
        angle = (2 * np.pi * i) / num_lines + random.uniform(-0.2, 0.2)
        start_r = random.randint(20, 40)
        end_r = iris_radius - random.randint(5, 15)
        
        start_x = int(center[0] + start_r * np.cos(angle))
        start_y = int(center[1] + start_r * np.sin(angle))
        end_x = int(center[0] + end_r * np.cos(angle))
        end_y = int(center[1] + end_r * np.sin(angle))
        
        # Vary line color slightly
        line_color = tuple(max(0, min(255, c + random.randint(-30, 30))) for c in base_color)
        cv2.line(img, (start_x, start_y), (end_x, end_y), line_color, random.randint(1, 3))
    
    # Add circular patterns
    num_circles = random.randint(3, 8)
    for i in range(num_circles):
        circle_r = random.randint(iris_radius//4, iris_radius - 10)
        circle_color = tuple(max(0, min(255, c + random.randint(-20, 20))) for c in base_color)
        cv2.circle(img, center, circle_r, circle_color, 1)
    
    # Pupil
    pupil_radius = random.randint(25, 45)
    cv2.circle(img, center, pupil_radius, (0, 0, 0), -1)
    
    # Add pupil reflection
    reflection_center = (center[0] - pupil_radius//3, center[1] - pupil_radius//3)
    cv2.circle(img, reflection_center, pupil_radius//4, (255, 255, 255), -1)
    
    # Add some noise for realism
    noise = np.random.normal(0, 10, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Add slight blur for realism
    img = cv2.GaussianBlur(img, (3, 3), 0.5)
    
    return img

def create_eye_context(iris_img, size=(600, 400)):
    """Create a full eye context around the iris"""
    
    # Create larger canvas
    eye_img = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    
    # Add skin tone background
    skin_color = (220, 180, 140)
    eye_img[:] = skin_color
    
    # Add some skin texture
    for _ in range(100):
        x = random.randint(0, size[0]-1)
        y = random.randint(0, size[1]-1)
        cv2.circle(eye_img, (x, y), 1, 
                  tuple(max(0, min(255, c + random.randint(-20, 20))) for c in skin_color), -1)
    
    # Position iris in center
    iris_h, iris_w = iris_img.shape[:2]
    start_x = (size[0] - iris_w) // 2
    start_y = (size[1] - iris_h) // 2
    
    # Blend iris into eye context
    eye_img[start_y:start_y+iris_h, start_x:start_x+iris_w] = iris_img
    
    # Add eyelids
    # Upper eyelid
    pts = np.array([
        [start_x - 50, start_y + iris_h//3],
        [start_x + iris_w//2, start_y - 20],
        [start_x + iris_w + 50, start_y + iris_h//3],
        [start_x + iris_w, start_y + iris_h//2],
        [start_x, start_y + iris_h//2]
    ], np.int32)
    
    cv2.fillPoly(eye_img, [pts], (200, 150, 120))
    
    # Lower eyelid
    pts_lower = np.array([
        [start_x - 30, start_y + 2*iris_h//3],
        [start_x + iris_w//2, start_y + iris_h + 10],
        [start_x + iris_w + 30, start_y + 2*iris_h//3],
        [start_x + iris_w, start_y + iris_h//2],
        [start_x, start_y + iris_h//2]
    ], np.int32)
    
    cv2.fillPoly(eye_img, [pts_lower], (200, 150, 120))
    
    # Add eyelashes
    for i in range(20):
        # Upper lashes
        x = start_x + random.randint(-30, iris_w + 30)
        y = start_y + random.randint(-10, iris_h//3)
        length = random.randint(10, 25)
        angle = random.uniform(-0.5, 0.5)
        end_x = int(x + length * np.cos(angle - np.pi/2))
        end_y = int(y + length * np.sin(angle - np.pi/2))
        cv2.line(eye_img, (x, y), (end_x, end_y), (50, 30, 20), 2)
        
        # Lower lashes
        x = start_x + random.randint(-20, iris_w + 20)
        y = start_y + random.randint(2*iris_h//3, iris_h + 10)
        length = random.randint(5, 15)
        angle = random.uniform(-0.3, 0.3)
        end_x = int(x + length * np.cos(angle + np.pi/2))
        end_y = int(y + length * np.sin(angle + np.pi/2))
        cv2.line(eye_img, (x, y), (end_x, end_y), (50, 30, 20), 1)
    
    return eye_img

def create_sample_dataset():
    """Create a complete sample dataset with realistic iris images"""
    
    print("🎨 Creating realistic iris sample dataset...")
    
    # Create directories
    os.makedirs('testSamples', exist_ok=True)
    os.makedirs('sample_dataset', exist_ok=True)
    
    # Create samples for different people
    num_people = 20
    samples_per_person = 5
    
    for person_id in range(1, num_people + 1):
        print(f"   Creating samples for Person {person_id}...")
        
        person_dir = f'sample_dataset/person_{person_id:02d}'
        os.makedirs(person_dir, exist_ok=True)
        
        for sample_id in range(1, samples_per_person + 1):
            # Create iris with slight variations
            iris_img = create_realistic_iris(person_id=person_id)
            
            # Add some variation for different samples of same person
            if sample_id > 1:
                # Slight rotation
                angle = random.uniform(-5, 5)
                center = (iris_img.shape[1]//2, iris_img.shape[0]//2)
                rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                iris_img = cv2.warpAffine(iris_img, rotation_matrix, (iris_img.shape[1], iris_img.shape[0]))
                
                # Slight brightness variation
                brightness = random.uniform(0.8, 1.2)
                iris_img = np.clip(iris_img * brightness, 0, 255).astype(np.uint8)
            
            # Create full eye context
            eye_img = create_eye_context(iris_img)
            
            # Save images
            filename = f'{person_dir}/iris_{sample_id:02d}.jpg'
            cv2.imwrite(filename, eye_img)
            
            # Also save some in testSamples for easy testing
            if sample_id <= 2:
                test_filename = f'testSamples/person_{person_id:02d}_sample_{sample_id}.jpg'
                cv2.imwrite(test_filename, eye_img)
    
    print(f"✅ Created {num_people * samples_per_person} realistic iris images")
    print(f"   📁 Dataset: sample_dataset/ ({num_people} people)")
    print(f"   📁 Test samples: testSamples/ ({num_people * 2} images)")
    
    return True

if __name__ == "__main__":
    create_sample_dataset()
