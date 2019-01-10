from create_overlay_image import ChainInfoOverlay
import tkinter as tk
from PIL import ImageTk, Image
import cv2
import numpy as np

class PuyoSpectatorAssist(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.overlay_maker = ChainInfoOverlay(testmode=False)
        self.overlay_image = ImageTk.PhotoImage(file='img/green_bg.png')
        self.displayCanvas = tk.Label(self)
        self.displayCanvas.pack()
        self.test_image = ImageTk.PhotoImage(file='calibration_images/hartman_penglai.png')
        self.screenshot = None
        self.ticker = 0
        self.p1_masks = [np.zeros((1080, 1920), np.uint8)] * 4
        self.p2_masks = [np.zeros((1080, 1920), np.uint8)] * 4
        self.p1_next_BGRs = [[0, 0, 0]] * 4
        self.p2_next_BGRs = [[0, 0, 0]] * 4

        cv2.rectangle(self.p1_masks[0], (774, 356), (809, 371), (255, 255, 255), -1)
        cv2.rectangle(self.p1_masks[1], (774, 306), (809, 321), (255, 255, 255), -1)
        cv2.rectangle(self.p1_masks[2], (734, 256), (769, 271), (255, 255, 255), -1)
        cv2.rectangle(self.p1_masks[3], (734, 176), (769, 191), (255, 255, 255), -1)
        cv2.rectangle(self.p2_masks[0], (1100, 356), (1135, 371), (255, 255, 255), -1)
        cv2.rectangle(self.p2_masks[1], (1100, 306), (1135, 321), (255, 255, 255), -1)
        cv2.rectangle(self.p2_masks[2], (1150, 256), (1185, 271), (255, 255, 255), -1)
        cv2.rectangle(self.p2_masks[3], (1150, 176), (1185, 191), (255, 255, 255), -1)

    def detectPieceChange(self):
        self.screenshot = self.overlay_maker.captureScreen().screenshot

        new_p1_next_BGRs = [[]] * 4
        new_p2_next_BGRs = [[]] * 4

        p1_change = False
        p2_change = False

        for index, new_BGR in enumerate(new_p1_next_BGRs):
            new_BGR = cv2.mean(self.screenshot, mask=self.p1_masks[index])[:3]
            if new_BGR != self.p1_next_BGRs[index]: p1_change = True
            self.p1_next_BGRs[index] = new_BGR

        for index, new_BGR in enumerate(new_p2_next_BGRs):
            new_BGR = cv2.mean(self.screenshot, mask=self.p2_masks[index])[:3]
            if new_BGR != self.p2_next_BGRs[index]: p2_change = True
            self.p2_next_BGRs[index] = new_BGR

        if p1_change is True: print('P1 next piece changed.')
        if p2_change is True: print('P2 next piece changed.')
        self.changeOverlay(p1_change=p1_change, p2_change=p2_change)

    def changeOverlay(self, p1_change = False, p2_change = False):
        self.overlay_maker.scrapeMatrices().analyzePops()

        if p1_change is True: self.overlay_maker.display_p1 = True
        if p2_change is True: self.overlay_maker.display_p2 = True
        
        overlay = self.overlay_maker.createOverlay().overlay

        self.overlay_image = ImageTk.PhotoImage(overlay)
        self.displayCanvas.config(image=self.overlay_image)

        self.after(17, self.detectPieceChange)
    
    def run(self):
        self.mainloop()

root = PuyoSpectatorAssist()
root.title('PuyoSpectatorAssist Overlay')
root.geometry('1920x1080')
root.detectPieceChange()
root.run()
