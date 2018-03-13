import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# Uncomment the next line for use in a Jupyter notebook
#%matplotlib inline
import numpy as np
from extra_functions import perspect_transform, color_thresh, rover_coords

# Define a function to convert from cartesian to polar coordinates
def to_polar_coords(xpix, ypix):
    # Calculate distance to each pixel
    dist = np.sqrt(xpix**2 + ypix**2)
    # Calculate angle using arctangent function
    angles = np.arctan2(ypix, xpix)
    return dist, angles

image = mpimg.imread('angle_example.jpg')
# Perform perspective transform
source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
# Define calibration box in source (actual) and destination (desired) coordinates
# These source and destination points are defined to warp the image
# to a grid where each 10x10 pixel square represents 1 square meter
dst_size = 5 
# Set a bottom offset to account for the fact that the bottom of the image 
# is not the position of the rover but a bit in front of it
bottom_offset = 6
destination = np.float32([[image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                  [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                  ])
warped = perspect_transform(image,source,destination) 
# Threshold the warped image
colorsel = color_thresh(warped, rgb_thresh=(160, 160, 160))
# Convert to rover-centric coords
xpix, ypix = rover_coords(colorsel)  
# Convert to polar coords
distances, angles = to_polar_coords(xpix, ypix) 
# Compute the average angle of all polar angles !!!!!!!!!!!
avg_angle = np.mean(angles) 

# Do some plotting
fig = plt.figure(figsize=(12,9))
plt.subplot(221)
plt.imshow(image)
plt.gca().set_title('ORIGINAL', fontsize=16)
plt.subplot(222)
plt.imshow(warped)
plt.gca().set_title('WARPED', fontsize=16)
plt.subplot(223)
plt.imshow(colorsel, cmap='gray')
plt.gca().set_title('THRESHOLDED', fontsize=16)
plt.subplot(224)
plt.plot(xpix, ypix, '.')
plt.gca().set_title('STEER ANGLE (IN ROVER COORDS)', fontsize=16)
plt.ylim(-160, 160)
plt.xlim(0, 160)
arrow_length = 100
x_arrow = arrow_length * np.cos(avg_angle)
y_arrow = arrow_length * np.sin(avg_angle)
plt.arrow(0, 0, x_arrow, y_arrow, color='red', zorder=2, head_width=10, width=2)
plt.show()

# Clip values to -15/+15deg
avg_angle_degrees = avg_angle * 180/np.pi
steering = np.clip(avg_angle_degrees, -15, 15)