# Ignore this file, this is just me reading some stuff out of a book

import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
# print('width: {} pixels'.format(image.shape[1]))
# print('height: {} pixels'.format(image.shape[0]))
# print('channels: {}'.format(image.shape[2]))

# Find regions
# Player 1 Board
cv2.rectangle(image, (279, 159), (663, 879), (255, 0, 0), 1)
# Player 2 Board
cv2.rectangle(image, (1256, 159), (1640, 879), (0, 0, 255), 1)

# cv2.imshow('Image', image)
# cv2.waitKey(0)

# Get average color of board unit?
image = cv2.imread(args['image'])
# Crop P1, row 1, col 1
# https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
crop_puyo = image[820:880, 279:343]
average = np.average(np.average(crop_puyo, axis=0), axis=0) # Outputs BGR

def cropPuyo(input_img, player_num, rowcoltuple):
    row = rowcoltuple[0]
    col = rowcoltuple[1]

    start_x, start_y = 0, 0

    if player_num == 1:
        start_x = 279
        start_y = 160
    elif player_num == 2:
        start_x = 1256
        start_y = 160

    x1 = start_x + 64 * (col - 1)
    x2 = start_x + 64 * (col)
    y1 = start_y + 60 * (12 - row)
    y2 = start_y + 60 * (12 - row + 1)

    return input_img[y1:y2, x1:x2]


# Compile averages
# List out row,col positions
blue_puyos = [(1, 1), (1, 2), (1, 3), (1, 5), (1, 6),
              (2, 4), (3, 2), (3, 3), (3, 5), (3, 6),
              (4, 3), (4, 6)]
blue_BGR_data = []
for pos in blue_puyos:
    row = pos[0]
    col = pos[1]
    puyo = cropPuyo(image, 1, (row, col))
    blue_BGR_data.append(np.average(np.average(puyo, axis=0), axis=0))
blue_avg_triplet = np.average(np.array(blue_BGR_data), axis=0)
blue_stdev_triplet = np.std(np.array(blue_BGR_data), axis=0)
print('Blue:')
print(blue_avg_triplet)
print(blue_stdev_triplet)
print('\n\n')

red_puyos = [(3, 1), (4, 1), (4, 2), (4, 4), (5, 3), (7, 1), (8, 1)]
red_BGR_data = []
for pos in red_puyos:
    row = pos[0]
    col = pos[1]
    puyo = cropPuyo(image, 1, (row, col))
    red_BGR_data.append(np.average(np.average(puyo, axis=0), axis=0))
red_avg_triplet = np.average(np.array(red_BGR_data), axis=0)
red_stdev_triplet = np.std(np.array(red_BGR_data), axis=0)
print('Red:')
print(red_avg_triplet)
print(red_stdev_triplet)
print('\n\n')

green_puyos = [(2, 1), (2, 2), (2, 3), (5, 6), (6, 4), (6, 5)]
green_BGR_data = []
for pos in green_puyos:
    row = pos[0]
    col = pos[1]
    puyo = cropPuyo(image, 1, (row, col))
    green_BGR_data.append(np.average(np.average(puyo, axis=0), axis=0))
green_avg_triplet = np.average(np.array(green_BGR_data), axis=0)
green_stdev_triplet = np.std(np.array(green_BGR_data), axis=0)
print('green:')
print(green_avg_triplet)
print(green_stdev_triplet)
print('\n\n')

purple_puyos = [(1, 4), (2, 5), (2, 6), (3, 4), (4, 5), (5, 1), (5, 2), (5, 4), (5, 5),
                (6, 1), (6, 3), (7, 4), (7, 5)]
purple_BGR_data = []
for pos in purple_puyos:
    row = pos[0]
    col = pos[1]
    puyo = cropPuyo(image, 1, (row, col))
    purple_BGR_data.append(np.average(np.average(puyo, axis=0), axis=0))
purple_avg_triplet = np.average(np.array(purple_BGR_data), axis=0)
purple_stdev_triplet = np.std(np.array(purple_BGR_data), axis=0)
print('purple:')
print(purple_avg_triplet)
print(purple_stdev_triplet)
print('\n\n')


# cv2.imshow('Single Puyo', crop_puyo)
# cv2.imwrite('blue_puyo.jpg', crop_puyo)
# cv2.waitKey(0)

cv2.imshow('blue_puyo', bluepuyo)
cv2.waitKey(0)