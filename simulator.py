import numpy as np
import math
import copy
import webbrowser

test_matrix = np.asarray([['0', 'B', 'B', '0', '0', '0'],
                          ['0', 'B', 'B', '0', '0', '0'],
                          ['Y', 'B', 'B', '0', '0', '0'],
                          ['Y', 'B', 'B', '0', '0', '0'],
                          ['Y', 'J', 'J', 'Y', '0', '0'],
                          ['Y', 'G', 'Y', 'Y', '0', '0'],
                          ['R', 'G', 'Y', 'Y', 'Y', '0'],
                          ['R', 'R', 'Y', 'Y', 'Y', '0'],
                          ['R', 'R', 'B', 'Y', 'Y', '0'],
                          ['R', 'R', 'B', 'Y', 'Y', '0'],
                          ['R', 'R', 'B', 'B', 'Y', '0'],
                          ['R', 'R', 'B', 'B', 'Y', '0'],
                          ['R', 'R', 'B', 'B', 'Y', '0']])

test_matrix2 = np.asarray([['0', '0', '0', '0', '0', '0'],
                           ['0', '0', '0', '0', '0', '0'],
                           ['0', '0', '0', '0', '0', '0'],
                           ['0', '0', '0', '0', '0', '0'],
                           ['0', '0', '0', '0', '0', '0'],
                           ['J', '0', '0', '0', '0', 'R'],
                           ['J', '0', '0', '0', '0', 'R'],
                           ['B', 'G', '0', '0', '0', 'R'],
                           ['G', 'Y', 'Y', '0', 'R', 'Y'],
                           ['G', 'G', 'Y', '0', 'J', 'Y'],
                           ['B', 'R', 'G', 'P', 'J', 'Y'],
                           ['B', 'B', 'R', 'G', 'P', 'P'],
                           ['R', 'R', 'G', 'G', 'P', 'Y']])

class SimulatorSettings:
    def __init__(self, settings = None):
        '''
        Load default Tsu rule settings by default.
        Supply settings {} otherwise.
        '''
        if settings is None:
            self.puyo_colors = ['R', 'G', 'B', 'Y', 'P']
            self.garbage_types = ['J', 'H', 'N', 'S']
            self.puyo_to_pop = 4
            self.target_point = 70
            self.hidden_rows = 1
            self.chain_powers = [0, 8, 16, 32, 64, 96, 128, 160, 192, 224, 256,
                                 288, 320, 352, 384, 416, 448, 480, 512, 544,
                                 576, 608, 640, 672]
            self.color_bonus = [0, 3, 6, 12, 24]
            self.group_bonus = [0, 2, 3, 4, 5, 6, 7, 10]
        else:
            self.puyo_colors = settings['puyo_colors']
            self.garbage_types = settings['garbage_types']
            self.puyo_to_pop = settings['puyo_to_pop']
            self.target_point = settings['target_point']
            self.hidden_rows = settings['hidden_rows']
            self.chain_powers = settings['chain_powers']
            self.color_bonus = settings['color_bonus']
            self.group_bonus = settings['group_bonus']

