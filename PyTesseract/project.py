"""
----------PAGE SEGMENTATION MODES----------
O Orientation and script detection (OSD) only
1 Automatic page segmentation with OSD. ‘
2 Automatic page segmentation, but no OSD, or OCR.
3 Fully automatic page segmentation, but no OSD. (Default)
4 Assume a single column of text of variable sizes.
5 Assume a single uniform block of vertically aligned text.
6 Assume a single uniform block of text
7 Treat the image as a single text line.
8 Treat the image as a single word.
9 Treat the image as a single word in a circle.
10 Treat the image as a single character.
11 Sparse text. Find as much text as possible in no particular order.
12 Sparse text with OSD.
13 Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract—specific.

----------OCR ENGINE MODES----------
0 Legacy engine only.
1 Neural nets LSTM engine only.
2 Legacy + LSTM engines.
3 Default, based on what is available.
"""

import pytesseract
from pytesseract import Output
import PIL.Image
import cv2

# Tesseract configuration
myconfig = r"--psm 11 --oem 3"

#image to text conversion simple
# text = pytesseract.image_to_string(PIL.Image.open(r"C:\Users\Saqib\OneDrive - Punjab Group of Colleges\UCP\Semester 4\Programing for Big Data (D12)\@Project\Images\text.jpg"), config=myconfig) # Use a raw string (prefixing the string literal with 'r') to avoid 'SyntaxError' caused by backslashes in file path. This ensures that backslashes are treated as literal characters and not as escape characters. You can also replace single backslashes with double backslashes to resolve the same error
# print(text)

# Read the image file
img = cv2.imread(r"C:\Users\Saqib\OneDrive - Punjab Group of Colleges\UCP\Semester 4\Programing for Big Data (D12)\@Project\Images\logos2.jpg")
if img is None:
    raise FileNotFoundError("The image file was not found.")
height, width, _ = img.shape

# # To Create boxes around indivisual character in the image 
# # Get bounding boxes of the text
# boxes = pytesseract.image_to_boxes(img, config=myconfig)
# # print(boxes)
# # Draw bounding boxes on the image
# for box in boxes.splitlines():
#     box = box.split(" ")
#     img = cv2.rectangle(img, ( (int(box[1])), height - int(box[2]) ), ( (int(box[3])), height - int(box[4]) ), (0, 255, 0), 2)
#     #Method-2 
#     # x1, y1, x2, y2 = int(box[1]), height - int(box[2]), int(box[3]), height - int(box[4])
#     # img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# To Create boxes around whole words in the image 
data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)
# print(data['text'])
amount_boxes = len(data['text'])
for i in range(amount_boxes):
    if float(data['conf'][i]) > 80:
            x, y, width, height = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            img = cv2.rectangle(img, (x, y), (x+width, y+height), (0, 255, 0), 2)
            img = cv2.putText(img, data['text'][i], (x, y+height+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            
# Display the image with bounding boxes
cv2.imshow("img", img)
cv2.waitKey(0)
print(img)

