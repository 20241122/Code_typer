# ==========================================
# 1. 라이브러리, 문제
# ==========================================
from tkinter import *
from tkinter.font import *
import random 
import time

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import font_manager, rc
from matplotlib.figure import Figure

import keyboard
import keyboardlayout as kl
import keyboardlayout.tkinter as klt

rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

# 문제
problem = {
    "문제1" : {
        """print("Hello, World!")""" : 1,
    },
}

# ==========================================
# 2. 전역 변수
# ==========================================

running = True
correct = 0 #정답 개수

timer = 0
timer_min = 0
timer_sec = 0

CPM = 0 #타수
total_characters = 0
correct_characters = 0

accuracy = 100 #정확도
current_total_characters = 0
incorrect_characters = 0

backspace_count = 0 #백스페이스 누른 횟수
backspace_ratio = 100

last_char = ""       # 방금 전 쳤던 글자
last_time = 0.0      # 방금 전 글자를 친 시간
case_switch_times = [] # 대/소문자 변환에 걸린 시간들을 모아둘 리스트

key_count = {
    'q': 0, 'w': 0, 'e': 0, 'r': 0, 't': 0, 'y': 0, 'u': 0, 'i': 0, 'o': 0, 'p': 0,
    'a': 0, 's': 0, 'd': 0, 'f': 0, 'g': 0, 'h': 0, 'j': 0, 'k': 0, 'l': 0,
    'z': 0, 'x': 0, 'c': 0, 'v': 0, 'b': 0, 'n': 0, 'm': 0,
    'space': 0, 'backspace': 0
}

incorrect_key_count = {
    'q': 0, 'w': 0, 'e': 0, 'r': 0, 't': 0, 'y': 0, 'u': 0, 'i': 0, 'o': 0, 'p': 0,
    'a': 0, 's': 0, 'd': 0, 'f': 0, 'g': 0, 'h': 0, 'j': 0, 'k': 0, 'l': 0,
    'z': 0, 'x': 0, 'c': 0, 'v': 0, 'b': 0, 'n': 0, 'm': 0,
    'space': 0, 'backspace': 0
}

correct_key_count = {
    'q': 0, 'w': 0, 'e': 0, 'r': 0, 't': 0, 'y': 0, 'u': 0, 'i': 0, 'o': 0, 'p': 0,
    'a': 0, 's': 0, 'd': 0, 'f': 0, 'g': 0, 'h': 0, 'j': 0, 'k': 0, 'l': 0,
    'z': 0, 'x': 0, 'c': 0, 'v': 0, 'b': 0, 'n': 0, 'm': 0,
    'space': 0, 'backspace': 0
}


max_count = 0 #key_count의 최댓값
key_percentages = 0 #key_count의 최댓값에 대한 비율

key_color_incorrect = None #오타 히트맵에서 보일 키의 색상코드
key_color_correct = None #정답 히트맵에서 보일 키의 색상코드

    #히트맵 레이아웃
popup = None
keyboard_layout = None
key_info = None
keyboard_info = None
letter_key_size = None
layout_name = None

# ==========================================
# 3. 함수 모음
# ==========================================

# 3-0. 게임 스타트(메인-> 단문 연습)
def game_start():
    global start_time
    start_time = time.time()
    restart()

# 3-1. 스톱워치
def stopwatch():
    global timer, real_time, timer_min, timer_sec

    if running == False:
        return 0;

    timer += 1
    real_time = timer // 10

    if real_time >= 60:
        timer_min = real_time // 60
        timer_sec = real_time % 60
    else:
        timer_sec = real_time

    label_stopwatch_min.config(text=f"{timer_min}분")
    label_stopwatch_sec.config(text=f"{timer_sec}초")

    CPM_calcuate()
    accuracy_calcuate()
    check_input_len()
    container.after(100, stopwatch)

