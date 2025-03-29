import numpy as np
import cv2
import os
from pathlib import Path

def detect_edges(img):
    """
    Finds edges in green (crops) areas of an image.
    """
    # Convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    
    # Create green mask
    green_low = np.array([35, 40, 40])   
    green_high = np.array([90, 255, 255]) 
    green_mask = cv2.inRange(hsv, green_low, green_high)
    
    # Isolating just the green part of the image
    green_segment = cv2.bitwise_and(img, img, mask=green_mask)
    
    # Edge detection
    # Convert to grayscale for edge detection
    gray = cv2.cvtColor(green_segment, cv2.COLOR_RGB2GRAY)
    
    # Detecting edges using Sobel edge detection
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    edges = np.sqrt(sobelx**2 + sobely**2)
    edges = np.uint8(255 * edges / np.max(edges)) #scale to 0-255
    
    # convert to rgb (3 channel image)
    rgb_edge = np.stack([edges] * 3, axis=-1)
    
    return rgb_edge

def process_images(input_dir, output_dir):
    """
    Takes input folder with test images, processes them and outputs them
    into a output folder
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # loops through every image
    for img_file in input_path.glob("*.jpg"):
        image = cv2.imread(str(img_file))
        if image is None:
            continue
        
        # Converts image to rgb then processes it
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output = detect_edges(rgb_img)
        
        # writes the same filename for the output file
        output_file = output_path / img_file.name
        cv2.imwrite(str(output_file), cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

def main():
    process_images("Crops", "Processed_Images")

if __name__ == "__main__":
    main()