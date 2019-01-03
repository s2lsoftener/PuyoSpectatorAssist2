import numpy as np
import cv2

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

def collectAvgBGR(image, positions, player, target_list):
    for pos in positions:
        row = pos[0]
        col = pos[1]
        puyo = cropPuyo(image, player, (row, col))
        avg_data = np.average(np.average(puyo, axis=0), axis=0)
        target_list.append(avg_data)

red_BGR_data = []
green_BGR_data = []
blue_BGR_data = []
yellow_BGR_data = []
purple_BGR_data = []
ojama_BGR_data = []

# Rulue, blue, red, green, purple
image = cv2.imread('calibration_images/test.png')
blue_puyos = [(1, 1), (1, 2), (1, 3), (1, 5), (1, 6),
              (2, 4), (3, 2), (3, 3), (3, 5), (3, 6),
              (4, 3), (4, 6)]
collectAvgBGR(image, blue_puyos, 1, blue_BGR_data)
blue_puyos = [(1, 1), (1, 2), (1, 4), (2, 3), (3, 2), (3, 4), (3, 5),
              (4, 4), (5, 2), (6, 1), (6, 2), (6, 5)]
collectAvgBGR(image, blue_puyos, 2, blue_BGR_data)

red_puyos = [(3, 1), (4, 1), (4, 2), (4, 4), (5, 3), (7, 1), (8, 1)]
collectAvgBGR(image, red_puyos, 1, red_BGR_data)
red_puyos = [(2, 1), (2, 2), (2, 5), (2, 6), (4, 5), (5, 1), (5, 5)]
collectAvgBGR(image, red_puyos, 2, red_BGR_data)

green_puyos = [(2, 1), (2, 2), (2, 3), (5, 6), (6, 4), (6, 5)]
collectAvgBGR(image, green_puyos, 1, green_BGR_data)
green_puyos = [(1, 3), (2, 4), (3, 3), (4, 3)]
collectAvgBGR(image, green_puyos, 2, green_BGR_data)

purple_puyos = [(1, 4), (2, 5), (2, 6), (3, 4), (4, 5), (5, 1), (5, 2), (5, 4), (5, 5),
                (6, 1), (6, 3), (7, 4), (7, 5)]
collectAvgBGR(image, purple_puyos, 1, purple_BGR_data)
purple_puyos = [(1, 5), (1, 6), (3, 1), (3, 6), (4, 1), (4, 2), (5, 4), (6, 4), (8, 2)]
collectAvgBGR(image, purple_puyos, 2, purple_BGR_data)

ojama_puyos = [(4, 6), (5, 3), (7, 1), (7, 2), (7, 5)]
collectAvgBGR(image, ojama_puyos, 2, ojama_BGR_data)


image = cv2.imread('calibration_images/rulue_yellow.png')
yellow_puyos = [(1, 4), (2, 4), (3, 3), (4, 3), (4, 6), (5, 6), (6, 4), (6, 6), (7, 5), (8, 4)]
collectAvgBGR(image, yellow_puyos, 1, yellow_BGR_data)
yellow_puyos = [(1, 5), (4, 1), (4, 6), (5, 2), (5, 6), (6, 2), (6, 6), (7, 4), (8, 1)]
collectAvgBGR(image, yellow_puyos, 2, yellow_BGR_data)


image = cv2.imread('calibration_images/amitie_witch.png')
red_puyos = [(1, 3), (2, 2), (2, 3), (3, 4), (4, 3)]
collectAvgBGR(image, red_puyos, 1, red_BGR_data)
red_puyos = [(1, 3), (2, 1), (2, 4), (2, 5), (3, 1), (3, 2), (3, 5),
             (5, 2), (5, 3), (5, 4), (6, 5), (8, 4), (9, 2), (9, 5),
             (10, 2), (11, 2)]
collectAvgBGR(image, red_puyos, 2, red_BGR_data)

blue_puyos = [(3, 1), (3, 3), (3, 6), (4, 1), (4, 2), (4, 6),
              (5, 6), (7, 6), (8, 6)]
collectAvgBGR(image, blue_puyos, 1, blue_BGR_data)
blue_puyos = [(2, 6), (3, 6), (4, 3), (4, 6), (6, 3), (6, 4), (7, 3), (7, 6),
              (8, 1), (8, 2), (8, 6), (9, 1), (9, 3), (9, 6), (11, 1), (11, 6),
              (12, 1), (12, 2)]
collectAvgBGR(image, blue_puyos, 2, blue_BGR_data)