# 3-2. 다음 문제 내기
def next_question():
    global target_problem, target_line

    # 입력창 비우기
    entry_input.delete("1.0", END)

    # 결과 메시지 초기화
    label_help.config(text="타자를 입력하고 [Enter] 또는 [Space]를 누르세요.", fg="black")
    
    # 랜덤 문제 뽑기
    target_problem = random.choice(list(problem.keys()))

    # 문제의 문장 가져오기
    target_problem_lines = problem[target_problem]

    # 가중치 리스트와 문장 리스트 뽑기
    lines = list(target_problem_lines.keys())
    weights = list(target_problem_lines.values())

    # 가중치 높은 문장 뽑기
    target_line = random.choices(lines, weights=weights, k=1)[0]

    label_problem.config(text=target_line)

# 3-3. 입력 확인
def check_answer():
    user_typed = entry_input.get("1.0", "end-1c")

    global total_characters
    
    if user_typed == target_line:
        total_characters += len(user_typed)
        label_help.config(text="O 정답!", fg="green")
        correct_count()
        entry_input.delete("1.0", END)
    else:
        label_help.config(text="X 오타가 있습니다.", fg="red")
        label_help.after(1000, lambda: label_help.config(text="타자를 입력하고 [Enter] 또는 [Space]를 누르세요.", fg="black"))
        problem[target_problem][target_line] += 1

        return "break"

# 3-4. 정답 카운트
def correct_count():
    global correct, running
    correct += 1

    label_count.config(text=f"맞힌 개수: {correct}")

    # 10개 이상 맞췄을 시 결과창 표시
    if correct >= 1:
        running = False
        result_window()
        keyboard.unhook_all() 
    else:
        container.after(100, next_question)

    
# 3-5. 타수 계산
def CPM_calcuate():
    global CPM, total_characters, correct_characters
    if timer <= 0:
        CPM = 0
        label_CPM.config(text="타수: 0")
        return 0
    
    current_problem = label_problem.cget("text")
    user_typed = entry_input.get("1.0", "end-1c")
    current_characters = len(user_typed)

    for i in range(current_characters, -1, -1):
        if current_problem[:i] == user_typed[:i]:
            correct_characters = i
            break

    CPM = ((total_characters + correct_characters) * 600) // timer
    label_CPM.config(text=f"타수: {CPM}")

# 3-6. 정확도 계산
def accuracy_calcuate():
    global accuracy, current_total_characters, incorrect_characters

    if timer < 0:
        accuracy = 100
        label_accuracy.config(text=f"정확도: 100.0%")
        return 100
    
    user_typed = entry_input.get("1.0", "end-1c")
    current_total_characters = len(user_typed)
    
    if current_total_characters == 0:
        accuracy = 100
        label_accuracy.config(text=f"정확도: {accuracy:.1f}%")
        return 100

    accuracy = ((correct_characters/current_total_characters) * 100)
    
    if accuracy < 0:
        accuracy = 0

    label_accuracy.config(text=f"정확도: {accuracy:.1f}%")

    if timer <= 0 :
        incorrect_characters = 0
    else: incorrect_characters = current_total_characters - correct_characters

    

    label_typo.config(text=f"오타: {incorrect_characters}")

# 3-7. 백스페이스 횟수 추적
def backspace_count_up():
    global backspace_count
    backspace_count += 1

# 3-8. 백스페이스 비율 계산
def backspace_ratio_calcuate():
    global backspace_ratio

    if total_characters == 0:
        backspace_ratio = 100
        return 100

    backspace_ratio = 100 - (backspace_count / total_characters) * 100

    if backspace_ratio < 0:
        backspace_ratio = 0
        return 0


# 3-9. 대소문자 딜레이 감지(작성중)
def measure_shift_delay(event):
    global last_char, last_time, case_switch_times

    char = event.char
    keysym = event.keysym
    current_time = time.time()

    if keysym in ['Shift_L', 'Shift_R', 'Caps_Lock', 'Control_L', 'Alt_L']:
        return

    target_text = label_problem.cget("text")
    user_typed = entry_input.get("1.0", "end-1c")

    if target_text.startswith(user_typed):
        expected_index = len(user_typed)

        if expected_index < len(target_text) and char == target_text[expected_index]:
            if char.isalpha():
                if last_char and last_char.isalpha():
                    if (last_char.islower() and char.isupper()) or (last_char.isupper() and char.islower()):
                        delay = current_time - last_time
                        case_switch_times.append(delay)
                        print(f"{last_char} -> {char}. 딜레이: {delay:.3f}초")
                
                last_char = char 
                last_time = current_time
            else:
                # 공백이나 특수기호를 칠 때
                last_char = ""
                last_time = current_time
        else:
            # 오타를 낸 경우
            last_char = ""
    else:
        # 오타를 내고 문자를 밀려 쓸 경우
        last_char = ""

