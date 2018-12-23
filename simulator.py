import numpy as np
import copy

test_matrix = np.asarray([['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['R', '0', '0', '0', '0', '0'],
                          ['0', 'R', '0', '0', '0', '0'],
                          ['0', '0', 'B', '0', '0', '0'],
                          ['0', '0', 'B', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0'],
                          ['0', '0', '0', '0', '0', '0']])

# Settings
puyo_colors = ['R', 'G', 'B', 'Y', 'P'] # Red, Gree, Blue, Yellow, Purple
garbage_types = ['J', 'H', 'N', 'S'] # oJama, Hard, poiNt, Sun
puyo_to_pop = 4
target_point = 70
chain_powers = [0, 8, 16, 32, 64, 96, 128, 160, 192, 224, 256,
                288, 320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672]
color_bonus = [0, 3, 6, 12, 24]
group_bonus = [0, 2, 3, 4, 5, 6, 7, 10]

# Value checking functions
def typeOfPuyo(p): # Expects one-letter string
    if p == '0':
        return 'empty'
    elif p in puyo_colors:
        return 'puyo'
    elif p in garbage_types:
        return 'garbage'
    else:
        return 'error'

# Check if passed matrix has groups that can pop
def applyGravity(matrix):
    matrix = copy.copy(matrix)
    matrix = np.transpose(matrix) # Transpose to manipulate by board column
    for col in matrix:
        filter_empty = col[col != '0']
        if len(filter_empty) > 0:
            col[:] = '0'
            col[-len(filter_empty):] = filter_empty
    return np.transpose(matrix)

# Check for pops
def checkPops(matrix):
    # Create a matrix that tracks which cells have already been tested.
    checkMatrix = np.empty_like(matrix)