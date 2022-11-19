from tkinter import *
import tkinter as tk
from tkinter import messagebox
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

window_login = Tk()

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

def window_login_func():
    #로그인 창 설정
    window_login.title("회원 로그인")

    tk.Label(window_login, text = "ID : ").grid(row = 0, column = 0, padx = 10, pady = 10)
    tk.Label(window_login, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
    tk.Entry(window_login, textvariable = user_id).grid(row = 0, column = 1, padx = 10, pady = 10)
    tk.Entry(window_login, textvariable = password, show='*').grid(row = 1, column = 1, padx = 10, pady = 10)
    tk.Button(window_login, text = "로그인", command = login).grid(row = 2, column = 1, padx = 10, pady = 10)

    window_login.mainloop()

#마이페이지
def myPage():
    window_myPage = Tk()

    window_myPage.title("마이페이지")


#설문
def survey1():

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
    
    window_survey1 = Tk()
    window_survey1.title("설문 제목.")
    window_survey1.geometry("500x500+500+200")

    q1 = tk.Label(window_survey1, text="질문1내용")
    q1.pack()


    q1_var = tk.IntVar()

    button_q1a1 = tk.Radiobutton(window_survey1, text="질문1의 선택지1", value=1, variable=q1_var)
    button_q1a2 = tk.Radiobutton(window_survey1, text="질문1의 선택지2", value=2, variable=q1_var)
    button_q1a3 = tk.Radiobutton(window_survey1, text="질문1의 선택지3", value=3, variable=q1_var)
    button_q1a4 = tk.Radiobutton(window_survey1, text="질문1의 선택지4", value=4, variable=q1_var)

    button_q1a1.pack()
    button_q1a2.pack()
    button_q1a3.pack()
    button_q1a4.pack()

    next1 = tk.Button(window_survey1, text="다음")
    next1.pack()
#일단 첫번째 질문 선택 화면까지는 단순히 구현했으나
#이후로는 영상-질문-영상-질문의 연속이고 앞서 말씀드린것처럼
#영상을 아예 이미지로 대체하는 것에 대한 결정이 안났고
#이제 답변을 사용자의 데이터에 저장하고 통계를 내는 과정이 시작되기 때문에
#또한 위의 마이페이지 화면 구성 부분은 
# 두 과정은 사용자 데이터 구조를 만드신 조원분이 방향성을 알려주신 후 진행하는게 좋을 것 같습니다

#홈화면
def window_thumnails_func():
    
    global exit

    if exit:
        window_thumnails = Tk()
            
        window_thumnails.title("홈")

        Button(window_thumnails, text="마이페이지", command = myPage).grid(row=0, column=0, ipadx=200, ipady=10)
        Button(window_thumnails, text="<<").grid(row=3, column=0, ipadx=200, ipady=10)
        Button(window_thumnails, text=">>").grid(row=3, column=2, ipadx=200, ipady=10)


        thumb1 = PhotoImage(file=r"./gui/thumb1_cat.png")
        t1 = tk.Button(window_thumnails, image=thumb1, command=survey1).grid(row=1, column=0)

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

        window_thumnails.mainloop()

    else:
        pass



if __name__ == '__main__':
    window_login_func()

    window_thumnails_func()