# 3-10. 오타 표시하기
def typo_marking():
    global correct_characters

    entry_input.tag_remove("typo", "1.0", END)

    # 문제 가져오기
    current_problem = label_problem.cget("text")
    user_typed = entry_input.get("1.0", "end-1c")
    current_characters = len(user_typed)

    for i in range(current_characters, -1, -1):
        if current_problem[:i] == user_typed[:i]:
            correct_characters = i
            break
        else:
            entry_input.tag_add("typo", f"1.{i}", f"1.{i+1}")

# 3-11. 사용자가 입력한 글자수 추적
def check_input_len():
    global target_problem, target_line

    current_problem = label_problem.cget("text")
    user_typed = entry_input.get("1.0", "end-1c")

    if  len(user_typed) > len(current_problem):
        label_help.config(text="X 글자 수를 초과하여 다음 문제로 넘어갑니다.", fg="red")
        label_help.after(1000, lambda: label_help.config(text="타자를 입력하고 [Enter] 또는 [Space]를 누르세요.", fg="black"))
        problem[target_problem][target_line] += 1

        entry_input.delete("1.0", END)
        next_question()

# 3-12. 사용자가 입력한 키 추적(작성중)
def count_input_key(event):
    global key_count

    #방금 누른 키보드의 글자나 키 이름 가져오기
    char = event.char.lower()  # 알파벳(a~z, A~Z)은 모두 소문자로 통일해서 가져옴
    keysym = event.keysym.lower() # 스페이스바, 백스페이스 같은 특수키의 이름 가져옴

    #방금 누른 키가 딕셔너리에 있다면 숫자 1 증가시키기
    if char in key_count:
        key_count[char] += 1
        print(f"[{char}] 키 / 누적: {key_count[char]}번") # 테스트용 출력
        
    elif keysym == 'space':
        key_count['space'] += 1
        
    elif keysym == 'backspace':
        key_count['backspace'] += 1

# 3-13. 입력된 키가 오타면 눌린 횟수 카운트하기(작성중)
def count_incorrect_key(event):

    current_problem = label_problem.cget("text")
    user_typed = entry_input.get("1.0", "end-1c")

    #방금 누른 키보드의 글자나 키 이름 가져오기
    char = event.char.lower()  # 알파벳(a~z, A~Z)은 모두 소문자로 통일해서 가져옴
    keysym = event.keysym.lower() # 스페이스바, 백스페이스 같은 특수키의 이름 가져옴

    #방금 누른 키가 오타면 1 증가시키기
    if char in incorrect_key_count:
        incorrect_key_count[char] += 1
        print(f"[{char}] 키 / 누적: {incorrect_key_count[char]}번") # 테스트용 출력
        
    elif keysym == 'space':
        key_count['space'] += 1
        
    elif keysym == 'backspace':
        key_count['backspace'] += 1

# 3-14. 입력된 키가 정답이면 그 수를 카운트하기(작성중)
def count_correct_key(event):
    current_problem = label_problem.cget("text")
    user_typed = entry_input.get("1.0", "end-1c")

    #방금 누른 키보드의 글자나 키 이름 가져오기
    char = event.char.lower()  # 알파벳(a~z, A~Z)은 모두 소문자로 통일해서 가져옴
    keysym = event.keysym.lower() # 스페이스바, 백스페이스 같은 특수키의 이름 가져옴

    #방금 누른 키가 오타면 1 증가시키기
    if char in correct_key_count:
        correct_key_count[char] += 1
        print(f"[{char}] 키 / 누적: {correct_key_count[char]}번") # 테스트용 출력
        
    elif keysym == 'space':
        key_count['space'] += 1
        
    elif keysym == 'backspace':
        key_count['backspace'] += 1
    print("정답입니다! 현재 누른 수: %d", )

# 3-15. 키 딕셔너리에서 최댓값 찾기
def max_key_count():
    max_key = max(key_count.values())
    max_count = key_count[max_key]
    print(max_key, max_count) 

    return max_count

