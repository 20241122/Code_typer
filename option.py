from tkinter import *


# ==========================================
# @. 메인 화면 프레임
# ==========================================

# 4-1. 
def create_frame(parent_window):

    main_window = parent_window
    container = Frame(parent_window)

    practice_frame = Frame(container)
    practice_frame.pack()

    # 
    label_help = Label(practice_frame, text="")
    label_help.pack(pady=20)
    label_help.config(text="챌린지 모드", width=40, height=5, font=("Consolas", 15, "bold"), anchor="center")

    #
    label_help = Label(practice_frame, text="")
    label_help.pack(pady=20)
    label_help.config(text="원하는 레벨을 선택하세요.", fg="black")

    #레벨 표시
     

    #mainmenuButton = Button(practice_frame, text="메인 메뉴로", command=show_main)
    #mainmenuButton.pack()

    return container


