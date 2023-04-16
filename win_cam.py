from tkinter import *
import cv2
from PIL import Image, ImageTk
import time

class App:
    def __init__(self):
        self.name = "Viewer"
        self.window = Tk()
        self.window.title(self.name)
        self.window.geometry("1600x800+275+0")
        # root = ttk.Window(themename='darkly')
        self.video0 = VideoCapture(video_source=0)
        self.video1 = VideoCapture(video_source=1)
        self.Label = Label(self.window, text=self.name, font=15, bg="blue", fg="white").pack(side=TOP, fill=BOTH)
        self.canvas0 = Canvas(self.window, width=self.video0.width, height=self.video0.height, bg="red")
        self.canvas0.pack(side=LEFT)
        self.canvas1 = Canvas(self.window, width=self.video1.width, height=self.video1.height, bg="red")
        self.canvas1.pack(side=LEFT)
        self.update()
        self.window.mainloop()

    def update(self):
        is_open0, frame0 = self.video0.get_frame()
        is_open1, frame1 = self.video1.get_frame()
        if is_open0:
            self.frame0 = ImageTk.PhotoImage(image=Image.fromarray(frame0))
            self.canvas0.create_image(0, 0, image=self.frame0, anchor=NW)
        if is_open1:
            self.frame1 = ImageTk.PhotoImage(image=Image.fromarray(frame1))
            self.canvas1.create_image(0, 0, image=self.frame1, anchor=NW)
        self.window.after(1, self.update)



class VideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    def get_frame(self):
        is_open, frame = self.vid.read()
        return is_open, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def __del__(self):
        self.vid.release()

App()