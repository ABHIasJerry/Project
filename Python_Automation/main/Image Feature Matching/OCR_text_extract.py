import cv2
import pytesseract
from pytesseract import Output
my_config = r"--psm 11 --oem 3"
img = cv2.imread('ImagesTrain/sample.jpg')
height, width, _ = img.shape
data = pytesseract.image_to_boxes(img, config=my_config, output_type=Output.DICT)
print(data['text'])

# To create boxes around text in images
# boxes = pytesseract.image_to_boxes(img, config=my_config)
# for box in boxes.splitlines():
#     box = box.split(" ")
#     img = cv2.rectangle(img, (int(box[1]), height - int(box[2])), (int(box[3]), height - int(box[4])), (0, 255, 0), 2)
#
# cv2.imshow("img", img)
# cv2.waitKey(0)

amount_boxes = len(data['text'])
for i in range(amount_boxes):
    if float(data['conf'][i]) > 20:  # 20 -> lower the value for more capture. vary accordingly
        (x, y, width, height) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        img = cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)
        img = cv2.putText(img, data['text'][i], (x, y + height + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("img", img)
    cv2.waitKey(0)

