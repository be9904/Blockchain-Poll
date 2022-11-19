from tkinter import *
import tkinter as tk
from tkinter import messagebox
from socket import *
from tcp import client
import survey
import time
from blockchain import *
from plot import *

class AppGUI:
    def __init__(self):
        # create client instance
        self._client = client.LocalClient(BlockchainClient())
        self.isAdmin = False
        # create client socket
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        # connect to server
        self.clientSocket.connect((self._client.serverIP, self._client.serverPort))

        self.start_app()

    def start_app(self):
        window_login = tk.Tk()
        window_login.geometry("300x150+500+200")

        user_id, password = StringVar(), StringVar()

        window_login.title("회원 로그인")

        tk.Label(window_login, text = "ID : ").grid(row = 0, column = 0, padx = 10, pady = 10)
        tk.Label(window_login, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
        tk.Entry(window_login, textvariable = user_id).grid(row = 0, column = 1, padx = 10, pady = 10)
        tk.Entry(window_login, textvariable = password, show='*').grid(row = 1, column = 1, padx = 10, pady = 10)
        tk.Button(window_login, text='로그인', command= lambda: self.login_tcp(window_login, user_id, password)).grid(row = 2, column = 1, padx = 10, pady = 10)
        window_login.protocol("WM_DELETE_WINDOW", lambda: self.disconnect(window_login))
        window_login.mainloop()



    def login_tcp(self, window, username, password):
        # 프레임 내에서 텍스트 변경
        # tk.Label(window_login, text = "TEST").grid(row = 0, column = 0, padx = 10, pady = 10)
        login_success = False

        packet = self._client.try_login(self.clientSocket, username.get(), password.get())
        login_success = packet[0]
        if not login_success:
            messagebox.showinfo('로그인', packet[1])
        if login_success:
            window.destroy()
            if username.get() == 'admin':
                self.isAdmin = True
                self.window_thumnails_func(self.isAdmin)
            else:
                self.window_thumnails_func(self.isAdmin)        

        #설문
    def survey1(self, window):
        window.destroy()

        # setup survey
        survey1 = survey.CreateSample()
        curQ = survey1.head

        # load question
        window = self.load_question(survey1, curQ, curWindow=None)

    # for debugging
    def print_results(self, survey):
        q = survey.head
        while q is not None:
            print("q:", q.userChoice)
            q = q.nextVal
            print()

    def choose_answer(self, question, index):
        question.choose_option(index.get())

    def destroy_window(self, window, survey):
        window.destroy()
        messagebox.showinfo('설문 완료', '설문을 완료하여 코인이 지급되었습니다!')
        self.print_results(survey)
        self.window_thumnails_func(self.isAdmin)

    def load_question(self, survey, curQ, curWindow):
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
                command=lambda:self.choose_answer(curQ, q1_var)
            ).pack()

        if curQ.nextVal is None:
            next = tk.Button(text_frame, text="완료", command= lambda: self.destroy_window(window, survey))
            next.pack()
        else:
            next = tk.Button(text_frame, text="다음", command= lambda: self.load_question(survey, curQ.nextVal, window))
            next.pack()

    #홈화면
    def window_thumnails_func(self, isAdmin):
        window_thumnails = tk.Tk()
        
        window_thumnails.title("홈")

        Button(window_thumnails, text="마이페이지", command = myPage).grid(row=0, column=0, padx=(0,230))
        if isAdmin:
            tk.Button(window_thumnails, text="서버 종료", command=lambda:self.close_server(window_thumnails)) \
            .grid(
                row=0,
                column=2,
                padx=(245,0)
            )
        Button(window_thumnails, text="<<").grid(row=3, column=0, ipadx=75, ipady=5)
        Button(window_thumnails, text=">>").grid(row=3, column=2, ipadx=75, ipady=5)


        thumb1 = PhotoImage(file=r"./gui/thumb1_cat.png")
        t1 = tk.Button(window_thumnails, image=thumb1, command=lambda:self.survey1(window_thumnails)).grid(row=1, column=0)

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

        window_thumnails.protocol("WM_DELETE_WINDOW", lambda: self.disconnect(window_thumnails))
        window_thumnails.mainloop()

    def disconnect(self, window):
        try:
            self.clientSocket.send('disconnect'.encode())
            self.clientSocket.close()
        except:
            pass
        window.destroy()

    def close_server(self, window):
        try:
            self.clientSocket.send('close server'.encode())
            self.clientSocket.close()
        except:
            pass
        window.destroy()

#마이페이지
def myPage():
    window_myPage = Tk()

    window_myPage.title("마이페이지")

if __name__ == '__main__':
    app = AppGUI()