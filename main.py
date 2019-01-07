from create_overlay_image import ChainInfoOverlay
import tkinter as tk
from PIL import ImageTk, Image

class PuyoSpectatorAssist(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.overlay_maker = ChainInfoOverlay(testmode=False)
        self.overlay_image = ImageTk.PhotoImage(file='img/green_bg.png')
        self.displayCanvas = tk.Label(self)
        self.displayCanvas.pack()
        self.test_image = ImageTk.PhotoImage(file='calibration_images/hartman_penglai.png')
        self.ticker = 0
    
    def changeOverlay(self):
        # print('Running')
        # self.ticker += 1

        # if self.ticker % 2 == 0:
        #     image = self.overlay_maker.captureScreen().scrapeMatrices().analyzePops().createOverlay().overlay
        #     self.overlay_image = ImageTk.PhotoImage(image)
        #     self.displayCanvas.config(image=self.overlay_image)
        # else:
        #     self.displayCanvas.config(image=self.test_image)
        image = self.overlay_maker.captureScreen().scrapeMatrices().analyzePops().createOverlay().overlay
        self.overlay_image = ImageTk.PhotoImage(image)
        self.displayCanvas.config(image=self.overlay_image)

        self.after(34, self.changeOverlay)
    
    def run(self):
        self.mainloop()

root = PuyoSpectatorAssist()
root.title('PuyoSpectatorAssist Overlay')
root.geometry('1920x1080')
root.changeOverlay()
root.run()