# 3-16. 최댓값에 대한 비율 구하기
def key_count_percentages():
    max_count = max_key_count()
    key_percentages = {}

    for key, count in key_count.items():
        if max_count == 0:
            key_percentages[key] = 0.0
        
    # (이번 키 누른 횟수 /어떤 키를 제일 많이 누른 횟수) * 100
        else:
            key_percentages[key] = (count / max_count) * 100

    return key_percentages


# 3-18. 히트맵에 나타낼 키의 색상값을 구하기
def heatmap_incorrect_color(percentage):
    red = 255
    green = int(255 * (100 - percentage) / 100)
    blue = int(255 * (100 - percentage) / 100)

    key_color_incorrect = f"#{red:02x}{green:02x}{blue:02x}"

    return key_color_incorrect

# 3-13. 차트 그리기
def drawing_chart(result_frame):

    for widget in result_frame.winfo_children():
        widget.destroy()

    categories = ['타수', 'backspace 비율', '대/소문자 전환 시간']
    N = len(categories)

    # 각도 설정 
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1] 

    # 데이터 값
        #cpm
    CPM_score = min((CPM / 330) * 100, 100)

        #backspace 비율
    backspace_ratio_calcuate()

        #대/소문자 변환 시간
    if case_switch_times:
        avg_delay = sum(case_switch_times) / len(case_switch_times)
    else:
        avg_delay = 0

    shift_score = max(0, min(100, (1.0 - avg_delay) / 0.7 * 100))

    values = [CPM_score, backspace_ratio, shift_score]
    values += values[:1]

    fig = Figure(figsize=(4, 4))
    ax = fig.add_subplot(111, polar=True)
    
    ax.plot(angles, values, color='blue', linewidth=2, linestyle='solid')
    ax.fill(angles, values, color='blue', alpha=0.25)

    for i in range(N):
        angle_rad = angles[i]
        val = values[i]
        
        if i == 0:
            raw_text = f"({CPM}/280)"
        elif i == 1:
            raw_text = f"({backspace_count}번)"
        elif i == 2:
            raw_text = f"({avg_delay:.2f}초/0.3초)"
            
        label_text = f"{val:.1f}점\n{raw_text}"
        
        ax.text(angle_rad, val + 15, label_text, ha='center', va='center', fontsize=10, fontweight='bold')

    avg_score = ( CPM_score + backspace_ratio + shift_score ) / 3

    ax.set_title("결과 그래프", fontsize=10, loc='left')
    ax.text(1.2, 0.01, "총 점수" + f"\n{avg_score:.1f}점", verticalalignment='bottom', horizontalalignment='right',   transform=ax.transAxes, fontsize=10)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')

    ax.set_ylim(0, 125)

    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], color="grey", size=8)

    ax.text
    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# 3-14. 히트맵 표시(작성중)
