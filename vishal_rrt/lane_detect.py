import cv2
import numpy as np

def process_frame(frame):
    #grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    #canny edge detection
    edges = cv2.Canny(blur, 50, 150)
    
    #region of interest focusing on lower trigular region (typically where lanes are)
    height, width = edges.shape
    vertices = np.array([[(0, height), (width / 2, height / 2), (width, height)]], dtype=np.int32) #triangular shape
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, vertices, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    
    #hough line transform
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=100)
    
    #blank image to draw lines on
    line_image = np.zeros_like(frame)
    
    #draw the lines
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), color=[0, 255, 0], thickness=3)
        
    #combine line image with original frame
    result = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
    
    return result

def main():
    #loading video
    cap = cv2.VideoCapture('lanes_clip.mp4')
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_frame(frame)
        
        cv2.imshow('Lane Detection', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()