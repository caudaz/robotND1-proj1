import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from extra_functions_04 import perspect_transform, color_thresh, source, destination

# Read in the sample image
image = mpimg.imread('sample.jpg')


# Define a function to convert from image coords to rover coords
def rover_coords(binary_img):
    # Identify nonzero pixels
    # 2 vectors
    ypos, xpos = binary_img.nonzero()
    print(ypos,xpos)
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.
    # 2 vectors (after coord transform)
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)
    return x_pixel, y_pixel

# Perform warping and color thresholding
warped = perspect_transform(image, source, destination)
colorsel = color_thresh(warped, rgb_thresh=(160, 160, 160))
# Extract x and y positions of navigable terrain pixels
# and convert to rover coordinates
xpix, ypix = rover_coords(colorsel)
print(xpix,ypix)

# Plot BEFORE-Original
fig = plt.figure(figsize=(7.5,5))
plt.imshow(image)
plt.ylim(160,0)
plt.xlim(0, 320)
plt.title('BEFORE-Original', fontsize=20)
# Plot BEFORE-Warped
fig = plt.figure(figsize=(7.5,5))
plt.imshow(warped)
plt.ylim(160,0)
plt.xlim(0, 320)
plt.title('BEFORE-Warped', fontsize=20)
# Plot BEFORE-ColorThreshold
fig = plt.figure(figsize=(7.5,5))
plt.imshow(colorsel)
plt.imshow(colorsel, cmap='gray')
plt.ylim(160,0)
plt.xlim(0, 320)
plt.title('BEFORE-ColorThreshold', fontsize=20)
# Plot AFTER the map in rover-centric coords
fig = plt.figure(figsize=(5, 7.5))
plt.plot(xpix, ypix, '.')
plt.ylim(-160, 160)
plt.xlim(0, 160)
plt.title('AFTER Rover-Centric Map', fontsize=20)
#plt.show() # Uncomment if running on your local machine