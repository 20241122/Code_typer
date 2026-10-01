# ==========================================
# 1. 라이브러리
# ==========================================
from tkinter import *

# ==========================================
# 2. 프레임
# ==========================================

# 4-1. 
def create_frame(parent_window):
    global main_window, practice_frame, result_frame, container

    main_window = parent_window
    container = Frame(parent_window)

    option_frame = Frame(container)
    option_frame.pack()