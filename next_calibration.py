import numpy as np
import cv2
import json

filename = 'lagnus2.png'
image = cv2.imread('calibration_images/' + filename)
cv2.rectangle(image, (768, 396), (815, 411), (255, 0, 0), 1)
cv2.rectangle(image, (1094, 396), (1141, 411), (0, 0, 255), 1)

cv2.imshow('Preview', image)
cv2.waitKey(0)
