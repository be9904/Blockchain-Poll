from tkinter import *
import tkinter as tk
from tkinter import messagebox
from socket import *
from tcp import client
import survey
import time
#from PIL import ImageTk
#import numpy as np
#import cv2 as cv
#import os

#처음엔 로그인 윈도우를 가장 먼저 띄우고 로그인에 성공하면
#로그인 윈도우는 사라지고 홈화면 윈도우가 뜨는 방식을 생각하고
#홈화면 윈도우를 구성하는 함수를 만든 다음에 로그인에 성공하면
#그 함수를 실행하는 방향으로 작성했습니다

#그런데 홈화면에서 이미지를 불러와야 하고 이미지를 불러오는게
#클래스 안에서 진행되면 에러가 뜨더라구요
#그래서 일단 함수로 하지 않고 그냥 처음부터 홈화면 윈도우를 열어놓는 것으로
#로그인 윈도우 부분을 비활성화해놓고 홈화면 윈도우 부분을 완성한 뒤
#로그인과 홈화면을 한꺼번에 실행하니 또다른 에러가...ㅠㅠ

#다른 좋은 방식이 있으시면 알려주시고 최대한 에러를 해결할 방법을 찾아보겠습니다.

# create client instance
_client = client.LocalClient()
# create client socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# connect to server
clientSocket.connect((_client.serverIP, _client.serverPort))

window_login = tk.Tk()
window_login.geometry("300x150+500+200")

user_id, password = StringVar(), StringVar()

exit = 0
#로그인 함수
def login():
    if user_id.get() == "id" and password.get() == "pw":
        print("로그인 성공")
        global exit
        exit = 1
        window_login.destroy() 
    else:
        messagebox.showinfo('로그인', '로그인 실패')

def login_tcp(username, password):
    # 프레임 내에서 텍스트 변경
    # tk.Label(window_login, text = "TEST").grid(row = 0, column = 0, padx = 10, pady = 10)
    login_success = False

    packet = _client.try_login(clientSocket, username.get(), password.get())
    login_success = packet[0]
    if not login_success:
        messagebox.showinfo('로그인', packet[1])
    if login_success:
        window_login.destroy()
        if username.get() == 'admin':
            window_thumnails_func(True)
        else:
            window_thumnails_func(False)        

