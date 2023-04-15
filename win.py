from model import *
from utilities import *
from PIL import Image, ImageTk

# Variables
mouse_id = None
label_ids = []
label_m_ids = []

# Frame 1
def tree_changed_label(e):
    set_current_label()
    e_name.delete(0,END)
    e_name.insert(0,current_label.name)
    e_colour.delete(0,END)
    e_colour.insert(0,current_label.colour)
    v_label_w.set(current_label.width)
    v_label_h.set(current_label.height)
    v_label_name.set(current_label.name)

def tree_changed_model(e):
    global current_image
    set_current_model()
    e_model_name.delete(0,END)
    e_model_name.insert(0,current_model.name)
    update_tree(t_label)
    current_image = current_model.get_first_image()
    update_tree(t_image)

def update_tree(tree):
    clear_tree(tree)
    if tree == t_image:
        update_tree_images()
        return
    if tree == t_label:
        tree_list = current_model.labels
        current = current_label
    elif tree == t_model:
        tree_list = models
        current = current_model
    # print("Update tree:", tree, tree_list)
    for item in tree_list:
        tree.insert(parent='', index='end', iid=str(item.number), text="Parent", values=item.name)
    tree.selection_set(current.number)

def update_tree_images():
    clear_tree(t_image)
    for count, item in enumerate(current_model.images):
        manual_labels = int(len(item.labels))
        model_labels = len(item.box_list)
        tag = "normal"
        if manual_labels < model_labels: tag = "red"
        if manual_labels > model_labels: tag = "blue"
        t_image.insert(parent='', index='end', iid=str(item.number), text="Parent", values=(item.name, f"{int(len(item.labels))} {len(item.box_list)}"), tags=tag)
    if current_image:
        t_image.selection_set(current_image.number)

def clear_tree(tree):
    for item in tree.get_children():
        tree.delete(item)

