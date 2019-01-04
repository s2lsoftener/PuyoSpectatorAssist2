import numpy as np
import cv2
import shutil
import os
import json

if os.path.isdir('calibration_images/confirmation/'):
    shutil.rmtree('calibration_images/confirmation/')
os.mkdir('calibration_images/confirmation/')
os.mkdir('calibration_images/confirmation/red/')
os.mkdir('calibration_images/confirmation/green/')
os.mkdir('calibration_images/confirmation/blue/')
os.mkdir('calibration_images/confirmation/yellow/')
os.mkdir('calibration_images/confirmation/purple/')
os.mkdir('calibration_images/confirmation/ojama/')

def cropPuyo(input_img, player_num, rowcoltuple):
    row = rowcoltuple[0]
    col = rowcoltuple[1]

    start_x, start_y = 0, 0

    if player_num == 1:
        start_x = 279
        start_y = 159
    elif player_num == 2:
        start_x = 1256
        start_y = 159

    x1 = start_x + 64 * (col - 1)
    x2 = start_x + 64 * (col)
    y1 = start_y + 60 * (12 - row)
    y2 = start_y + 60 * (12 - row + 1)

    return input_img[y1:y2, x1:x2]

def collectAvgBGR(image, positions, player, target_list, color, filename):
    index = 0
    for pos in positions:
        row, col = pos

        # Crop the Puyo
        puyo = cropPuyo(image, player, (row, col))

        # Create a circular mask to focus more on the puyo instead of the char bg
        height, width = puyo.shape[0], puyo.shape[1]
        circle_mask = np.zeros((height, width), np.uint8)
        cv2.circle(circle_mask, (width // 2, height // 2), height // 2, (255, 255, 255), -1)
        # center_x = int(width / 2)
        # center_y = int(height * 0.75)
        # ellipse_width = int(width * 0.4)
        # ellipse_height = int(height * 0.1)

        # cv2.ellipse(ellipse_mask, (center_x, center_y), (ellipse_width, ellipse_height), 0, 0, 360, (255, 255, 255), -1)

        # Get avg RGB of the circular region (circular_mask) in the puyo img
        avg_data = cv2.mean(puyo, mask=circle_mask)[:3]
        avg_data = list(avg_data)
        target_list.append(avg_data)

        # Save the cropped puyo file to make sure they were sorted correctly
        puyo_circle = cv2.bitwise_and(puyo, puyo, mask=circle_mask)
        print('calibration_images/confirmation/' + color + '/' + str(index) + '_p' + str(player) + '_' + filename)
        print(avg_data)
        cv2.imwrite('calibration_images/confirmation/' + color + '/' + str(index) + '_p' + str(player) + '_' + filename, puyo_circle)
        index += 1

red_BGR_data = []
green_BGR_data = []
blue_BGR_data = []
yellow_BGR_data = []
purple_BGR_data = []
ojama_BGR_data = []

# Rulue, blue, red, green, purple
filename = 'test.png'
image = cv2.imread('calibration_images/' + filename)
blue_puyos = [(1, 1), (1, 2), (1, 3), (1, 5), (1, 6),
              (2, 4), (3, 2), (3, 3), (3, 5), (3, 6),
              (4, 3), (4, 6)]
collectAvgBGR(image, blue_puyos, 1, blue_BGR_data, 'blue', filename)
blue_puyos = [(1, 1), (1, 2), (1, 4), (2, 3), (3, 2), (3, 4), (3, 5),
              (4, 4), (5, 2), (6, 1), (6, 2), (6, 5)]
collectAvgBGR(image, blue_puyos, 2, blue_BGR_data, 'blue', filename)

red_puyos = [(3, 1), (4, 1), (4, 2), (4, 4), (5, 3), (7, 1), (8, 1)]
collectAvgBGR(image, red_puyos, 1, red_BGR_data, 'red', filename)
red_puyos = [(2, 1), (2, 2), (2, 5), (2, 6), (4, 5), (5, 1), (5, 5)]
collectAvgBGR(image, red_puyos, 2, red_BGR_data, 'red', filename)

green_puyos = [(2, 1), (2, 2), (2, 3), (5, 6), (6, 4), (6, 5)]
collectAvgBGR(image, green_puyos, 1, green_BGR_data, 'green', filename)
green_puyos = [(1, 3), (2, 4), (3, 3), (4, 3)]
collectAvgBGR(image, green_puyos, 2, green_BGR_data, 'green', filename)

purple_puyos = [(1, 4), (2, 5), (2, 6), (3, 4), (4, 5), (5, 1), (5, 2), (5, 4), (5, 5),
                (6, 1), (6, 3), (7, 4), (7, 5)]
collectAvgBGR(image, purple_puyos, 1, purple_BGR_data, 'purple', filename)
purple_puyos = [(1, 5), (1, 6), (3, 1), (3, 6), (4, 1), (4, 2), (5, 4), (6, 4), (8, 2)]
collectAvgBGR(image, purple_puyos, 2, purple_BGR_data, 'purple', filename)

ojama_puyos = [(4, 6), (5, 3), (7, 1), (7, 2), (7, 5)]
collectAvgBGR(image, ojama_puyos, 2, ojama_BGR_data, 'ojama', filename)


filename = 'rulue_yellow.png'
image = cv2.imread('calibration_images/' + filename)
yellow_puyos = [(1, 4), (2, 4), (3, 3), (4, 3), (4, 6), (5, 6), (6, 4), (6, 6), (7, 5), (8, 4)]
collectAvgBGR(image, yellow_puyos, 1, yellow_BGR_data, 'yellow', filename)
yellow_puyos = [(1, 5), (4, 1), (4, 6), (5, 2), (5, 6), (6, 2), (6, 6), (7, 4), (8, 1)]
collectAvgBGR(image, yellow_puyos, 2, yellow_BGR_data, 'yellow', filename)


filename = 'amitie_witch.png'
image = cv2.imread('calibration_images/' + filename)
red_puyos = [(1, 3), (2, 2), (2, 3), (3, 4), (4, 3)]
collectAvgBGR(image, red_puyos, 1, red_BGR_data, 'red', filename)
red_puyos = [(1, 3), (2, 1), (2, 4), (2, 5), (3, 1), (3, 2), (3, 5),
             (5, 2), (5, 3), (5, 4), (6, 5), (8, 4), (9, 2), (9, 5),
             (10, 2), (11, 2)]
collectAvgBGR(image, red_puyos, 2, red_BGR_data, 'red', filename)

blue_puyos = [(3, 1), (3, 3), (3, 6), (4, 1), (4, 2), (4, 6),
              (5, 6), (7, 6), (8, 6)]
collectAvgBGR(image, blue_puyos, 1, blue_BGR_data, 'blue', filename)
blue_puyos = [(2, 6), (3, 6), (4, 3), (4, 6), (6, 3), (6, 4), (7, 3), (7, 6),
              (8, 1), (8, 2), (8, 6), (9, 1), (9, 3), (9, 6), (11, 1), (11, 6),
              (12, 1), (12, 2)]
collectAvgBGR(image, blue_puyos, 2, blue_BGR_data, 'blue', filename)

yellow_puyos = [(1, 4), (1, 5), (2, 4), (3, 5), (4, 5), (6, 6)]
collectAvgBGR(image, yellow_puyos, 1, yellow_BGR_data, 'yellow', filename)
yellow_puyos = [(1, 4), (1, 5), (1, 6), (2, 2), (3, 4), (4, 1), (4, 4), (4, 5),
                (5, 1), (6, 1), (10, 1), (10, 5), (10, 6)]
collectAvgBGR(image, yellow_puyos, 2, yellow_BGR_data, 'yellow', filename)

purple_puyos = [(1, 1), (1, 2), (1, 6), (2, 1), (2, 5), (2, 6), (3, 2),
                (6, 1), (9, 6)]
collectAvgBGR(image, purple_puyos, 1, purple_BGR_data, 'purple', filename)
purple_puyos = [(1, 1), (1, 2), (2, 3), (3, 3), (5, 5), (5, 6), (6, 2), (6, 6),
                (7, 1), (7, 2), (7, 5), (8, 5), (9, 4), (10, 3)]
collectAvgBGR(image, purple_puyos, 2, purple_BGR_data, 'purple', filename)

ojama_puyos = [(4, 2), (7, 4), (8, 3), (11, 3)]
collectAvgBGR(image, ojama_puyos, 2, ojama_BGR_data, 'ojama', filename)


filename = 'amitie_witch_green.png'
image = cv2.imread('calibration_images/' + filename)
green_puyos = [(5, 5), (6, 6), (7, 4), (8, 5), (10, 5), (10, 6)]
collectAvgBGR(image, green_puyos, 1, green_BGR_data, 'green', filename)
green_puyos = [(3, 1), (4, 2), (5, 4), (6, 2), (7, 1), (7, 2), (8, 5), (9, 3), (9, 5), (9, 6),
               (11, 4), (11, 5), (11, 6)]
collectAvgBGR(image, green_puyos, 2, green_BGR_data, 'green', filename)

ojama_puyos = [(1, 1), (1, 3), (2, 1), (2, 3), (2, 5), (3, 2), (3, 4), (3, 5), (3, 6),
               (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (5, 2), (5, 4), (5, 6), (6, 1),
               (6, 2), (7, 1), (7, 5), (8, 1), (8, 2), (8, 3), (9, 1)]
collectAvgBGR(image, ojama_puyos, 1, ojama_BGR_data, 'ojama', filename)
ojama_puyos = [(1, 3), (1, 4), (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (3, 5), (3, 6),
               (4, 3), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (8, 1), (9, 1), (10, 1), (10, 2),
               (11, 1), (12, 1)]
collectAvgBGR(image, ojama_puyos, 2, ojama_BGR_data, 'ojama', filename)


filename = 'hartman_penglai.png'
image = cv2.imread('calibration_images/' + filename)
red_puyos = [(1, 4), (3, 4), (3, 5), (4, 2), (4, 4), (9, 2), (10, 1), (11, 1), (11, 2)]
collectAvgBGR(image, red_puyos, 1, red_BGR_data, 'red', filename)
red_puyos = [(1, 5), (2, 5), (2, 6), (3, 4), (4, 3), (4, 4), (7, 3), (7, 4), (7, 5), (7, 6),
             (8, 4), (8, 5), (11, 4)]
collectAvgBGR(image, red_puyos, 2, red_BGR_data, 'red', filename)

green_puyos = [(1, 5), (2, 1), (2, 2), (2, 5), (3, 1), (3, 6), (4, 5), (5, 3), (5, 4), (6, 6),
               (7, 2), (7, 3), (8, 3), (9, 4)]
collectAvgBGR(image, green_puyos, 1, green_BGR_data, 'green', filename)
green_puyos = [(1, 6), (2, 1), (2, 2), (3, 1), (3, 5), (3, 6), (4, 6), (5, 1), (5, 3),
               (6, 2), (6, 4), (6, 5), (6, 6), (8, 3), (8, 6)]
collectAvgBGR(image, green_puyos, 2, green_BGR_data, 'green', filename)

blue_puyos = [(1, 1), (1, 2), (2, 3), (3, 2), (5, 2), (5, 5), (6, 2), (7, 1), (8, 2), (8, 4), (8, 5)]
collectAvgBGR(image, blue_puyos, 1, blue_BGR_data, 'blue', filename)
blue_puyos = [(1, 1), (1, 2), (2, 3), (3, 2), (4, 5), (9, 3), (9, 4), (10, 4)]
collectAvgBGR(image, blue_puyos, 2, blue_BGR_data, 'blue', filename)

yellow_puyos = [(1, 3), (1, 6), (2, 4), (2, 6), (3, 3), (4, 1), (4, 3), (4, 6), (5, 1), (5, 6), (6, 1),
                (7, 4), (7, 5), (8, 1), (9, 1)]
collectAvgBGR(image, yellow_puyos, 1, yellow_BGR_data, 'yellow', filename)
yellow_puyos = [(1, 3), (1, 4), (2, 4), (3, 3), (4, 1), (4, 2), (5, 2), (5, 4), (5, 5), (5, 6), (6, 1),
                (6, 3), (7, 1), (7, 2), (9, 6), (10, 3), (11, 3)]
collectAvgBGR(image, yellow_puyos, 2, yellow_BGR_data, 'yellow', filename)

# ojama_puyos = [(6, 3), (6, 4), (6, 5), (10, 2), (12, 1)]
# collectAvgBGR(image, ojama_puyos, 1, ojama_BGR_data, 'ojama', filename)


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

# Pad the upper and lower limits, just in case
mins = [red_min_triplet, green_min_triplet, blue_min_triplet, yellow_min_triplet, purple_min_triplet,
        ojama_min_triplet]
for m in mins: m -= 10

maxs = [red_max_triplet, green_max_triplet, blue_max_triplet, yellow_max_triplet, purple_max_triplet,
        ojama_max_triplet]
for m in maxs: m += 10

# Save to JSON file
json_data = {
    'red': {
        'lower': red_min_triplet.tolist(),
        'upper': red_max_triplet.tolist()
    },
    'green': {
        'lower': green_min_triplet.tolist(),
        'upper': green_max_triplet.tolist()
    },
    'blue': {
        'lower': blue_min_triplet.tolist(),
        'upper': blue_max_triplet.tolist()
    },
    'yellow': {
        'lower': yellow_min_triplet.tolist(),
        'upper': yellow_max_triplet.tolist()
    },
    'purple': {
        'lower': purple_min_triplet.tolist(),
        'upper': purple_max_triplet.tolist()
    },
    'ojama': {
        'lower': ojama_min_triplet.tolist(),
        'upper': ojama_max_triplet.tolist()
    }
}

with open('calibration_BGR.json', 'w') as fp:
    json.dump(json_data, fp, indent=4)
