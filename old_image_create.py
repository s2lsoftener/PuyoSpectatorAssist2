import time
import copy
import numpy as np
import os.path
import mss
from PIL import Image
from PIL import ImageStat
from calibrate_scrn import Player1, Player2, cell_width, cell_height
from calibrate_puyo import getCellColors, RGB_data
from chainsim import simulateChain, game_colors, exportToPN, applyGravity

directory = os.path.dirname(os.path.abspath(__file__))

# Get field
def getField(player):
    with mss.mss() as sct:
        if player == 1:
            sct_img = sct.grab(Player1['board'])
            img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        elif player == 2:
            sct_img = sct.grab(Player2['board'])
            img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    return img


# Guess a cell's color by referencing the above RGB triplets
def getPuyoColor(puyo, threshold=0.2):
    LL = 1 - threshold  # lower limit
    UL = 1 + threshold  # upper limit
    if (puyo[0] > RGB_data['R'][0] * LL and puyo[0] < RGB_data['R'][0] * UL and
        puyo[1] > RGB_data['R'][1] * LL and puyo[1] < RGB_data['R'][1] * UL and
            puyo[2] > RGB_data['R'][2] * LL and puyo[2] < RGB_data['R'][2] * UL):
        return str('R')
    elif (puyo[0] > RGB_data['G'][0] * LL and puyo[0] < RGB_data['G'][0] * UL and
          puyo[1] > RGB_data['G'][1] * LL and puyo[1] < RGB_data['G'][1] * UL and
            puyo[2] > RGB_data['G'][2] * LL and puyo[2] < RGB_data['G'][2] * UL):
        return str('G')
    elif (puyo[0] > RGB_data['B'][0] * LL and puyo[0] < RGB_data['B'][0] * UL and
          puyo[1] > RGB_data['B'][1] * LL and puyo[1] < RGB_data['B'][1] * UL and
            puyo[2] > RGB_data['B'][2] * LL and puyo[2] < RGB_data['B'][2] * UL):
        return str('B')
    elif (puyo[0] > RGB_data['Y'][0] * LL and puyo[0] < RGB_data['Y'][0] * UL and
          puyo[1] > RGB_data['Y'][1] * LL and puyo[1] < RGB_data['Y'][1] * UL and
            puyo[2] > RGB_data['Y'][2] * LL and puyo[2] < RGB_data['Y'][2] * UL):
        return str('Y')
    elif (puyo[0] > RGB_data['P'][0] * LL and puyo[0] < RGB_data['P'][0] * UL and
          puyo[1] > RGB_data['P'][1] * LL and puyo[1] < RGB_data['P'][1] * UL and
            puyo[2] > RGB_data['P'][2] * LL and puyo[2] < RGB_data['P'][2] * UL):
        return str('P')
    elif (puyo[0] > RGB_data['J'][0] * LL and puyo[0] < RGB_data['J'][0] * UL and
          puyo[1] > RGB_data['J'][1] * LL and puyo[1] < RGB_data['J'][1] * UL and
            puyo[2] > RGB_data['J'][2] * LL and puyo[2] < RGB_data['J'][2] * UL):
        return str('J')
    else:
        return str('0')


# Guess cell colors for a whole field
def getFieldPuyoColors(field):
    color_data = getCellColors(field)
    matrix = np.array([['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0']])
    for index1, row in enumerate(color_data):
        for index2, col in enumerate(row):
            matrix[index1 + 1, index2] = getPuyoColor(
                color_data[index1][index2])
    return matrix


# Try out chains
def addSinglePuyos(matrix, color):
    edit_matrix = copy.copy(matrix)
    edit_matrix = applyGravity(edit_matrix)
    matrices = []
    positions = []
    chainlengths = []

    for index, column in enumerate(edit_matrix.T):
        numzero = len(column[column == '0'])
        column[numzero - 1] = color
        matrices.append(copy.copy(edit_matrix))
        column[numzero - 1] = '0'
        positions.append([numzero - 1, index])
    for matrix in matrices:
        simResult = simulateChain(matrix)['chain']
        chainlengths.append(simResult)
    chainlengths = np.array(chainlengths)
    positions = np.array(positions)
    positions = positions[chainlengths > 1]
    chainlengths = chainlengths[chainlengths > 1]
    return [chainlengths, positions, color]


