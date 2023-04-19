from model import *
from utilities import *

class App:
    def __init__(self, dual=True):
        self.name = "Viewer"
        self.window = ttk.Window(themename='litera')
        self.window.title(self.name)
        self.window.geometry("1600x800+275+0")
        self.dual = dual

        Label(self.window, text=self.name, font=15, bg="blue", fg="white").pack(side=TOP, fill=BOTH)

        load_models()

        self.set_up_frames()
        self.set_up_model_frame()
        self.set_up_buttons()
        self.set_up_video_frame()
        self.set_up_keys()

        self.window.mainloop()

    def tree_changed_model(self, e):
        print("Tree changed: Model")
        x = self.t_model.selection()
        if len(x) == 0:
            number = 0
        else:
            number = int(x[0])
        self.model = get_model(number)
        print(self.model)

    def set_up_frames(self):
        # Set up frames
        side_width = 130

        # Vertical Frames
        self.frame_a = Frame(self.window, width=side_width, height=800)
        self.frame_b = Frame(self.window, height=800)
        self.frame_c = Frame(self.window, height=800)
        self.frame_a.pack(side="left")
        self.frame_b.pack(side="left")
        self.frame_c.pack(side="left")

    def set_up_model_frame(self):
        self.t_model = new_tree(heading="Model", frame=self.frame_a, height=10, width=150, command_if_changed=self.tree_changed_model)
        self.model = models[0]
        self.update_model_tree()

    def update_model_tree(self):
        tree = self.t_model
        self.clear_tree(tree)
        tree_list = models
        for item in tree_list:
            tree.insert(parent='', index='end', iid=str(item.number), text="Parent", values=item.name)
        tree.selection_set(self.model.number)

    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def set_up_video_frame(self):
        self.video0 = VideoCapture(video_source=0)
        self.canvas0 = Canvas(self.frame_b, width=self.video0.width, height=self.video0.height)
        self.canvas0.pack()
        self.videos = [(self.video0, self.canvas0), ]
        if self.dual:
            self.video1 = VideoCapture(video_source=1)
            self.canvas1 = Canvas(self.frame_c, width=self.video1.width, height=self.video1.height)
            self.canvas1.pack(side=LEFT)
            self.videos.append((self.video1, self.canvas1))
        self.update()

    def set_up_buttons(self):
        # Image capture
        Button(self.frame_b, text="Capture", command=self.capture_image).pack()

        # Recording
        self.v_recording = StringVar(self.frame_b)
        Checkbutton(self.frame_b, text="Record", variable=self.v_recording, onvalue="Recording", offvalue="Not recording").pack()
        self.v_recording.set('0')

    def set_up_keys(self):
        self.window.bind('<Escape>', lambda e: self.exit(e))

    def exit(self, e):
        self.window.destroy()

    def capture_image(self):
        is_open0, frame_cv0, frame0 = self.video0.get_frame(model=self.model, record=False)
        if is_open0:
            filename = self.model.get_next_save_file()
            cv2.imwrite(filename, frame_cv0)
        if self.dual:
            is_open1, frame_cv1, frame1 = self.video1.get_frame(model=self.model, record=False)
            if is_open1:
                filename = self.model.get_next_save_file()
                cv2.imwrite(filename, frame_cv1)

    def update(self):
        recording = self.v_recording.get() == "Recording"
        is_open0, frame_cv0, frame0 = self.video0.get_frame(self.model, record=recording)
        if is_open0:
            self.frame0 = ImageTk.PhotoImage(image=Image.fromarray(frame0))
            boxes = self.model.boxes_live(frame_cv0)
            print(boxes)
            self.canvas0.create_image(0, 0, image=self.frame0, anchor=NW)
        if self.dual:
            is_open1, frame_cv1, frame1 = self.video1.get_frame(self.model, record=recording)
            if is_open1:
                self.frame1 = ImageTk.PhotoImage(image=Image.fromarray(frame1))
                boxes = self.model.boxes_live(frame_cv1)
                print(boxes)
                self.canvas1.create_image(0, 0, image=self.frame1, anchor=NW)
        self.window.after(1, self.update)

class VideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    def get_frame(self, model, record=False):
        is_open, frame = self.vid.read()
        if is_open:
            if record:
                filename = model.get_next_save_file()
                print("Recording:", record, filename)
                cv2.imwrite(filename, frame)

            return is_open, frame, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # def get_frame(self):
    #     is_open, frame = self.vid.read()
    #     return is_open, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def __del__(self):
        self.vid.release()

App(dual=False)