# Lane Detection Using OpenCV

This repository contains a Python implementation of a lane detection algorithm using OpenCV. The script processes video frames to detect lane lines using edge detection, region masking, and Hough Line Transform.

## Features

- **Grayscale Conversion**: Converts frames to grayscale for better edge detection.
- **Gaussian Blur**: Smoothens the image to reduce noise.
- **Canny Edge Detection**: Detects edges to highlight lane boundaries.
- **Region of Interest Masking**: Focuses on the lower triangular area where lanes are typically located.
- **Hough Line Transform**: Detects and draws lane lines based on detected edges.
- **Video Processing**: Reads a video file and processes frames in real time.

## Prerequisites

To run the code, install the required dependencies:

```bash
pip install opencv-python numpyk

