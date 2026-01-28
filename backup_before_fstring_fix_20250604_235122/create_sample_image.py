import numpy as np
import cv2

# Create a simple sample iris image for testing
def create_sample_iris():
    # Create a 300x300 image
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    
    # Draw outer circle (iris boundary)
    cv2.circle(img, (150, 150), 80, (100, 100, 100), -1)
    
    # Draw inner circle (pupil)
    cv2.circle(img, (150, 150), 30, (0, 0, 0), -1)
    
    # Add some texture lines
    for i in range(0, 360, 15):
        angle = np.radians(i)
        x1 = int(150 + 30 * np.cos(angle))
        y1 = int(150 + 30 * np.sin(angle))
        x2 = int(150 + 80 * np.cos(angle))
        y2 = int(150 + 80 * np.sin(angle))
        cv2.line(img, (x1, y1), (x2, y2), (150, 150, 150), 1)
    
    return img

# Create and save sample image
sample_img = create_sample_iris()
cv2.imwrite('testSamples/sample_iris.jpg', sample_img)
print("Sample iris image created: testSamples/sample_iris.jpg")