def show_heatmap():
    global popup, keyboard_frame, keyboard_layout

    popup = Toplevel(main_window)
    popup.title("히트맵")
    popup.geometry("950x400")

    popup.resizable(False, False)

    keyboard_frame = Frame(popup)
    keyboard_frame.pack(expand=True, fill='both', padx=20, pady=10)

    heatmap_button_frame = Frame(popup)
    heatmap_button_frame.pack(pady=10)

    layout_name = kl.LayoutName.QWERTY
    key_size = 60
    grey = '#bebebe'
    black = '#000000'

    keyboard_info = kl.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=black
    )

    key_info = kl.KeyInfo(
        margin=10,
        color=grey,
        txt_color=black,
        txt_font=Font(family='Arial', size=key_size//6),
        txt_padding=(key_size//6, key_size//10)
    )

    letter_key_size = (key_size, key_size)
    keyboard_layout = klt.KeyboardLayout(
        layout_name,
        keyboard_info,
        letter_key_size,
        key_info,
        master=keyboard_frame
    )

    keyboard_layout.pack(expand=True, fill='both', padx=20, pady=20)

    heatmap_Button_incorrect = Button(heatmap_button_frame, text="정답", command=pop_correct)
    heatmap_Button_incorrect.pack(side="left")

    heatmap_Button_incorrect = Button(heatmap_button_frame, text="오타", command=pop_incorrect)
    heatmap_Button_incorrect.pack(side="left")

#3-15. 히트맵 정답 표시(작성중)
def pop_correct():
    global popup, keyboard_layout, key_info, layout_name, keyboard_info, letter_key_size

    if keyboard_layout:
        keyboard_layout.destroy()
        keyboard_frame.update()

    layout_name = kl.LayoutName.QWERTY
    key_size = 60
    grey = '#bebebe'
    black = '#000000'

    keyboard_info = kl.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=grey
    )

    key_info = kl.KeyInfo(
        margin=10,
        color=grey,
        txt_color=black,
        txt_font=Font(family='Arial', size=key_size//6),
        txt_padding=(key_size//6, key_size//10)
    )

    letter_key_size = (key_size, key_size)
    keyboard_layout = klt.KeyboardLayout(
        layout_name,
        keyboard_info,
        letter_key_size,
        key_info,
        master=keyboard_frame
    )

    keyboard_layout.pack(expand=True, fill='both', padx=20, pady=20)

    print("히트맵 변경 정상적으로 바뀜!(정답)")

#3-16. 히트맵 오답 표시(작성중)
def pop_incorrect():
    global popup, keyboard_layout, key_info, layout_name, keyboard_info, letter_key_size

    if keyboard_layout:
        keyboard_layout.destroy()
        keyboard_frame.update()

    layout_name = kl.LayoutName.QWERTY
    key_size = 60
    black = '#000000'

    keyboard_info = kl.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=black
    )

    key_info = kl.KeyInfo(
        margin=10,
        color=key_color_incorrect,
        txt_color=black,
        txt_font=Font(family='Arial', size=key_size//6),
        txt_padding=(key_size//6, key_size//10)
    )

    letter_key_size = (key_size, key_size)
    keyboard_layout = klt.KeyboardLayout(
        layout_name,
        keyboard_info,
        letter_key_size,
        key_info,
        master=keyboard_frame
    )

    keyboard_layout.pack(expand=True, fill='both', padx=20, pady=20)

    print("히트맵 변경 정상적으로 바뀜!(오타)")

# 3-15. 결과창 표시
def result_window():
    entry_input.unbind("<Return>")

    practice_frame.pack_forget()
    result_frame.pack()

    label_result_min.config(text=f"{timer_min}분")
    label_result_sec.config(text=f"{timer_sec}초")
    label_result_CPM.config(text=f"타수: {CPM}")
    label_result_accuracy.config(text=f"정확도: {accuracy}")

    drawing_chart(chart_frame)
    max_key_count() #테스트


# 3-16. 다시하기
def restart():
    global correct, timer, timer_sec, timer_min, accuracy, running, total_characters, CPM, correct_characters, current_total_characters, incorrect_characters, last_char, case_switch_times
    # 변수 초기화
    running = True
    correct = 0

    timer = 0
    timer_min = 0
    timer_sec = 0

    CPM = 0
    total_characters = 0
    correct_characters = 0

    accuracy = 100
    current_total_characters = 0
    incorrect_characters = 0

    last_char = ""
    case_switch_times.clear()

    # 화면 초기화
    label_count.config(text="맞힌 개수: 0")
    label_CPM.config(text="타수: 0")
    label_accuracy.config(text=f"정확도: 100.0%")
    label_typo.config(text=f"오타: 0")
    label_stopwatch_min.config(text="0분")
    label_stopwatch_sec.config(text="0초")

    # 프레임 전환
    result_frame.pack_forget()
    practice_frame.pack()

    entry_input.bind("<Return>", lambda event: check_answer())

    next_question()
    container.after(100, stopwatch)

# 3-17. 메인 메뉴로(작성중)
def show_main():
    global correct, timer, timer_sec, timer_min, accuracy, running, total_characters, CPM, correct_characters, current_total_characters, incorrect_characters

    result_frame.pack_forget()

    # 변수 초기화
    running = True
    correct = 0
    
    timer = 0
    timer_min = 0
    timer_sec = 0
    
    CPM = 0
    total_characters = 0
    correct_characters = 0
    
    accuracy = 100
    current_total_characters = 0
    incorrect_characters = 0

# ==========================================
# 4. 타자연습 실행 프레임
# ==========================================

# 4-1. 
def create_frame(parent_window):
    global main_window, practice_frame, result_frame, container
    global label_count, label_problem, entry_input, label_help
    global label_CPM, label_accuracy, label_typo
    global label_stopwatch_min, label_stopwatch_sec
    global label_result_min, label_result_sec, label_result_CPM, label_result_accuracy
    global chart_frame

    main_window = parent_window
    container = Frame(parent_window)

    practice_frame = Frame(container)
    practice_frame.pack()

    # 4-2. 맞힌 개수 표시
    label_count = Label(practice_frame, text="맞힌 개수: 0", anchor="e")
    label_count.pack()

    # 4-3. 문제 표시 영역
    label_problem = Label(practice_frame, text="", width=40, height=5, font=("Consolas", 15, "bold"), anchor="center")
    label_problem.pack()

    # 4-4. 사용자 입력 영역
    entry_input = Text(practice_frame, font=("Courier New", 13), width=40, height=1)
    entry_input.pack()

    entry_input.bind("<Return>", lambda event: check_answer())
    entry_input.bind("<KeyRelease>", lambda event: (accuracy_calcuate(), typo_marking(), check_input_len()))
    entry_input.bind("<KeyPress>", measure_shift_delay, add="+")
    entry_input.bind("<KeyPress>", count_input_key, add="+")

    keyboard.add_hotkey('backspace', backspace_count_up)


    # 4-5. enter 눌렀을 때, 오타 여부 표시
    label_help = Label(practice_frame, text="")
    label_help.pack(pady=20)
    label_help.config(text="타자를 입력하고 [Enter] 또는 [Space]를 누르세요.", fg="black")

    # 4-6.오타 난 곳 표시 - 틀린 글자 빨간색으로
    entry_input.tag_config("typo", foreground="red")

    # 4-7. 타수 표시
    label_CPM = Label(practice_frame, text="타수: 0")
    label_CPM.pack()

    # 4-8. 정확도 표시
    label_accuracy = Label(practice_frame, text="정확도: 100.0%")
    label_accuracy.pack()

    # 4-9. 오타 개수 표시
    label_typo = Label(practice_frame, text="오타: 0")
    label_typo.pack()

    # 4-10. 소요시간 표시
    frame_time = Frame(practice_frame)
    frame_time.pack()

    label_time = Label(frame_time, text="소요 시간:")
    label_time.pack(side="left")

    label_stopwatch_min = Label(frame_time, text="0분")
    label_stopwatch_min.pack(side="left")

    label_stopwatch_sec = Label(frame_time, text="0초")
    label_stopwatch_sec.pack(side="left")

    mainmenuButton = Button(practice_frame, text="메인 메뉴로", command=show_main)
    mainmenuButton.pack()

# ==========================================
# 5. 결과창 프레임
# ==========================================

    result_frame = Frame(container)
    label_result = Label(result_frame, text="연습 결과", width=40, height=5, font=("Consolas", 15, "bold"), anchor="center")
    label_result.pack()

    # 5-1. 결과창용 시간 표시
    result_time_frame = Frame(result_frame)
    result_time_frame.pack()
    
    label_time = Label(result_time_frame, text="소요 시간: ")
    label_time.pack(side="left")

    label_result_min = Label(result_time_frame, text="0분")
    label_result_min.pack(side="left")

    label_result_sec = Label(result_time_frame, text="0초")
    label_result_sec.pack(side="left")

    # 5-3. 결과창용 타수 표시
    label_result_CPM = Label(result_frame, text="")
    label_result_CPM.pack()

    # 5-4. 결과창용 정확도 표시 
    label_result_accuracy = Label(result_frame, text="")
    label_result_accuracy.pack()

    # 5-5. 다시하기 버튼 표시
    restartButton = Button(result_frame, text="다시 하기", command=restart)
    restartButton.pack()

    # 5-6. 히트맵 보기 버튼 표시
    heatmapButton = Button(result_frame, text="히트맵 보기", command=show_heatmap)
    heatmapButton.pack()

    # 5-7. 결과창용 차트 표시
    chart_frame = Frame(result_frame)
    chart_frame.pack(pady=10)

    return container