def window_login_func():
    #로그인 창 설정
    window_login.title("회원 로그인")

    tk.Label(window_login, text = "ID : ").grid(row = 0, column = 0, padx = 10, pady = 10)
    tk.Label(window_login, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
    tk.Entry(window_login, textvariable = user_id).grid(row = 0, column = 1, padx = 10, pady = 10)
    tk.Entry(window_login, textvariable = password, show='*').grid(row = 1, column = 1, padx = 10, pady = 10)
    tk.Button(window_login, text='로그인', command= lambda: login_tcp(user_id, password)).grid(row = 2, column = 1, padx = 10, pady = 10)
    window_login.protocol("WM_DELETE_WINDOW", lambda: disconnect(window_login))
    window_login.mainloop()

#마이페이지
def myPage():
    window_myPage = Tk()

    window_myPage.title("마이페이지")


#설문
def survey1(window):

   # window_video1 = Tk()
    #window_video1.title("설문 제목")

    #video = cv.VideoCapture('thumb1_video1.mp4')
    #ret, frame = video.read()
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #img = Image.fromarray(frame)
    #imgtk = ImageTk.PhotoImage(image=img)
    #lbl1.imgtk = imgtk
    #lbl1.configure(image=imgtk)
    #lbl1.after(10, video_play)

#openCV로 동영상을 불러오는 방법을 찾아보고 따라해보았지만
#영상은 프레임, 코덱 등 바로 이해하고 따라하기 어려운 부분이 있었고
#실행또한 되지 않았습니다ㅠ

#저희가 다수의 영상을 필요로 하는 만큼 복잡도를 줄이기 위해
#그냥 이미지나 gif로 대체하는 것에 대한 의견을 여쭤보고 싶습니다

    window.destroy()

    # setup survey
    survey1 = survey.CreateSample()
    curQ = survey1.head

    # load question
    window = load_question(survey1, curQ, curWindow=None)

    # button_q1a1 = tk.Radiobutton(window_survey1, text="질문1의 선택지1", value=1, variable=q1_var)
    # button_q1a2 = tk.Radiobutton(window_survey1, text="질문1의 선택지2", value=2, variable=q1_var)
    # button_q1a3 = tk.Radiobutton(window_survey1, text="질문1의 선택지3", value=3, variable=q1_var)
    # button_q1a4 = tk.Radiobutton(window_survey1, text="질문1의 선택지4", value=4, variable=q1_var)

    # button_q1a1.pack()
    # button_q1a2.pack()
    # button_q1a3.pack()
    # button_q1a4.pack()

    # next1 = tk.Button(window, text="다음")
    # next1.pack()

# for debugging
def print_results(survey):
    q = survey.head
    while q.nextVal is not None:
        print("q:", q.userChoice)
        q = q.nextVal
        print()

def choose_answer(question, index):
    question.choose_option(index.get())

def destroy_window(window, survey):
    window.destroy()
    messagebox.showinfo('설문 완료', '설문을 완료하여 코인이 지급되었습니다!')
    print_results(survey)
    window_thumnails_func()

def load_question(survey, curQ, curWindow):
    if curWindow is not None:
        curWindow.destroy()

    window = Tk()
    window.geometry("500x500+500+200")
    window.title(survey.name)

    image_frame = tk.Frame(window, relief='groove', bd=2)
    image_frame.pack(side='left', fill='both', expand=True)
    i = PhotoImage(file="./gui/q1image.png")
    t = tk.Label(image_frame, image=i)
    t.image = i
    t.pack()

    text_frame = tk.Frame(window, relief='groove', bd=2)
    text_frame.pack(side='right', fill='both', expand=True)
    tk.Label(text_frame, text=curQ.question).pack()

    q1_var = tk.IntVar()
    
    for i in range(len(curQ.answer)):
        tk.Radiobutton(
            text_frame,
            text=curQ.answer[i][0],
            value=i,
            variable=q1_var,
            command=lambda:choose_answer(curQ, q1_var)
        ).pack()

    if curQ.nextVal is None:
        next = tk.Button(text_frame, text="완료", command= lambda: destroy_window(window, survey))
        next.pack()
    else:
        next = tk.Button(text_frame, text="다음", command= lambda: load_question(survey, curQ.nextVal, window))
        next.pack()
#일단 첫번째 질문 선택 화면까지는 단순히 구현했으나
#이후로는 영상-질문-영상-질문의 연속이고 앞서 말씀드린것처럼
#영상을 아예 이미지로 대체하는 것에 대한 결정이 안났고
#이제 답변을 사용자의 데이터에 저장하고 통계를 내는 과정이 시작되기 때문에
#또한 위의 마이페이지 화면 구성 부분은 
# 두 과정은 사용자 데이터 구조를 만드신 조원분이 방향성을 알려주신 후 진행하는게 좋을 것 같습니다

#홈화면
def window_thumnails_func(isAdmin):
    window_thumnails = tk.Tk()
    
    window_thumnails.title("홈")

    Button(window_thumnails, text="마이페이지", command = myPage).grid(row=0, column=0, padx=(0,230))
    if isAdmin:
        tk.Button(window_thumnails, text="서버 종료", command=lambda:close_server(window_thumnails)) \
        .grid(
            row=0,
            column=2,
            padx=(245,0)
        )
    Button(window_thumnails, text="<<").grid(row=3, column=0, ipadx=75, ipady=5)
    Button(window_thumnails, text=">>").grid(row=3, column=2, ipadx=75, ipady=5)


    thumb1 = PhotoImage(file=r"./gui/thumb1_cat.png")
    t1 = tk.Button(window_thumnails, image=thumb1, command=lambda:survey1(window_thumnails)).grid(row=1, column=0)

    thumb2 = PhotoImage(file=r"./gui/thumb2_mbti.png")
    t2 = tk.Button(window_thumnails, image=thumb2).grid(row=1,column=1)

    thumb3 = PhotoImage(file=r"./gui/thumb3_game.png")
    t3 = tk.Button(window_thumnails, image=thumb3).grid(row=1, column=2)

    thumb4 = PhotoImage(file=r"./gui/thumb4_food.png")
    t4 = tk.Button(window_thumnails, image=thumb4).grid(row=2, column=0)

    thumb5 = PhotoImage(file=r"./gui/thumb5_character.png")
    t5 = tk.Button(window_thumnails, image=thumb5).grid(row=2, column=1)

    thumb6 = PhotoImage(file=r"./gui/thumb6_ott.png")
    t6 = tk.Button(window_thumnails, image=thumb6).grid(row=2, column=2)

    window_thumnails.protocol("WM_DELETE_WINDOW", lambda: disconnect(window_thumnails))
    window_thumnails.mainloop()

def disconnect(window):
    try:
        clientSocket.send('disconnect'.encode())
        clientSocket.close()
    except:
        pass
    window.destroy()

def close_server(window):
    try:
        clientSocket.send('close server'.encode())
        clientSocket.close()
    except:
        pass
    window.destroy()

if __name__ == '__main__':
    window_login_func()

    # window_thumnails_func()