class ChainSimulator:
    '''
    Creates a Puyo field object with chain analysis methods.
    Use SimulatorSettings() to supply this class with
        a settings object.

    Properties:
    matrix -- 2D Numpy Array with one-letter strings for each cell
    initial_matrix -- copy of original input matrix
    settings -- imported settings object from SimulatorSettings class
    popping_groups -- list containing groups of puyos (as lists) that
                      will pop
    popping_garbage -- list containing garbage puyos that will pop
    has_pops -- Initializes with None. Ends simulator loop when value
                is False.
    chain_length -- Length of the chain
    score -- total score of the chain
    link_score -- score for the currently popping link
    garbage_count -- total garbage the chain would send
    link_garbage_count -- garbage the current popping link would send
    leftover_NP -- leftover nuisance points from rounding after
                   dividing by target point.
    '''
    def __init__(self, matrix, settings):
        self.matrix = copy.copy(matrix)
        self.initial_matrix = copy.copy(matrix)
        self.settings = settings
        self.popping_groups = []
        self.popping_garbage = []
        self.has_pops = None
        self.chain_length = 0
        self.score = 0
        self.link_score = 0
        self.garbage_count = 0
        self.link_garbage_count = 0
        self.leftover_NP = 0

    def applyGravity(self):
        matrix = np.transpose(self.matrix)
        for col in matrix:
            filter_empty = col[col != '0']
            if len(filter_empty) > 0:
                col[:] = '0'
                col[-len(filter_empty):] = filter_empty
        self.matrix = np.transpose(matrix)
        return self

    def checkPuyoPops(self):
        # Create a matrix that tracks which cells have already been tested.
        check_matrix = np.zeros_like(self.matrix, dtype=bool)

        # List of groups that will pop
        popping_groups = []

        # Matrix dimensions
        rows = self.matrix.shape[0]
        cols = self.matrix.shape[1]

        # Loop over matrix
        for row in range(self.settings.hidden_rows, rows):
            for col in range(0, cols):
                if check_matrix[row, col] == False:
                    # Mark this cell as checked
                    check_matrix[row, col] = True

                    # Initiate group finding if this is a colored Puyo
                    if self.matrix[row, col] in self.settings.puyo_colors:
                        current_group = [{
                            'color': self.matrix[row, col],
                            'row': row,
                            'col': col
                        }]

                        for p in current_group:
                            # Check up (but not into the hidden rows)
                            if (p['row'] > self.settings.hidden_rows and
                                p['color'] == self.matrix[p['row'] - 1, p['col']] and
                                check_matrix[p['row'] - 1, p['col']] == False):
                                # Add Puyo above to current group
                                current_group.append({
                                    'color': self.matrix[p['row'] - 1, p['col']],
                                    'row': p['row'] - 1,
                                    'col': p['col']
                                })
                                check_matrix[p['row'] - 1, p['col']] = True

                            # Check down (but not into the floor)
                            if (p['row'] < rows - 1 and
                                p['color'] == self.matrix[p['row'] + 1, p['col']] and
                                check_matrix[p['row'] + 1, p['col']] == False):
                                # Add Puyo below to current group
                                current_group.append({
                                    'color': self.matrix[p['row'] + 1, p['col']],
                                    'row': p['row'] + 1,
                                    'col': p['col']
                                })
                                check_matrix[p['row'] + 1, p['col']] = True

                            # Check left (but not into the wall)
                            if (p['col'] > 0 and
                                p['color'] == self.matrix[p['row'], p['col'] - 1] and
                                check_matrix[p['row'], p['col'] - 1] == False):
                                # Add Puyo to the left to current group
                                current_group.append({
                                    'color': self.matrix[p['row'], p['col'] - 1],
                                    'row': p['row'],
                                    'col': p['col'] - 1
                                })
                                check_matrix[p['row'], p['col'] - 1] = True

                            # Check right (but not into the wall)
                            if (p['col'] < cols - 1 and
                                p['color'] == self.matrix[p['row'], p['col'] + 1] and
                                check_matrix[p['row'], p['col'] + 1] == False):
                                # Add Puyo to the left to current group
                                current_group.append({
                                    'color': self.matrix[p['row'], p['col'] + 1],
                                    'row': p['row'],
                                    'col': p['col'] + 1
                                })
                                check_matrix[p['row'], p['col'] + 1] = True

                        if len(current_group) >= self.settings.puyo_to_pop:
                            popping_groups.append(current_group)

        self.popping_groups = popping_groups

        # Mark if the chain can pop and increment chain length
        if len(self.popping_groups) > 0:
            self.has_pops = True
            self.chain_length += 1
        else:
            self.has_pops = False

        return self

    def checkGarbagePops(self):
        popping_garbage = []
        matrix = self.matrix
        garbage_types = self.settings.garbage_types

        for group in self.popping_groups:
            for puyo in group:
                row = puyo['row']
                col = puyo['col']
                
                # Check up
                if (row > 0 and
                    matrix[row - 1, col] in garbage_types):
                    popping_garbage.append({
                        'color': matrix[row - 1, col],
                        'row': row - 1,
                        'col': col
                    })

                # Check down
                if (row < matrix.shape[0] - 1 and
                    matrix[row + 1, col] in garbage_types):
                    popping_garbage.append({
                        'color': matrix[row + 1, col],
                        'row': row + 1,
                        'col': col
                    })

                # Check left
                if (col > 0 and
                    matrix[row, col - 1] in garbage_types):
                    popping_garbage.append({
                        'color': matrix[row, col - 1],
                        'row': row,
                        'col': col - 1
                    })

                # Check right
                if (col < matrix.shape[1] - 1 and
                    matrix[row, col + 1] in garbage_types):
                    popping_garbage.append({
                        'color': matrix[row, col + 1],
                        'row': row,
                        'col': col + 1
                    })

        self.popping_garbage = popping_garbage

        return self

    def scoreChainLink(self):
        color_bonus = self.settings.color_bonus
        chain_powers = self.settings.chain_powers
        
        # Determine group bonus
        link_group_bonus = 0
        for group in self.popping_groups:
            if len(group) >= 11: link_group_bonus += self.settings.group_bonus[-1]
            else: link_group_bonus += self.settings.group_bonus[len(group) - 4]

        # Count the number of different colors
        link_colors = set()
        for group in self.popping_groups:
            link_colors.add(group[0]['color'])
        link_color_bonus = color_bonus[len(link_colors) - 1]

        # Retrieve chain power from power table
        if self.chain_length > len(chain_powers):
            link_chain_power = self.settings.chain_powers[-1]
        else:
            link_chain_power = self.settings.chain_powers[self.chain_length - 1]

        # Count the number of Puyos being cleared
        link_puyo_cleared = 0
        for group in self.popping_groups: link_puyo_cleared += len(group)

        # Determine the link's total bonus
        link_total_bonuses = link_group_bonus + link_color_bonus + link_chain_power
        # Total bonus must be a value between 1 and 999, inclusive.
        if link_total_bonuses < 1: link_total_bonuses = 1
        elif link_total_bonuses > 999: link_total_bonuses = 999

        # Calculate score
        link_score = 10 * link_puyo_cleared * link_total_bonuses
        self.link_score = link_score
        self.score += link_score

        return self

    def calculateGarbage(self):
        nuisance_points = self.link_score / self.settings.target_point + self.leftover_NP
        nuisance_count = math.floor(nuisance_points)
        self.leftover_NP = nuisance_points - nuisance_count
        self.garbage_count += nuisance_count
        self.link_garbage_count = nuisance_count

        return self

    def popPuyos(self):
        for group in self.popping_groups:
            for puyo in group:
                row = puyo['row']
                col = puyo['col']
                self.matrix[row, col] = '0'
        return self

    def popGarbage(self):
        for garbage in self.popping_garbage:
            row = garbage['row']
            col = garbage['col']
            if garbage['color'] == 'J': self.matrix[row, col] = '0'
            elif garbage['color'] == 'H': self.matrix[row, col] = 'J'
        return self

    def simulateLink(self):
        self.applyGravity() \
            .checkPuyoPops() \
            .checkGarbagePops() \
        
        if self.has_pops == True:
            self.scoreChainLink() \
                .calculateGarbage() \
                .popPuyos() \
                .popGarbage() \
                .applyGravity()

        return self

    def simulateChain(self):
        while self.has_pops is not False: self.simulateLink()
        return self
    
    def openURL(self, chain = 'initial'):
        convert = {'R': 4,
               'G': 7,
               'B': 5,
               'Y': 6,
               'P': 8,
               'J': 1,
               '0': 0}

        if chain == 'initial':
            PN_matrix = copy.copy(self.initial_matrix)
        elif chain == 'result':
            PN_matrix = copy.copy(self.matrix)

        # Matrix dimensions
        rows = PN_matrix.shape[0]
        cols = PN_matrix.shape[1]

        for row in range(0, rows):
            for col in range(0, cols):
                PN_matrix[row, col] = convert[str(PN_matrix[row, col])]

        chaincode = str()
        for r in range(len(PN_matrix)):
            chaincode += np.array2string(PN_matrix[r]).replace(
                '[', '').replace("\'", "").replace(']', '').replace(' ', '')

        url = ('https://puyonexus.com/chainsim/?w=' + str(PN_matrix.shape[1]) +
            '&h=' + str(PN_matrix.shape[0] - 1) + '&chain=' + str(chaincode))
        webbrowser.open(url)

