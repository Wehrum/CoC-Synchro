import cv2
import numpy as np

# Load the image
img = cv2.imread('screenshots/screenshot.png')

# Convert the image to the HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define the range of white color in HSV
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])

# Define the range of additional color in RGB
lower_color = np.array([96, 95, 82])
upper_color = np.array([160, 214, 218])

# Convert the additional color range to HSV
hsv_lower_color = cv2.cvtColor(np.array([[lower_color]], dtype=np.uint8), cv2.COLOR_RGB2HSV)[0][0]
hsv_upper_color = cv2.cvtColor(np.array([[upper_color]], dtype=np.uint8), cv2.COLOR_RGB2HSV)[0][0]

# Create masks using color ranges
mask_white = cv2.inRange(hsv, lower_white, upper_white)
mask_color = cv2.inRange(hsv, hsv_lower_color, hsv_upper_color)

# Combine the masks
mask_combined = cv2.bitwise_or(mask_white, mask_color)

# Apply the mask to the original image to extract colors
result = cv2.bitwise_and(img, img, mask=mask_combined)

# Output extracted image as a new file
cv2.imwrite("result.png", result)
