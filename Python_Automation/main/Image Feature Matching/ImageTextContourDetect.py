# -----------------------------------------------------------------------------------------------
# Marking all Contours
# import cv2
# image = cv2.imread('ImagesTrain/sample.jpg', 0)

# # Marking total number of contours
# ret, thresh = cv2.threshold(image, 127, 255, 0)
# contours, hierarchy = cv2.findContours(thresh, 1, 2)
# print("Number of contours:" + str(len(contours)))
# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)
#     img = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

# # Grading out readable area
# th, threshed = cv2.threshold(image, 100, 255, cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)
# cnts = cv2.findContours(cv2.morphologyEx(threshed, cv2.MORPH_OPEN, np.ones((2,2))), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
# nh, nw = image.shape[:2]
# for cnt in cnts:
#     x,y,w,h = bbox = cv2.boundingRect(cnt)
#     if h >= 0.3 * nh:
#         cv2.rectangle(image, (x,y), (x+w, y+h), (0, 0, 0), 10, cv2.LINE_AA)

# screen_res = 1280, 720
# scale_width = screen_res[0] / image.shape[1]
# scale_height = screen_res[1] / image.shape[0]
# scale = min(scale_width, scale_height)
# window_width = int(image.shape[1] * scale)
# window_height = int(image.shape[0] * scale)
#
# cv2.namedWindow('Image Contour', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Image Contour', window_width, window_height)
# cv2.imshow('Image Contour', image)
# cv2.waitKey(0)


# --------------------------------------------------------------------------------------- #
# ---Finding contours ---
import cv2

img = cv2.imread('ImagesTrain/sample.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

im2 = img.copy()
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
screen_res = 1280, 720
scale_width = screen_res[0] / im2.shape[1]
scale_height = screen_res[1] / im2.shape[0]
scale = min(scale_width, scale_height)
window_width = int(im2.shape[1] * scale)
window_height = int(im2.shape[0] * scale)
cv2.namedWindow('Image Contour', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image Contour', window_width, window_height)
cv2.imshow('Image Contour', im2)
cv2.waitKey(0)

# ------------------------------------------------------------------------------------------ #
