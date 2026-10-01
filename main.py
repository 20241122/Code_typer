from tkinter import *
import pracitce_key
import practice_word
import practice_code
import challenge
import option


def show_practice_key():
    main_frame.pack_forget()
    code_frame.pack()
    
    practice_code.game_start() 

def show_practice_word():
    main_frame.pack_forget()
    code_frame.pack()
    
    practice_code.game_start() 

def show_practice_code():
    main_frame.pack_forget()
    code_frame.pack()
    
    practice_code.game_start() 

def show_challenge():
    main_frame.pack_forget()
    challenge_frame.pack()
    
    challenge.main_menu() 

def show_option():
    main_frame.pack_forget()
    challenge_frame.pack()
    
    challenge.main_menu() 

def game_():
    main_frame.pack_forget()
    challenge_frame.pack()
    
    challenge.main_menu() 

# 1. 윈도우 창 설정
root = Tk()
root.title("코딩 타자 연습")
root.geometry("550x550")

# 2. 메인 화면
main_frame = Frame(root)
main_frame.pack()

Label(main_frame, text="코딩 타자 연습", font=("Malgun Gothic", 25, "bold")).pack(pady=60)
Button(main_frame, text="자리 연습", font=("Malgun Gothic", 15), width=15, height=2, command=show_practice_code).pack(pady=10)
Button(main_frame, text="단어 연습", font=("Malgun Gothic", 15), width=15, height=2, command=show_practice_code).pack(pady=10)
Button(main_frame, text="단문 연습", font=("Malgun Gothic", 15), width=15, height=2, command=show_practice_code).pack(pady=10)
Button(main_frame, text="챌린지 모드", font=("Malgun Gothic", 15), width=15, height=2, command=show_challenge).pack(pady=10)
Button(main_frame, text="환경 설정", font=("Malgun Gothic", 15), width=15, height=2, command=show_challenge).pack(pady=10)
Button(main_frame, text="게임 종료", font=("Malgun Gothic", 15), width=15, height=2, command=show_challenge).pack(pady=10)

code_frame = practice_code.create_frame(root)
challenge_frame = challenge.create_frame(root)

# 프로그램 실행
root.mainloop()