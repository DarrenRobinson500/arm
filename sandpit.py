import ttkbootstrap as ttk
from ttkbootstrap.constants import *

win = ttk.Window()

themes = win.style.theme_names()
current_theme = win.style.theme_use()

print(themes)
print(current_theme)
