import numpy as np
import os
from PIL import Image
from mss import mss
import cv2
import copy
from simulator import BruteForcePop, SimulatorSettings
from scrape_matrix import scrapeMatrix

# Test matrix
test_matrix = np.asarray([['0', '0', '0', '0', '0', '0'],
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

# Initialize Chainsim settings
settings = SimulatorSettings()

# Load images
cell_width = 64
cell_height = 60

green_bg = Image.open('img/green_bg.png')
red_ret = Image.open('img/cursor/red_cursor.png')
red_ret = red_ret.resize((cell_width, cell_height))
green_ret = Image.open('img/cursor/green_cursor.png')
green_ret = green_ret.resize((cell_width, cell_height))
blue_ret = Image.open('img/cursor/blue_cursor.png')
blue_ret = blue_ret.resize((cell_width, cell_height))
yellow_ret = Image.open('img/cursor/yellow_cursor.png')
yellow_ret = yellow_ret.resize((cell_width, cell_height))
purple_ret = Image.open('img/cursor/purple_cursor.png')
purple_ret = purple_ret.resize((cell_width, cell_height))
reticules = {
    'R': red_ret,
    'G': green_ret,
    'B': blue_ret,
    'Y': yellow_ret,
    'P': purple_ret
}

two = Image.open('img/numbers/2.png')
three = Image.open('img/numbers/3.png')
four = Image.open('img/numbers/4.png')
five = Image.open('img/numbers/5.png')
six = Image.open('img/numbers/6.png')
seven = Image.open('img/numbers/7.png')
eight = Image.open('img/numbers/8.png')
nine = Image.open('img/numbers/9.png')
omg = Image.open('img/numbers/omg.png')
two = two.resize((cell_width, cell_height))
three = three.resize((cell_width, cell_height))
four = four.resize((cell_width, cell_height))
five = five.resize((cell_width, cell_height))
six = six.resize((cell_width, cell_height))
seven = seven.resize((cell_width, cell_height))
eight = eight.resize((cell_width, cell_height))
nine = nine.resize((cell_width, cell_height))
omg = omg.resize((cell_width, cell_height))
numbers = {
    '2': two,
    '3': three,
    '4': four,
    '5': five,
    '6': six,
    '7': seven,
    '8': eight,
    '9': nine,
    '10': omg,
    '11': omg,
    '12': omg,
    '13': omg,
    '14': omg,
    '15': omg,
    '16': omg,
    '17': omg,
    '18': omg,
    '19': omg
}

class ChainInfoOverlay:
    def __init__(self, testmode = False):
        self.screenshot = None
        self.p1_matrix = [[]]
        self.p2_matrix = [[]]
        self.p1_analysis = None
        self.p2_analysis = None
        self.settings = SimulatorSettings()
        self.background = copy.copy(green_bg)
        self.overlay = copy.copy(self.background)
        self.testmode = testmode
        self.display_p1 = True
        self.display_p2 = True


    def captureScreen(self):
        if self.testmode == True:
            PIL_img = Image.open('calibration_images/lagnus2.png')
            self.screenshot = cv2.cvtColor(np.array(PIL_img), cv2.COLOR_RGB2BGR)
        else:
            with mss() as sct:
                # Get information of monitor 1
                monitor_number = 1
                mon = sct.monitors[monitor_number]

                # The screen part to capture
                monitor = {
                    "top": -1080,
                    "left": -960,
                    "width": 1920,
                    "height": 1080,
                    "mon": monitor_number,
                }

                # Take screenshot and save to self.screenshot
                sct_img = sct.grab(monitor)
                PIL_img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
                self.screenshot = cv2.cvtColor(np.array(PIL_img), cv2.COLOR_RGB2BGR)
        return self
    
    def scrapeMatrices(self):
        self.p1_matrix = scrapeMatrix(self.screenshot, 1)
        self.p2_matrix = scrapeMatrix(self.screenshot, 2)
        return self
    
    def analyzePops(self):     
        self.p1_analysis = BruteForcePop(self.p1_matrix, self.settings, print_result=False)
        self.p2_analysis = BruteForcePop(self.p2_matrix, self.settings, print_result=False)

        if self.p1_analysis.already_popping is True: self.display_p1 = False
        if self.p2_analysis.already_popping is True: self.display_p2 = False

        return self
    
    def createOverlay(self):
        self.overlay = copy.copy(self.background)

        # Player 1
        if self.display_p1 is True:
            for chain in self.p1_analysis.popping_matrices:
                start_x = 279
                start_y = 159

                x = start_x + 64 * chain['col']
                y = start_y + 60 * (chain['row'] - 1)

                self.overlay.paste(reticules[chain['color']], (x, y), reticules[chain['color']])
                self.overlay.paste(numbers[str(chain['chain_length'])], (x, y), numbers[str(chain['chain_length'])])
        
        # Player 2
        if self.display_p2 is True:
            for chain in self.p2_analysis.popping_matrices:
                start_x = 1256
                start_y = 159

                x = start_x + 64 * chain['col']
                y = start_y + 60 * (chain['row'] - 1)

                self.overlay.paste(reticules[chain['color']], (x, y), reticules[chain['color']])
                self.overlay.paste(numbers[str(chain['chain_length'])], (x, y), numbers[str(chain['chain_length'])])
        
        return self
