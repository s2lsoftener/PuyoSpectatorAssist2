import json
import numpy as np
import cv2
from simulator import SimulatorSettings, ChainSimulator

with open('calibration_BGR.json', 'r') as fp:
    color_limits = json.load(fp)

def cropPuyo(screenshot, player_num, rowcoltuple):
    row = rowcoltuple[0]
    col = rowcoltuple[1]

    if player_num == 1:
        start_x = 279
        start_y = 159
    elif player_num == 2:
        start_x = 1256
        start_y = 159

    x1 = start_x + 64 * col
    x2 = start_x + 64 * (col + 1)
    y1 = start_y + 60 * row
    y2 = start_y + 60 * (row + 1)

    return screenshot[y1:y2, x1:x2]

def guessColor(puyo_img, limits):
    height, width = puyo_img.shape[0], puyo_img.shape[1]
    circle_mask = np.zeros((height, width), np.uint8)
    cv2.circle(circle_mask, (width // 2, height // 2), height // 2, (255, 255, 255), -1)
    avg_color = cv2.mean(puyo_img, mask=circle_mask)[:3]

    color = ''
    if (avg_color[0] > limits['red']['lower'][0] and avg_color[0] < limits['red']['upper'][0] and
            avg_color[1] > limits['red']['lower'][1] and avg_color[1] < limits['red']['upper'][1] and
            avg_color[2] > limits['red']['lower'][2] and avg_color[2] < limits['red']['upper'][2]):
        color = 'R'
    elif (avg_color[0] > limits['blue']['lower'][0] and avg_color[0] < limits['blue']['upper'][0] and
            avg_color[1] > limits['blue']['lower'][1] and avg_color[1] < limits['blue']['upper'][1] and
            avg_color[2] > limits['blue']['lower'][2] and avg_color[2] < limits['blue']['upper'][2]):
        color = 'B'
    elif (avg_color[0] > limits['green']['lower'][0] and avg_color[0] < limits['green']['upper'][0] and
            avg_color[1] > limits['green']['lower'][1] and avg_color[1] < limits['green']['upper'][1] and
            avg_color[2] > limits['green']['lower'][2] and avg_color[2] < limits['green']['upper'][2]):
        color = 'G'
    elif (avg_color[0] > limits['yellow']['lower'][0] and avg_color[0] < limits['yellow']['upper'][0] and
            avg_color[1] > limits['yellow']['lower'][1] and avg_color[1] < limits['yellow']['upper'][1] and
            avg_color[2] > limits['yellow']['lower'][2] and avg_color[2] < limits['yellow']['upper'][2]):
        color = 'Y'
    elif (avg_color[0] > limits['purple']['lower'][0] and avg_color[0] < limits['purple']['upper'][0] and
            avg_color[1] > limits['purple']['lower'][1] and avg_color[1] < limits['purple']['upper'][1] and
            avg_color[2] > limits['purple']['lower'][2] and avg_color[2] < limits['purple']['upper'][2]):
        color = 'P'
    elif (avg_color[0] > limits['ojama']['lower'][0] and avg_color[0] < limits['ojama']['upper'][0] and
            avg_color[1] > limits['ojama']['lower'][1] and avg_color[1] < limits['ojama']['upper'][1] and
            avg_color[2] > limits['ojama']['lower'][2] and avg_color[2] < limits['ojama']['upper'][2]):
        color = 'J'
    else:
        color = '0'
    
    return(color)

def scrapeMatrix(screenshot, player_num):
    matrix = [['0', '0', '0', '0', '0', '0']]
    for row in range(0, 12):
        new_row = []
        for col in range (0, 6):
            puyo = cropPuyo(screenshot, player_num, (row, col))
            color = guessColor(puyo, color_limits)
            new_row.append(color)
        matrix.append(new_row)
    return np.asarray(matrix)

if __name__ == '__main__':
    # Test read
    settings = SimulatorSettings()
    test_image = cv2.imread('calibration_images/ringo_seriri_1.png')
    matrix = scrapeMatrix(test_image, 2)
    puyo_matrix = ChainSimulator(matrix, settings).simulateChain()
    print(puyo_matrix.initial_matrix)
    puyo_matrix.openURL()