def tryPuyos(matrix, colors=['R', 'G', 'B', 'Y', 'P']):
    results = []
    for color in colors:
        results.append(addSinglePuyos(matrix, color))
    to_remove = []
    for index, result in enumerate(results):
        if len(result[0]) == 0:
            to_remove.append(index)
    to_remove.reverse()  # Remove the items in reverse order
    for item in to_remove:
        del results[int(item)]
    return results


transparent_bg = Image.open(directory + "/img/transparent_bg.png")
red_ret = Image.open(directory + "/img/cursor/red_cursor.png")
red_ret = red_ret.resize((cell_width, cell_height))
green_ret = Image.open(directory + "/img/cursor/green_cursor.png")
green_ret = green_ret.resize((cell_width, cell_height))
blue_ret = Image.open(directory + "/img/cursor/blue_cursor.png")
blue_ret = blue_ret.resize((cell_width, cell_height))
yellow_ret = Image.open(directory + "/img/cursor/yellow_cursor.png")
yellow_ret = yellow_ret.resize((cell_width, cell_height))
purple_ret = Image.open(directory + "/img/cursor/purple_cursor.png")
purple_ret = purple_ret.resize((cell_width, cell_height))
two = Image.open(directory + "/img/numbers/2.png")
three = Image.open(directory + "/img/numbers/3.png")
four = Image.open(directory + "/img/numbers/4.png")
five = Image.open(directory + "/img/numbers/5.png")
six = Image.open(directory + "/img/numbers/6.png")
seven = Image.open(directory + "/img/numbers/7.png")
eight = Image.open(directory + "/img/numbers/8.png")
nine = Image.open(directory + "/img/numbers/9.png")
death = Image.open(directory + "/img/numbers/omg.png")
two = two.resize((cell_width, cell_height))
three = three.resize((cell_width, cell_height))
four = four.resize((cell_width, cell_height))
five = five.resize((cell_width, cell_height))
six = six.resize((cell_width, cell_height))
seven = seven.resize((cell_width, cell_height))
eight = eight.resize((cell_width, cell_height))
nine = nine.resize((cell_width, cell_height))
death = death.resize((cell_width, cell_height))


