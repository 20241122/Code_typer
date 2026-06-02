from tkinter import *
import random

# 문제
problem = [
    """number = int(input("숫자를 입력하세요: "))
if number % 2 == 0:
print("짝수입니다!")
else:
print("홀수입니다!")""",

    """import random
menu = ["떡볶이", "마라탕", "햄버거", "돈가스", "짜장면"]
today_pick = random.choice(menu)
print("오늘 추천 메뉴는 바로 [" + today_pick + "] 입니다!")""",

    """import time
for i in [3, 2, 1]:
print(i)
time.sleep(1)
print("로켓 발사!!")"""
]

def next_question():
    # 입력창 비우기
    entry_input.delete(0, END)

    # 결과 메시지 초기화
    label_result.config(text="타자를 입력하고 [Enter]를 누르세요.", fg="black")
    
    # 랜덤 문제 뽑기
    target_problem = random.choice(problem)

    # 예문 한 줄 분리
    word = target_problem.splitlines()

    # 한 줄 랜덤 뽑기
    target_text = random.choice(word)
    label_problem.config(text=target_text)

def check_answer():
    current_problem = label_problem.cget("text")
    user_typed = entry_input.get()

    global total_characters
    total_characters += len(user_typed)
    
    if user_typed == current_problem:
        label_result.config(text="O 정답!", fg="green")
        correct_count()
    else:
        label_result.config(text="X 오타가 있습니다.", fg="red")
        root.after(1000, next_question)

# 정답 카운트
running = True
correct = 0
def correct_count():
    global correct
    correct += 1

    global running

    label_count.config(text=f"맞힌 개수: {correct}")

    CPM_calcuate()

    # 10개 이상 맞췄을 시 결과창 표시
    if correct >= 2:
        running = False
        result_window()
    else:
        root.after(1000, next_question)

# 결과창 표시
def result_window():
    entry_input.unbind("<Return>")

    practice_frame.pack_forget()
    result_frame.pack()

    thanks = Label(result_frame, text="연습 결과", width=40, height=5, font=("Consolas", 15, "bold"), anchor="center")
    thanks.pack()

    # 결과창용 시간 표시 프레임
    result_time_frame = Frame(result_frame)
    result_time_frame.pack()
    
    label_time = Label(result_time_frame, text="소요 시간: ")
    label_time.pack(side="left")

    label_res_min = Label(result_time_frame, text=f"{min}분")
    label_res_min.pack(side="left")

    label_res_sec = Label(result_time_frame, text=f"{sec}초")
    label_res_sec.pack(side="left")

    #타수 표시
    label_CPM = Label(result_frame, text=f"타수: {CPM}")
    label_CPM.pack()
    
# 스톱워치
timer = 0
min = 0
sec = 0

def stopwatch():
    global timer
    global min
    global sec

    timer += 1
    if timer >= 60:
        min = timer // 60
        sec = timer % 60
    else:
        sec = timer

    label_stopwatch_min.config(text=f"{min}분")
    label_stopwatch_sec.config(text=f"{sec}초")

    if running == False:
        ()
    else:
        root.after(1000, stopwatch)

# 타수
CPM = 0
total_characters = 0

def CPM_calcuate():
    global CPM
    global total_characters

    if timer <= 0:
        CPM = 0
    else:
        CPM = (total_characters * 60) // timer

    label_CPM.config(text=f"타수: {CPM}")

#화면 구성
root = Tk()

#연습모드 프레임
practice_frame = Frame(root)
practice_frame.pack()

#결과창 프레임
result_frame = Frame(root)

root.title("코딩 타자 연습")
root.geometry("500x300")

# 문제 표시 영역
label_problem = Label(practice_frame, text="", width=40, height=5, font=("Consolas", 15, "bold"), anchor="center")
label_problem.pack()

# 사용자 입력 영역
entry_input = Entry(practice_frame, font=("CourierNew", 14), width=40)
entry_input.pack()

entry_input.bind("<Return>", lambda event: check_answer())

# 오타 여부 표시
label_result = Label(practice_frame, text="")
label_result.pack(pady=20)

# 맞힌 개수 표시
label_count = Label(practice_frame, text="맞힌 개수: 0")
label_count.pack()

# 시간 표시
frame_time = Frame(practice_frame)
frame_time.pack()

label_time = Label(frame_time, text="소요 시간:")
label_time.pack(side="left")

label_stopwatch_min = Label(frame_time, text="0분")
label_stopwatch_min.pack(side="left")

label_stopwatch_sec = Label(frame_time, text="0초")
label_stopwatch_sec.pack(side="left")
root.after(1000, stopwatch)

#타수 표시
label_CPM = Label(practice_frame, text="타수: 0")
label_CPM.pack()

# 프로그램 시작
next_question()
root.mainloop()