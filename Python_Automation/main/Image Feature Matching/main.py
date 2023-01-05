
# ------------------------------------------ Feature Testing with 2 images -------------------------- #
import cv2
import numpy as np
import os
print("OpenCV Version: ", cv2.__version__)  # works fine with 4.5.5
print("Numpy Version: ", np.__version__)  # works fine with 1.24.1


# Add 0 to import in grey scale
img1 = cv2.imread('ImagesLoad/abc.png', 0)
img2 = cv2.imread('ImagesTrain/sample.jpg', 0)

#define the screen resolution
screen_res = 1280, 720

# IMG 1
scale_width = screen_res[0] / img1.shape[1]
scale_height = screen_res[1] / img1.shape[0]
scale = min(scale_width, scale_height)
#resized window width and height
window_width = int(img1.shape[1] * scale)
window_height = int(img1.shape[0] * scale)

# IMG 2
scale_width_1 = screen_res[0] / img2.shape[1]
scale_height_1 = screen_res[1] / img2.shape[0]
scale = min(scale_width, scale_height)
#resized window width and height
window_width_1 = int(img2.shape[1] * scale)
window_height_1 = int(img2.shape[0] * scale)

# To compute using ORB algorithm
orb = cv2.ORB_create(nfeatures=1000)  # default match feature is 500

# Obtain Key-points and descriptions [Method 1]
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# To print the description values and shape
# print(des1.shape) # To print the shape value. Eg: 500, 32
# print(des1[0])  # To print the array value. Eg: [123, 100, ...] upto 32 numbers
# print(des2.shape)
# print(des2[0])

# Brute Force Match Algorithm [Method 1 - detailed]
brute_force = cv2.BFMatcher()
matches = brute_force.knnMatch(des1, des2, k=2)
good_match = []
for m, n in matches:
    if m.distance < 0.75*n.distance:   # 75% match is acceptable
        good_match.append([m])
print('Good matches count: ', len(good_match))  # Good matches value
if len(good_match) > 50:
    print('Match is acceptable')
elif len(good_match) > 90:
    print('Match is great')
else:
    print('Match is poor')
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good_match, None, flags=2)
# IMG 3
scale_width_2 = screen_res[0] / img3.shape[1]
scale_height_2 = screen_res[1] / img3.shape[0]
scale = min(scale_width, scale_height)
#resized window width and height
window_width_2 = int(img3.shape[1] * scale)
window_height_2 = int(img3.shape[0] * scale)

# To plot the key-points that match in both images [Method 2 -simple]
# imgkp1 = cv2.drawKeypoints(img1, kp1, None)
# imgkp2 = cv2.drawKeypoints(img2, kp2, None)

# Display images
# cv2.imshow('kp1', imgkp1)  # To show the key match points
# cv2.imshow('kp2', imgkp2)

# Show Image 1
# cv2.namedWindow('IMAGE 1', cv2.WINDOW_NORMAL)  # makes window size re-sized
# cv2.resizeWindow('IMAGE 1', window_width, window_height)
# cv2.imshow('IMAGE 1', img1)  # To show normal images

# Show Image 1
# cv2.namedWindow('IMAGE 2', cv2.WINDOW_NORMAL)  # makes window size re-sized
# cv2.resizeWindow('IMAGE 2', window_width_1, window_height_1)
# cv2.imshow('IMAGE 1', img2)

# Show Analytical Image
cv2.namedWindow('Image Analytics', cv2.WINDOW_NORMAL)  # makes window size re-sized
cv2.resizeWindow('Image Analytics', window_width_2, window_height_2)
cv2.imshow('Image Analytics', img3)  # To show comparison images with good match plots

cv2.waitKey(0)
print('Opened Images for you.')