if __name__ == '__main__':
    starttime = time.time()
    while True:
        # Player 1, initialize values and images
        p1_current = getFieldPuyoColors(getField(1))
        p1_chaintests = tryPuyos(p1_current)
        p1_chaintext = str('')
        p1_overlay = copy.copy(transparent_bg)
        p1_overlaynum = copy.copy(transparent_bg)
        numlines_p1 = 0

        # Player 2, initialize values and images
        p2_current = getFieldPuyoColors(getField(2))
        p2_chaintests = tryPuyos(p2_current)
        p2_chaintext = str('')
        p2_overlay = copy.copy(transparent_bg)
        p2_overlaynum = copy.copy(transparent_bg)
        numlines_p2 = 0

        # Player 1 overlay
        for icol, color in enumerate(p1_chaintests):
            for ipops, pops in enumerate(color[0]):
                row = color[1][ipops][0] + 1
                col = color[1][ipops][1] + 1
                p1_chaintext = (p1_chaintext + str(pops) +
                                ' Chain, Col: ' +
                                str(col) + '\n')
                row_topedge = Player1['board']['top'] + ((row - 2) * cell_height)
                row_bottomedge = Player1['board']['top'] + ((row - 1) * cell_height)
                col_leftedge = Player1['board']['left'] + ((col - 1) * cell_width)
                col_rightedge = Player1['board']['left'] + (col * cell_width)
                reticule_loc = (col_leftedge, row_topedge,
                                col_rightedge, row_bottomedge)
                if color[2] == 'R':
                    p1_overlay.paste(red_ret, reticule_loc)
                if color[2] == 'G':
                    p1_overlay.paste(green_ret, reticule_loc)
                if color[2] == 'B':
                    p1_overlay.paste(blue_ret, reticule_loc)
                if color[2] == 'Y':
                    p1_overlay.paste(yellow_ret, reticule_loc)
                if color[2] == 'P':
                    p1_overlay.paste(purple_ret, reticule_loc)
                if pops == 2:
                    p1_overlaynum.paste(two, reticule_loc)
                if pops == 3:
                    p1_overlaynum.paste(three, reticule_loc)
                if pops == 4:
                    p1_overlaynum.paste(four, reticule_loc)
                if pops == 5:
                    p1_overlaynum.paste(five, reticule_loc)
                if pops == 6:
                    p1_overlaynum.paste(six, reticule_loc)
                if pops == 7:
                    p1_overlaynum.paste(seven, reticule_loc)
                if pops == 8:
                    p1_overlaynum.paste(eight, reticule_loc)
                if pops == 9:
                    p1_overlaynum.paste(nine, reticule_loc)
                if pops >= 10:
                    p1_overlaynum.paste(death, reticule_loc)
                numlines_p1 = numlines_p1 + 1
        if numlines_p1 < 6:
            p1_overlay.save(
                directory + "/image001.png")
            p1_overlaynum.save(
                directory + "/image002.png")
            print(p1_chaintext)

        # Player 2 overlay
        for icol, color in enumerate(p2_chaintests):
            for ipops, pops in enumerate(color[0]):
                row = color[1][ipops][0] + 1
                col = color[1][ipops][1] + 1
                p2_chaintext = (p2_chaintext + str(pops) +
                                ' Chain, Col: ' +
                                str(col) + '\n')
                row_topedge = Player1['board']['top'] + ((row - 2) * cell_height)
                row_bottomedge = Player1['board']['top'] + ((row - 1) * cell_height)
                col_leftedge = Player1['board']['left'] + ((col - 1) * cell_width)
                col_rightedge = Player1['board']['left'] + (col * cell_width)
                reticule_loc = (col_leftedge, row_topedge,
                                col_rightedge, row_bottomedge)
                if color[2] == 'R':
                    p2_overlay.paste(red_ret, reticule_loc)
                if color[2] == 'G':
                    p2_overlay.paste(green_ret, reticule_loc)
                if color[2] == 'B':
                    p2_overlay.paste(blue_ret, reticule_loc)
                if color[2] == 'Y':
                    p2_overlay.paste(yellow_ret, reticule_loc)
                if color[2] == 'P':
                    p2_overlay.paste(purple_ret, reticule_loc)
                if pops == 2:
                    p2_overlaynum.paste(two, reticule_loc)
                if pops == 3:
                    p2_overlaynum.paste(three, reticule_loc)
                if pops == 4:
                    p2_overlaynum.paste(four, reticule_loc)
                if pops == 5:
                    p2_overlaynum.paste(five, reticule_loc)
                if pops == 6:
                    p2_overlaynum.paste(six, reticule_loc)
                if pops == 7:
                    p2_overlaynum.paste(seven, reticule_loc)
                if pops == 8:
                    p2_overlaynum.paste(eight, reticule_loc)
                if pops == 9:
                    p2_overlaynum.paste(nine, reticule_loc)
                if pops >= 10:
                    p2_overlaynum.paste(death, reticule_loc)
                numlines_p2 = numlines_p2 + 1
        if numlines_p2 < 6:
            p2_overlay.save(
                directory + "/image003.png")
            p2_overlaynum.save(
                directory + "/image004.png")
            print(p2_chaintext)
        time.sleep(0.7 - ((time.time() - starttime) % 0.7))
    
© 2019 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
Press h to open a hovercard with more details.