class BruteForcePop:
    def __init__(self, matrix, settings, auto = True, print_result = True):
        self.matrix = copy.copy(matrix)
        self.settings = settings
        self.test_matrices = []
        self.popping_matrices = []
        self.already_popping = False
        if auto is True:
            self.generateMatrices().simulateMatrices()
            if print_result is True: print(self.popping_matrices)

    def generateMatrices(self):
        # Check if matrix is already popping.
        # Don't continue with rest of function if it is.
        test_matrix = ChainSimulator(self.matrix, self.settings).simulateChain()
        if test_matrix.chain_length > 0:
            self.already_popping = True
            return self
        
        # Add a single Puyo of each color in each column
        for color in self.settings.puyo_colors:
            for col in range(0, self.matrix.shape[1]):
                if self.matrix[0, col] == '0':
                    matrix = copy.copy(self.matrix)

                    # Get row position of added Puyo
                    row_matrix = np.transpose(copy.copy(matrix))
                    row = len(row_matrix[col][row_matrix[col] == '0'])

                    # Add data to self.test_matrices
                    matrix[0, col] = color
                    self.test_matrices.append({
                        'matrix': matrix,
                        'color': color,
                        'row': row - 1,
                        'col': col,
                        'score': 0,
                        'chain_length': 0
                    })
        
        # Add a double Puyo of each color in each column
        for color in self.settings.puyo_colors:
            for col in range(0, self.matrix.shape[1]):
                if self.matrix[0, col] == '0' and self.matrix[1, col] == '0':
                    matrix = copy.copy(self.matrix)

                    # Get row position of added Puyo
                    row_matrix = np.transpose(copy.copy(matrix))
                    row = len(row_matrix[col][row_matrix[col] == '0'])

                    # Add data to self.test_matrices
                    matrix[0:2, col] = color
                    self.test_matrices.append({
                        'matrix': matrix,
                        'color': color,
                        'row': row - 1,
                        'col': col,
                        'score': 0,
                        'chain_length': 0
                    })
        return self

    def simulateMatrices(self):
        for matrix_data in self.test_matrices:
            matrix = copy.copy(matrix_data['matrix'])
            sim = ChainSimulator(matrix, self.settings).simulateChain()
            matrix_data['score'] = sim.score
            matrix_data['chain_length'] = sim.chain_length
            if matrix_data['chain_length'] >= 2:
                self.popping_matrices.append(matrix_data)
        return self

settings = SimulatorSettings()
