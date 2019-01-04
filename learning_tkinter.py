from tkinter import *
from PIL import ImageTk, Image

class MainWindow():
    def __init__(self, main):
        self.canvas = Canvas(main, width=1920, height=1080)
        self.canvas.pack()
        self.canvas.grid(row=0, column=0)
        self.image = ImageTk.PhotoImage(file='calibration_images/amitie_witch.png')

        self.canvas.create_image(200, 200, anchor=NW, image=self.image)


# test_img = Image.open('calibration_images/amitie_witch.png')
# test_img.show()
root = Tk()
root.title('PuyoSpectatorAssist Overlay')
root.geometry('1920x1080')
canvas = Canvas(root, width=1920, height=1080)
canvas.pack()
PILimage = Image.open('calibration_images/amitie_witch.png')

# image = ImageTk.PhotoImage(file='calibration_images/amitie_witch.png')
image = ImageTk.PhotoImage(PILimage)
image2 = ImageTk.PhotoImage(file='calibration_images/hartman_penglai.png')
imagesprite = canvas.create_image(0, 0, anchor=NW, image=image)
imagesprite = canvas.itemconfig(imagesprite, image=image2)
root.mainloop()
