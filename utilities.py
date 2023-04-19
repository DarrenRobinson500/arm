import ttkbootstrap as ttk
import tkinter
from tkinter import *
import cv2
from PIL import Image, ImageTk
from PIL import Image, ImageTk


trees = []

def button_row(buttons, frame):
    for text, command in buttons:
        new_button = ttk.Button(frame, text=text, command=command, width=13)
        new_button.pack(side="left", padx=5, pady=5)

def write(widget, text):
    widget.delete(0, END)
    widget.insert(0, text)

def new_tree(heading, frame, height, width, command_if_changed):
    f_tree = Frame(frame)
    f_tree.pack(pady=10, padx=10)
    s_tree = Scrollbar(f_tree)
    s_tree.pack(side=RIGHT, fill=Y)
    tree = ttk.Treeview(f_tree, height=height, yscrollcommand=s_tree.set, selectmode="extended")
    s_tree.config(command=tree.yview)
    tree['columns'] = ("Name")
    tree.column("#0", width=0, minwidth=0)
    tree.column("Name", anchor=W, width=width)
    tree.heading("#0", text="")
    tree.heading("Name", text=heading, anchor=W)
    tree.pack()
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("evenrow", background="lightblue")
    tree.bind('<<TreeviewSelect>>', command_if_changed)
    trees.append(tree)
    return tree