def set_current_label():
    global current_label
    x = t_label.selection()
    if len(x) == 0: label_number = 0
    else: label_number = int(x[0])
    current_label = current_model.get_label(label_number)
    v_label_w.set(current_label.width // 2)
    v_label_h.set(current_label.height // 2)

def set_current_model():
    global current_model
    x = t_model.selection()
    if len(x) == 0: number = 0
    else: number = int(x[0])
    current_model = get_model(number)
    # print("Set current model:", current_model, number, x)
    update_model_info()

# Frame 2a
def mouse_move(e):
    if var_delete.get() == "Delete Mode": return
    draw_mouse_rectangle(e.x, e.y)

def draw_mouse_rectangle(x, y):
    global mouse_id
    if mouse_id: canvas.delete(mouse_id)
    x1, y1 = x - current_label.width // 2, y - current_label.height // 2
    x2, y2 = x + current_label.width // 2, y + current_label.height // 2
    mouse_id = canvas.create_rectangle(x1, y1, x2, y2, outline=current_label.colour, width=2)

def mouse_rectangle_clear(e):
    global rectangle_label
    if mouse_id: canvas.delete(mouse_id)

def mouse_click(e):
    # A mouse click to create new label
    if var_delete.get() == "Delete Mode":
        current_image.delete_label(e.x, e.y)
    else:
        x1, y1 = e.x - current_label.width // 2, e.y - current_label.height // 2
        x2, y2 = e.x + current_label.width // 2, e.y + current_label.height // 2
        w, h = current_image.image.width(), current_image.image.height()
        current_image.add_label(current_label.number, x1, y1, x2, y2, w, h)
    add_label_rectangles()
    update_tree_images()

def copy_modelled_labels():
    # print(current_image.box_list)
    for id, x1, y1, x2, y2 in current_image.box_list:
        w, h = current_image.image.width(), current_image.image.height()
        current_image.add_label(id, x1, y1, x2, y2, w, h)
    next_image()

def add_label_rectangles():
    global label_ids

    # Remove existing labels
    for id in label_ids: canvas.delete(id)
    label_ids = []

    if current_image is None: return

    # Add new labels
    width, height = current_image.image.width(), current_image.image.height()
    for class_id, x, y, w, h in current_image.labels:
        label = current_model.get_label(class_id)
        if label is None: label = current_model.get_label(0)
        x1, y1 = int(x * width), int(y * height)
        x2, y2 = int((x + w) * width), int((y + h) * height)
        label_id = canvas.create_rectangle(x1, y1, x2, y2, outline=label.colour, width=2)
        label_ids.append(label_id)

def add_label_rectangles_m():
    global label_m_ids

    # Remove existing labels
    for id in label_m_ids: canvas_m.delete(id)
    label_m_ids = []

    # Add new labels
    boxes = current_model.boxes(current_image)

    for class_id, x1, y1, x2, y2 in boxes:
        label = current_model.get_label(class_id)
        if label is None: label = current_model.get_label(0)
        label_id = canvas_m.create_rectangle(x1, y1, x2, y2, outline=label.colour, width=2)
        label_m_ids.append(label_id)

# Frame 2b
def load_videos():
    current_model.load_videos()
    refresh()

def next_image():
    global current_image
    current_image = current_model.get_next_image(current_image)
    t_image.selection_set(current_image.number)
    show_image()

def prev_image():
    global current_image
    current_image = current_model.get_prev_image(current_image)
    t_image.selection_set(current_image.number)
    show_image()

def show_image():
    if current_image:
        image = current_image.image
    else:
        image = blank_image

    canvas.itemconfig(image_container, image=image)
    canvas_m.itemconfig(image_container_m, image=image)
    add_label_rectangles()
    add_label_rectangles_m()
    # print("Show image:", current_image.number)

def image_tree_changed(e):
    set_current_image()
    show_image()
    if current_image:
        v_image_name.set(current_image.name)
    else:
        v_image_name.set("No image")
    # refresh()

def set_current_image():
    global current_image
    x = t_image.selection()
    if len(x) == 0: number = 0
    else: number = int(x[0])
    current_image = current_model.get_image(number)


# Frame 3a
def refresh():
    current_model.write_labels_to_file()
    for tree in trees: update_tree(tree)
    add_label_rectangles()
    add_label_rectangles_m()
    v_label_name.set(current_label.name.replace("_", " ").title())
    # print("Available videos:", current_model.available_videos())
    v_video_name.set(current_model.available_videos())
    if current_image:
        v_image_name.set(current_image.name)
    print("Refresh:", current_image.number)


def add_label():
    MyLabel(name=e_name.get(), model=current_model, colour=e_colour.get(), width=int(v_label_w.get()), height=int(v_label_h.get()))
    refresh()

def update_label():
    current_label.name = e_name.get()
    current_label.colour = e_colour.get()
    current_label.width = int(v_label_w.get())
    current_label.height = int(v_label_h.get())
    refresh()

def remove_label():
    current_label.delete()
    refresh()

def spin_x_changed():
    current_label.width = int(s_label_w.get())
    current_label.model.write_labels_to_file()

def spin_y_changed():
    current_label.height = int(s_label_h.get())
    current_label.model.write_labels_to_file()

# Frame 3b
def add_model():
    Model(v_model_name.get())
    refresh()

def update_model():
    current_model.name = v_model_name.get()
    # current_model.train_path = v_train.get()
    # current_model.val_path = v_val.get()
    write_models_to_file()

def train_model():
    current_model.train()
    update_model_info()

def update_model_info():
    for count, text in enumerate([f"{current_model.train_time // timedelta(minutes=1)} min", f"{round(float(current_model.map50), 3) * 100}%", f"{round(float(current_model.map95), 3) * 100}%"], 2):
        Label(frame_3b1, text=str(text), pady=10, padx=10).grid(row=count, column=1, sticky=W)
    v_video_name.set(current_model.available_videos())

def remove_model():
    global current_model
    delete_model(current_model)
    current_model = models[0]
    refresh()
    # pass


# Main Page
root = ttk.Window(themename='darkly')
root.title("Neural Network Trainer")
root.geometry("1600x800+275+0")
blank_image = ImageTk.PhotoImage(Image.open("data/blank.png"))

# root.attributes("-fullscreen", True)

# Set up models
load_models()
current_model = models[0]
current_label = current_model.labels[0]

# Set up frames
side_width = 130
center_width = 1300

# Vertical Frames
frame_a = Frame(root, width=side_width, height=800)
frame_b = Frame(root, width=center_width, height=800)
frame_c = Frame(root, width=side_width, height=800)
frame_a.pack(side="left")
frame_b.pack(side="left")
frame_c.pack(side="left")

# Hortizontal Frames for center
frame_0 = Frame(frame_b, width=center_width, height=80, bg="blue", highlightbackground="white", highlightthickness=1)
frame_1 = Frame(frame_b, width=center_width, height=400, bg="white")
frame_2 = Frame(frame_b, width=center_width, height=80)
frame_3 = Frame(frame_b, width=center_width, height=320, highlightbackground="white", highlightthickness=1)
frame_0.pack()
frame_1.pack()
frame_2.pack()
frame_3.pack()

# Vertical Frames in 3
frame_0a = Frame(frame_0, width=center_width // 2)
frame_0b = Frame(frame_0, width=center_width // 2)
frame_0a.pack(side="left", padx=50)
frame_0b.pack(side="left", padx=50)

frame_3a = Frame(frame_3)
frame_3a1 = Frame(frame_3a)
frame_3a2 = Frame(frame_3a)
frame_3b = Frame(frame_3)
frame_3b1 = Frame(frame_3b)
frame_3b2 = Frame(frame_3b)
frame_3a.pack(side="left")
frame_3b.pack(side="left")
frame_3a1.pack(anchor=W)
frame_3a2.pack(side="bottom")
frame_3b1.pack(anchor=W)
frame_3b2.pack(side="bottom")

t_label = new_tree(heading="Label", frame=frame_a, height=10, width=150, command_if_changed=tree_changed_label)
t_model = new_tree(heading="Model", frame=frame_a, height=10, width=150, command_if_changed=tree_changed_model)

# Frame A - Delete mode checkbox
var_delete = StringVar(root)
cb_delete_mode = Checkbutton(frame_a, text="Delete", variable=var_delete, onvalue="Delete Mode", offvalue="Label Mode")
cb_delete_mode.pack()
var_delete.set('0')

# Frame 0 - Headings - Current Label and Current Image
v_label_name = tkinter.StringVar()
l_label_name = Label(frame_0a, textvariable=v_label_name, font="Calibri 24 bold")
l_label_name.pack(side="left")
v_image_name = tkinter.StringVar()
l_image_name = Label(frame_0b, textvariable=v_image_name, font="Calibri 24 bold")
l_image_name.pack(side="left")

# Frame 1 - Canvases
canvas = Canvas(frame_1, width=600, height=400, bg="white")
canvas.pack(side="left")
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Leave>', mouse_rectangle_clear)
canvas.bind('<Motion>', mouse_move)
canvas_m = Canvas(frame_1, width=600, height=400, bg="white")
canvas_m.pack(side="left")

# Frame 2 = Previous and Next Image Buttons
buttons = [("Video", load_videos), ("Previous", prev_image), ("Next", next_image), ("Copy", copy_modelled_labels)]
button_row(buttons, frame_2)

# Frame 3a - Labels
ttk.Label(frame_3a1, text="Labels", style="primary", font=('Helvetica', 12)).grid(row=0, column=0, sticky=N)
for text, column, row in [("Name", 0, 1), ("Colour", 0, 2), ("Width", 2, 1), ("Height", 2, 2)]:
    ttk.Label(frame_3a1, text=text, padding=10).grid(row=row, column=column)
v_label_w = IntVar(root)
v_label_h = IntVar(root)
e_name = Entry(frame_3a1)
e_colour = Entry(frame_3a1)
s_label_w = Spinbox(frame_3a1, from_=5, to=100, increment=5, textvariable=v_label_w, command=spin_x_changed, width=6)
s_label_h = Spinbox(frame_3a1, from_=5, to=100, increment=5, textvariable=v_label_h, command=spin_y_changed, width=6)
e_name.grid(row=1, column=1)
e_colour.grid(row=2, column=1)
s_label_w.grid(row=1, column=3)
s_label_h.grid(row=2, column=3)
buttons = [("Add Label", add_label), ("Update Label", update_label), ("Remove Label", remove_label)]
button_row(buttons, frame_3a2)

# Frame 3b - Model
ttk.Label(frame_3b1, text="Models", style="primary", font=('Helvetica', 12)).grid(row=0, column=0)
for count, text in enumerate(["Name:", "Training time:", "Map50:", "Map95:"], 1):
    Label(frame_3b1, text=text, pady=10, padx=10).grid(row=count, column=0, sticky=W)

v_model_name = StringVar(root)
e_model_name = Entry(frame_3b1, textvariable=v_model_name)
e_model_name.grid(row=1, column=1)
v_model_name.set(current_model.name)

buttons = [("Add Model", add_model), ("Train Model", train_model), ("Remove Model", remove_model)]
button_row(buttons, frame_3b2)

# Frame C - Images
v_video_name = StringVar(root, value=current_model.available_videos())
Label(frame_c, textvariable=v_video_name, pady=10).pack()

if len(current_model.images) > 0:
    current_image = current_model.images[0]
else:
    current_image = None

f_image_tree = Frame(frame_c)
f_image_tree.pack(pady=10)
s_image_tree = Scrollbar(f_image_tree)
s_image_tree.pack(side=RIGHT, fill=Y)

t_image = ttk.Treeview(f_image_tree, height=350, yscrollcommand=s_image_tree.set, selectmode="extended")
s_image_tree.config(command=t_image.yview)
t_image['columns'] = ("Name", "Labels")
t_image.column("#0", width=0, minwidth=0)
t_image.column("Name", anchor=W, width=65)
t_image.column("Labels", anchor=W, width=60)
t_image.heading("#0", text="")
t_image.heading("Name", text="File", anchor=W)
t_image.heading("Labels", text="Labels", anchor=W)
# update_tree_images()
t_image.pack()
t_image.tag_configure("oddrow", background="white")
t_image.tag_configure("evenrow", background="lightblue")
t_image.bind('<<TreeviewSelect>>', image_tree_changed)
t_image.tag_configure("red", background="red")
t_image.tag_configure("blue", background="blue")

def key_stroke(e):
    global v_label_w, v_label_h
    if e.char == "q": v_label_h.set(v_label_h.get() + 1)
    if e.char == "a": v_label_h.set(v_label_h.get() - 1)
    if e.char == ".": v_label_w.set(v_label_w.get() + 1)
    if e.char == ",": v_label_w.set(v_label_w.get() - 1)
    if e.char in ["q", "a", ",", "."]:
        spin_y_changed()
        spin_x_changed()
        x, y = root.winfo_pointerxy()
        x0, y0 = canvas.winfo_rootx(), canvas.winfo_rooty()
        draw_mouse_rectangle(x - x0, y - y0)
    if e.keysym == "Down": next_image()
    if e.keysym == "Up": prev_image()

def close_win(e):
    root.destroy()


# Keystrokes
root.bind('<KeyPress>', key_stroke)

root.bind('<Escape>', lambda e: close_win(e))

# Create image container
image_container = canvas.create_image(0, 0, anchor="nw")
image_container_m = canvas_m.create_image(0, 0, anchor="nw")
# image_container = canvas.create_image(0, 0, anchor="nw", image=current_image.image)
# image_container_m = canvas_m.create_image(0, 0, anchor="nw", image=current_image.image)

# Set the current label and populate entry fields
set_current_label()
write(e_name, current_label.name)
write(e_colour, current_label.colour)
v_label_w.set(current_label.width)
v_label_h.set(current_label.height)

update_model_info()
refresh()

# root.style.theme_use("litera")

# Sandpit Area

# Main loop
root.mainloop()