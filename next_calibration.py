import numpy as np
import cv2
import json

filename = 'lagnus2.png'
image = cv2.imread('calibration_images/' + filename)
cv2.rectangle(image, (774, 356), (809, 371), (255, 0, 0), 1)
cv2.rectangle(image, (1100, 356), (1135, 371), (0, 0, 255), 1)

cv2.rectangle(image, (774, 306), (809, 321), (255, 0, 0), 1)
cv2.rectangle(image, (1100, 306), (1135, 321), (0, 0, 255), 1)

cv2.rectangle(image, (734, 256), (769, 271), (255, 0, 0), 1)
cv2.rectangle(image, (1150, 256), (1185, 271), (0, 0, 255), 1)

cv2.rectangle(image, (734, 176), (769, 191), (255, 0, 0), 1)
cv2.rectangle(image, (1150, 176), (1185, 191), (0, 0, 255), 1)

cv2.imshow('Preview', image)
cv2.waitKey(0)
