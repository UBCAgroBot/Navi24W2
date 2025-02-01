import cv2
import random
import numpy as np

height = 41
width = 51
size = 20

grid = np.ones((height, width))

directions = [(0, -2), (-2, 0), (2, 0), (0, 2)]

# 1 is wall 0 is free space
def generate_map(x, y):
    grid[y, x] = 0
    random.shuffle(directions)

    for x1, y1 in directions:
        x2, y2 = x + x1, y + y1
        if 0 <= x2 < width and 0 <= y2 < height and grid[y2, x2] == 1:
            grid[y2, x2] = 0
            grid[y + y1 // 2, x + x1 // 2] = 0
            generate_map(x2, y2)

generate_map(1, 1)

image = np.zeros((height * size, width * size))

for i in range(height):
    for j in range(width):
        if grid[i, j] == 0:
            cv2.rectangle(image, (j * size, i * size), ((j + 1) * size, (i + 1) * size), 255, -1) # color white for path

cv2.imshow("Map", image)
cv2.waitKey(0)
cv2.destroyAllWindows()