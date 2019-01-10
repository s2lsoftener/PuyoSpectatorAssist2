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


blue_next_BGR = []
red_next_BGR = []

# Initialize masks.
p1_next_mask = np.zeros((1080, 1920), np.uint8)
p2_next_mask = np.zeros((1080, 1920), np.uint8)

# Draw a white rectangle. The -1 means to fill inside the rectangle.
cv2.rectangle(p1_next_mask, (768, 396), (815, 411), (255, 255, 255), -1)
cv2.rectangle(p2_next_mask, (1094, 396), (1141, 411), (255, 255, 255), -1)

def nextAvgBGR(image_path, p1_color):
    global blue_next_BGR, red_next_BGR, p1_next_mask, p2_next_mask

    image = cv2.imread(image_path)

    if p1_color == 'B':
        blue_next_BGR.append(list(cv2.mean(image, mask=p1_next_mask)[:3]))
        red_next_BGR.append(list(cv2.mean(image, mask=p2_next_mask)[:3]))
    else:
        red_next_BGR.append(list(cv2.mean(image, mask=p1_next_mask)[:3]))
        blue_next_BGR.append(list(cv2.mean(image, mask=p2_next_mask)[:3]))
    
# Analyze images
nextAvgBGR('calibration_images/lagnus2.png', 'B')

image_list = ['calibration_images/lagnus.png',
              'calibration_images/lagnus2.png',
              'calibration_images/lagnus3.png']

for image in image_list: nextAvgBGR(image, 'B')

blue_next_avg_triplet = np.average(np.array(blue_next_BGR), axis=0)
blue_next_min_triplet = np.min(np.array(blue_next_BGR), axis=0)
blue_next_max_triplet = np.max(np.array(blue_next_BGR), axis=0)

red_next_avg_triplet = np.average(np.array(red_next_BGR), axis=0)
red_next_min_triplet = np.min(np.array(red_next_BGR), axis=0)
red_next_max_triplet = np.max(np.array(red_next_BGR), axis=0)


print(blue_next_avg_triplet)
print(blue_next_min_triplet)
print(blue_next_max_triplet)
print('\n\n')

print(red_next_avg_triplet)
print(red_next_min_triplet)
print(red_next_max_triplet)
print('\n\n')
