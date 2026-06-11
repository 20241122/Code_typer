from tkinter import *
import random

# 문제
problem = {
    "문제1" : {
        """"number = int(input("숫자를 입력하세요: "))""" : 1,
        """"if number % 2 == 0:""" : 1,
        """"print("짝수입니다!")""" : 1,
        """"else:""" : 1,
        """"print("홀수입니다!")""": 1
    },

    "문제2" : {
        """"import random""" : 1,
        """"menu = ["떡볶이", "마라탕", "햄버거", "돈가스", "짜장면"]""" : 1,
    "   """"today_pick = random.choice(menu)""" :1,
        """"print("오늘 추천 메뉴는 바로 [" + today_pick + "] 입니다!")""": 1
    },

    "문제3" : {
         """import time""" : 1,
         """for i in [3, 2, 1]:""" : 1,
         """print(i)""" : 1,
         """time.sleep(1)""" : 1,
         """print("로켓 발사!!")""" : 1
    },
}

    """""import time
for i in [3, 2, 1]:
print(i)
time.sleep(1)
print("로켓 발사!!")""""": 1
}
    
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

    entry_input.delete(0, END)
    
    if user_typed == current_problem:
        total_characters += len(user_typed)
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

    label_result_min = Label(result_time_frame, text=f"{timer_min}분")
    label_result_min.pack(side="left")

    label_result_sec = Label(result_time_frame, text=f"{timer_sec}초")
    label_result_sec.pack(side="left")

    #결과창용 타수 표시 프레임
    label_result_CPM = Label(result_frame, text=f"타수: {CPM}")
    label_result_CPM.pack()

    
# 스톱워치
timer = 0
timer_min = 0
timer_sec = 0

def stopwatch():
    global timer, timer_min, timer_sec

    if running == False:
        return 0;

    timer += 1
    if timer >= 60:
        timer_min = timer // 60
        timer_sec = timer % 60
    else:
        timer_sec = timer

    label_stopwatch_min.config(text=f"{timer_min}분")
    label_stopwatch_sec.config(text=f"{timer_sec}초")

    CPM_calcuate()

    root.after(1000, stopwatch)

# 타수 계산
CPM = 0
total_characters = 0

def CPM_calcuate():
    global CPM, total_characters

    if timer <= 0:
        CPM = 0
        label_CPM.config(text="타수: 0")
        return 0;
    
    current_problem = label_problem.cget("text")
    user_typed = entry_input.get()
    current_characters = len(user_typed)
    
    correct_characters = 0
    
    for i in range(current_characters, 0, -1):
        if current_problem[:i] == user_typed[:i]:
            correct_characters = i
            break
    
    CPM = ((total_characters + correct_characters) * 60) // timer
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
entry_input = Entry(practice_frame, font=("Courier New", 14), width=40)
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