yellow_puyos = [(1, 4), (1, 5), (2, 4), (3, 5), (4, 5), (5, 6)]
collectAvgBGR(image, yellow_puyos, 1, yellow_BGR_data)
yellow_puyos = [(1, 4), (1, 5), (1, 6), (2, 2), (3, 4), (4, 1), (4, 4), (4, 5),
                (5, 1), (6, 1), (10, 1), (10, 5), (10, 6)]
collectAvgBGR(image, yellow_puyos, 2, yellow_BGR_data)

purple_puyos = [(1, 1), (1, 2), (1, 6), (2, 1), (2, 5), (2, 6), (3, 2),
                (6, 1), (9, 6)]
collectAvgBGR(image, purple_puyos, 1, purple_BGR_data)
purple_puyos = [(1, 1), (1, 2), (2, 3), (3, 3), (5, 5), (5, 6), (6, 2), (6, 6),
                (7, 1), (7, 2), (7, 5), (8, 5), (9, 4), (10, 3)]
collectAvgBGR(image, purple_puyos, 2, purple_BGR_data)

ojama_puyos = [(4, 2), (7, 4), (8, 3), (11, 3)]
collectAvgBGR(image, ojama_puyos, 2, ojama_BGR_data)


image = cv2.imread('calibration_images/amitie_witch_green.png')
green_puyos = [(5, 5), (6, 6), (7, 4), (8, 5), (10, 5), (10, 6)]
collectAvgBGR(image, green_puyos, 1, green_BGR_data)
green_puyos = [(3, 1), (4, 2), (5, 4), (6, 2), (7, 1), (7, 2), (8, 5), (9, 3), (9, 5), (9, 6),
               (11, 4), (11, 5), (11, 6)]
collectAvgBGR(image, green_puyos, 2, green_BGR_data)

ojama_puyos = [(1, 1), (1, 3), (2, 1), (2, 3), (2, 5), (3, 2), (3, 4), (3, 5), (3, 6),
               (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (5, 2), (5, 4), (5, 6), (6, 1),
               (6, 2), (7, 1), (7, 5), (8, 1), (8, 2), (8, 3), (9, 1)]
collectAvgBGR(image, ojama_puyos, 1, ojama_BGR_data)
ojama_puyos = [(1, 3), (1, 4), (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (3, 5), (3, 6),
               (4, 3), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (8, 1), (9, 1), (10, 1), (10, 2),
               (11, 1), (12, 1)]
collectAvgBGR(image, ojama_puyos, 2, ojama_BGR_data)





red_avg_triplet = np.average(np.array(red_BGR_data), axis=0)
red_min_triplet = np.min(np.array(red_BGR_data), axis=0)
red_max_triplet = np.max(np.array(red_BGR_data), axis=0)
print('Red:')
print(red_avg_triplet)
print(red_min_triplet)
print(red_max_triplet)
print('\n\n')

green_avg_triplet = np.average(np.array(green_BGR_data), axis=0)
green_min_triplet = np.min(np.array(green_BGR_data), axis=0)
green_max_triplet = np.max(np.array(green_BGR_data), axis=0)
print('green:')
print(green_avg_triplet)
print(green_min_triplet)
print(green_max_triplet)
print('\n\n')

blue_avg_triplet = np.average(np.array(blue_BGR_data), axis=0)
blue_min_triplet = np.min(np.array(blue_BGR_data), axis=0)
blue_max_triplet = np.max(np.array(blue_BGR_data), axis=0)
print('blue:')
print(blue_avg_triplet)
print(blue_min_triplet)
print(blue_max_triplet)
print('\n\n')

yellow_avg_triplet = np.average(np.array(yellow_BGR_data), axis=0)
yellow_min_triplet = np.min(np.array(yellow_BGR_data), axis=0)
yellow_max_triplet = np.max(np.array(yellow_BGR_data), axis=0)
print('yellow:')
print(yellow_avg_triplet)
print(yellow_min_triplet)
print(yellow_max_triplet)
print('\n\n')

purple_avg_triplet = np.average(np.array(purple_BGR_data), axis=0)
purple_min_triplet = np.min(np.array(purple_BGR_data), axis=0)
purple_max_triplet = np.max(np.array(purple_BGR_data), axis=0)
print('purple:')
print(purple_avg_triplet)
print(purple_min_triplet)
print(purple_max_triplet)
print('\n\n')

ojama_avg_triplet = np.average(np.array(ojama_BGR_data), axis=0)
ojama_min_triplet = np.min(np.array(ojama_BGR_data), axis=0)
ojama_max_triplet = np.max(np.array(ojama_BGR_data), axis=0)
print('ojama:')
print(ojama_avg_triplet)
print(ojama_min_triplet)
print(ojama_max_triplet)
print('\n\n')
