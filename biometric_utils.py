
import cv2
import numpy as np

# Globals for stats
count = 0
miss = []

def enhance_iris_image(image):
    """Enhanced iris image preprocessing for maximum accuracy"""
    try:
        # Convert to float32 for better processing
        if image.dtype != np.float32:
            image = image.astype(np.float32)

        # Normalize if needed
        if image.max() > 1.0:
            image = image / 255.0

        # Convert to LAB color space for better contrast enhancement
        if len(image.shape) == 3:
            lab = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2LAB)

            # Apply CLAHE to L channel for better contrast
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])

            # Convert back to RGB
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB).astype(np.float32) / 255.0
        else:
            # For grayscale images
            enhanced = cv2.equalizeHist((image * 255).astype(np.uint8)).astype(np.float32) / 255.0
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)

        # Apply Gaussian blur to reduce noise
        enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)

        return enhanced

    except Exception as e:
        print(f"Error in iris enhancement: {e}")
        return image

def getIrisFeatures(image_source):
    """
    Enhanced iris feature extraction with improved circle detection.
    Accepts filename (str) or image array.
    """
    global count, miss

    try:
        if isinstance(image_source, str):
            img = cv2.imread(image_source, 0)
        else:
            # Assuming numpy array
            if len(image_source.shape) == 3:
                img = cv2.cvtColor(image_source, cv2.COLOR_BGR2GRAY)
            else:
                img = image_source
                
        if img is None:
            return None

        # Enhanced preprocessing
        img_blur = cv2.medianBlur(img, 5)
        img_blur = cv2.equalizeHist(img_blur)  # Improve contrast
        
        # Detect circles (iris/pupil) with improved parameters
        circles = cv2.HoughCircles(
            img_blur,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=int(img.shape[0]/8),
            param1=50,
            param2=30,
            minRadius=int(img.shape[0]/20),
            maxRadius=int(img.shape[0]/4)
        )

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            height, width = img.shape
            
            # Find the best circle (largest one, likely the iris)
            best_circle = None
            max_radius = 0

            for (x, y, r) in circles:
                if r > max_radius and x-r > 0 and y-r > 0 and x+r < width and y+r < height:
                    max_radius = r
                    best_circle = (x, y, r)

            if best_circle is not None:
                x, y, r = best_circle

                # Create mask for iris region
                mask = np.zeros((height, width), np.uint8)
                cv2.circle(mask, (x, y), r, 255, -1)

                # Extract iris region
                iris_region = cv2.bitwise_and(img, img, mask=mask)

                # Crop to bounding box
                crop_x = max(0, x - r)
                crop_y = max(0, y - r)
                crop_w = min(width - crop_x, 2 * r)
                crop_h = min(height - crop_y, 2 * r)

                cropped_iris = iris_region[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]

                # Resize to standard size
                if cropped_iris.size > 0:
                    cropped_iris = cv2.resize(cropped_iris, (128, 128))
                    
                    # Convert back to color for consistency with enhancement logic
                    cropped_iris_color = cv2.cvtColor(cropped_iris, cv2.COLOR_GRAY2BGR)
                    
                    # Apply enhancement
                    final_iris = enhance_iris_image(cropped_iris_color)
                    
                    return final_iris

        return None

    except Exception as e:
        print(f"Error in iris extraction: {e}")
        return None
