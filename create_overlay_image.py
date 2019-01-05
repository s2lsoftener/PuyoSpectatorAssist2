import numpy as np
import os
from PIL import Image
from mss import mss
import cv2
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

# Get bruteforcepops
# Player 1
test_result = BruteForcePop(test_matrix, settings, print_result=False).popping_matrices
for result in test_result:
    row = result['row']
    col = result['col']
    color = result['color']
    chain_length = result['chain_length']

    start_x = 279
    start_y = 159

    x = start_x + 64 * col
    y = start_y + 60 * row

    green_bg.paste(reticules[color], (x, y), reticules[color])
    green_bg.paste(numbers[str(chain_length)], (x, y), numbers[str(chain_length)])

# green_bg.show()

def captureScreen():
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

        # Grab the data
        sct_img = sct.grab(monitor)
        
        # Convert to PIL image
        PIL_img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        PIL_img.save('calibration_images/ringo_ss_2.png')
        return cv2.cvtColor(np.array(PIL_img), cv2.COLOR_RGB2BGR)


screenshot = captureScreen()
p1 = scrapeMatrix(screenshot, 1)
print(p1)


class ChainInfoOverlay():
    def __init__(self):
        self.screenshot = None
        self.p1_matrix = [[]]
        self.p2_matrix = [[]]
        self.p1_chains = []
        self.p2_chains = []

    def captureScreen(self):
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
        

