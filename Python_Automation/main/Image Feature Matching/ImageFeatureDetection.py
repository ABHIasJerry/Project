import cv2
import numpy as np
import os

print("OpenCV Version: ", cv2.__version__)  # works fine with 4.5.5
print("Numpy Version: ", np.__version__)  # works fine with 1.24.1

#define the screen resolution
screen_res = 1280, 720

# Path for ImagesLoad
Load_path = 'ImagesLoad'
images = []
classNames = []
desList = []
good_match = []
matchList = []
finalValue = -1
Images_bucket = os.listdir(Load_path)
Images_bucket_count = len(Images_bucket)
for classes in Images_bucket:
    imgCur = cv2.imread(f'{Load_path}/{classes}', 0)
    images.append(imgCur)
    classNames.append(os.path.splitext(classes)[0])
print('Images found in Images Bucket: -> ', classNames)

# ORB Algorithm
orb = cv2.ORB_create(nfeatures=1000)  # default match feature is 500


def findDescriptor(images):
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
        return desList


def findID(img, desList, threshold=15):
    kp2, des2 = orb.detectAndCompute(img, None)
    brute_force = cv2.BFMatcher()
    try:
        for des in desList:
            matches = brute_force.knnMatch(des, des2, k=2)
            for m, n in matches:
                if m.distance < 0.75 * n.distance:  # 75% match is acceptable
                    good_match.append([m])
                    return good_match
            matchList.append(len(good_match))
    except:
        pass
    print(len(matchList))  # Prints the match list array
    if len(matchList) != 0:
        if max(matchList) > threshold:
            finalValue = matchList.index(max(matchList))
            return finalValue


desList = findDescriptor(images)
print('Number of images found: ', len(desList))

# Initialize Webcam
capture = cv2.VideoCapture(0)

# Running in infinite for loop
while True:
    success, img2 = capture.read()
    imgOriginal = img2.copy()
    img2 = cv2.cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    scale_width = screen_res[0] / imgOriginal.shape[1]
    scale_height = screen_res[1] / imgOriginal.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(imgOriginal.shape[1] * scale)
    window_height = int(imgOriginal.shape[0] * scale)
    id = findID(img2, desList)
    if id != -1:
        cv2.putText(imgOriginal, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, 1, (0, 0, 255), 2)
    cv2.namedWindow('Image Analytics', cv2.WINDOW_NORMAL)  # makes window size re-sized
    cv2.resizeWindow('Image Analytics', window_width, window_height)
    cv2.imshow('Image Capture', imgOriginal)
    cv2.waitKey(1)
    print(" Capturing image feed...")
