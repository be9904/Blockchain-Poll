from tkinter import *
import tkinter as tk
from tkinter import messagebox
from socket import *
from tcp import client
import survey
from blockchain import *
from user import *
from plot import *

class AppGUI:
    # constructor
    def __init__(self, isDebugging=False):
        # create client instance
        self._client = client.LocalClient(BlockchainClient())
        self.isAdmin = False
        # create client socket
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        # connect to server
        self.clientSocket.connect((self._client.serverIP, self._client.serverPort))
        self.curUser = None
        # sample survey
        self.sampleSurvey = survey.CreateSample()
        self.sampleSurveyResults = []
        # user info
        self.userBalance = None
        self.userTransactions = []

        self.start_app()

    ############################################################
    ######################### Init GUI #########################
    ############################################################
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
            self.curUser = User(BlockchainClient(), username.get())
            if self.curUser.name == 'admin':
                self.isAdmin = True
                self.window_thumbnails(self.isAdmin)
            else:
                self.window_thumbnails(self.isAdmin)        

    ############################################################
    ###################### Survey Screen #######################
    ############################################################
    def start_survey(self, window):
        # check if already participated, if already participated, show error message
        if self.sampleSurvey.participants.get(self.curUser.name):
            messagebox.showinfo('오류', '이미 참여한 설문입니다')
            return

        window.destroy()

        # setup survey
        curQ = self.sampleSurvey.head

        # create survey window
        window = Tk()
        window.geometry("700x300+500+200")
        window.title(self.sampleSurvey.name)

        # set image frame
        image_frame = tk.Frame(window, relief='groove', bd=2)
        image_frame.pack(side='left', fill='both', expand=True)
        i = PhotoImage(file="./gui/q1image.png")
        t = tk.Label(image_frame, image=i)
        t.image = i
        t.pack()

        # load question
        window = self.load_question(curQ, window, prevFrame=None)

    # get questions (recursive)
    def load_question(self, curQ, curWindow, prevFrame):
        if prevFrame is not None:
            prevFrame.pack_forget()
            prevFrame.destroy()

        text_frame = tk.Frame(curWindow, relief='groove', bd=2)
        text_frame.pack(side='right', fill='both', expand=True)
        tk.Label(text_frame, text=curQ.question, width=100).pack()

        q1_var = tk.IntVar()
        
        for i in range(len(curQ.answer)):
            tk.Radiobutton(
                text_frame,
                text=curQ.answer[i][0],
                value=i,
                variable=q1_var,
                command=lambda:self.choose_answer(curQ, q1_var),
                pady=5
            ).pack(anchor=W)

        if curQ.nextVal is None:
            next = tk.Button(text_frame, text="완료", command= lambda: self.finish_survey(curWindow))
            next.pack()
        else:
            next = tk.Button(text_frame, text="다음", command= lambda: self.load_question(curQ.nextVal, curWindow, text_frame))
            next.pack()

    ############################################################
    ################# Survey Command Functions #################
    ############################################################
    def no_survey(self):
        messagebox.showinfo('오류', '설문이 아직 준비되지 않았습니다')
    
    def choose_answer(self, question, index):
        question.choose_option(index.get())

    def finish_survey(self, window):
        window.destroy()

        transactions = []
        t = Transaction(
            sampleCreator.client,
            self.curUser.client,
            incentive
        )
        self.curUser.update_balance(incentive)
        t.sign_transaction()
        transactions.append(t)
        self.userTransactions.append(t)
        
        chain.add_block(transactions)
        chain.update_chain()
        
        # update balance

        # add curuser to participants list
        self.sampleSurvey.participants[self.curUser.name] = True

        messagebox.showinfo('설문 완료', '설문을 완료하여 코인이 지급되었습니다!')

        # request update to server
        msg = "update_userinfo "+str(self.curUser.balance)
        self.clientSocket.send(msg.encode())
        self.clientSocket.recv(1024).decode()
    
        self.save_results()
        self.window_thumbnails(self.isAdmin)

    ############################################################
    ####################### Home Screen ########################
    ############################################################
    def window_thumbnails(self, isAdmin):
        window = tk.Tk()
        window.geometry("+750+400")
        window.title("홈")

        if isAdmin:
            tk.Button(window, text="서버 종료", command=lambda:self.close_server(window)) \
            .grid(
                row=0,
                column=2,
                padx=(245,0)
            )
        tk.Button(window, text="<<").grid(row=3, column=0, ipadx=75, ipady=5)
        tk.Button(window, text=">>").grid(row=3, column=2, ipadx=75, ipady=5)
        tk.Button(window, text="마이페이지", command =self.window_mypage).grid(row=0, column=0, padx=(0,230))
        self.update_balance_ui(window)

        thumb1 = PhotoImage(file=r"./gui/thumb1_cat.png")
        t1 = tk.Button(window, image=thumb1).grid(row=1, column=0)
        tk.Label(window, text = str(self.sampleSurvey.view_cost)+" 코인").grid(row = 1, column = 0, pady=(180,0))
        tk.Button(window, text='설문 참여하기', command=lambda:self.start_survey(window))\
            .grid(row=1, column=0, padx=(0,210), pady=(175,0))
        tk.Button(window, text='설문 열람하기', command=lambda:self.window_results(window))\
            .grid(row=1, column=0, padx=(215,0), pady=(175,0))

        thumb2 = PhotoImage(file=r"./gui/thumb2_mbti.png")
        t2 = tk.Button(window, image=thumb2).grid(row=1,column=1)
        tk.Label(window, text = "15 코인").grid(row = 1, column = 1, pady=(180,0))
        tk.Button(window, text='설문 참여하기', command=self.no_survey)\
            .grid(row=1, column=1, padx=(0,210), pady=(175,0))
        tk.Button(window, text='설문 열람하기', command=self.no_survey)\
            .grid(row=1, column=1, padx=(215,0), pady=(175,0))

        thumb3 = PhotoImage(file=r"./gui/thumb3_game.png")
        t3 = tk.Button(window, image=thumb3).grid(row=1, column=2)
        tk.Label(window, text = "10 코인").grid(row = 1, column = 2, pady=(180,0))
        tk.Button(window, text='설문 참여하기', command=self.no_survey)\
            .grid(row=1, column=2, padx=(0,210), pady=(175,0))
        tk.Button(window, text='설문 열람하기', command=self.no_survey)\
            .grid(row=1, column=2, padx=(215,0), pady=(175,0))

        thumb4 = PhotoImage(file=r"./gui/thumb4_food.png")
        t4 = tk.Button(window, image=thumb4).grid(row=2, column=0)
        tk.Label(window, text = "25 코인").grid(row = 2, column = 0, pady=(180,0))
        tk.Button(window, text='설문 참여하기', command=self.no_survey)\
            .grid(row=2, column=0, padx=(0,210), pady=(175,0))
        tk.Button(window, text='설문 열람하기', command=self.no_survey)\
            .grid(row=2, column=0, padx=(215,0), pady=(175,0))

        thumb5 = PhotoImage(file=r"./gui/thumb5_character.png")
        t5 = tk.Button(window, image=thumb5).grid(row=2, column=1)
        tk.Label(window, text = "5 코인").grid(row = 2, column = 1, pady=(180,0))
        tk.Button(window, text='설문 참여하기', command=self.no_survey)\
            .grid(row=2, column=1, padx=(0,210), pady=(175,0))
        tk.Button(window, text='설문 열람하기', command=self.no_survey)\
            .grid(row=2, column=1, padx=(215,0), pady=(175,0))

        thumb6 = PhotoImage(file=r"./gui/thumb6_ott.png")
        t6 = tk.Button(window, image=thumb6).grid(row=2, column=2)
        tk.Label(window, text = "20 코인").grid(row = 2, column = 2, pady=(180,0))
        tk.Button(window, text='설문 참여하기', command=self.no_survey)\
            .grid(row=2, column=2, padx=(0,210), pady=(175,0))
        tk.Button(window, text='설문 열람하기', command=self.no_survey)\
            .grid(row=2, column=2, padx=(215,0), pady=(175,0))

        window.protocol("WM_DELETE_WINDOW", lambda: self.disconnect(window))
        window.mainloop()

    def update_balance_ui(self, window):
        self.userBalance = tk.Label(window, text="보유 코인: "+str(self.curUser.balance)).grid(row=0, column=1)

    # for debugging
    def save_results(self):
        q = self.sampleSurvey.head
        while q is not None:
            # print("q:", q.userChoice)
            self.sampleSurveyResults.append(q.userChoice)
            q = q.nextVal

    ############################################################
    #################### Protocol Functions ####################
    ############################################################
    def disconnect(self, window):
        try:
            self.clientSocket.send('disconnect'.encode())
            self.clientSocket.close()
        except:
            pass
        window.destroy()
        quit()

    def close_server(self, window):
        try:
            self.clientSocket.send('close server'.encode())
            self.clientSocket.close()
        except:
            pass
        window.destroy()
    
    ############################################################
    ###################### Results Screen ######################
    ############################################################
    def window_results(self, window):
        if self.sampleSurvey.buyers.get(self.curUser.name) is None:
            res = messagebox.askquestion('열람 확인', str(self.sampleSurvey.view_cost)+' 코인을 지불하고 설문을 열람하시겠습니까?')
            if res == 'yes':
                # transaction
                transactions = []
                t = Transaction(
                    self.curUser.client,
                    sampleCreator.client,
                    self.sampleSurvey.view_cost
                )
                self.curUser.update_balance(-self.sampleSurvey.view_cost)
                self.update_balance_ui(window)
                t.sign_transaction()
                transactions.append(t)
                self.userTransactions.append(t)
                
                chain.add_block(transactions)
                chain.update_chain()

                # add to buyers list
                self.sampleSurvey.buyers[self.curUser.name] = True

                # request update to server
                msg = "update_userinfo "+str(self.curUser.balance)
                self.clientSocket.send(msg.encode())
                self.clientSocket.recv(1024).decode()
                
                # show plot
                plot_hist(self.sampleSurveyResults)
            else:
                pass
        else:
            plot_hist(self.sampleSurveyResults)

    ############################################################
    ######################### My Page ##########################
    ############################################################
    def window_mypage(self):
        # window = tk.Toplevel(parentWindow)
        # window.title("마이페이지")
        # window.geometry("500x500+500+200")

        window = Tk()
        window.title('거래내역')
        window.geometry("600x400")

        if len(self.userTransactions) == 0:
            tk.Label(window, text = "거래내역이 없습니다.").grid(row = 0, column = 1, padx=(250,0), pady=(180,0))
            return

        canvas = Canvas(window)
        vsb = Scrollbar(window, orient="vertical", command=canvas.yview)

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        canvas.configure(yscrollcommand=vsb.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        row_num = 0

        for t in self.userTransactions:
            tk.Button(canvas, text=t.txn_hash[:14]+"...", command=lambda t=t:self.showinfo(t))\
                .grid(row=row_num, ipadx=235)
            row_num += 1

    def showinfo(self, t):
        messagebox.showinfo('거래내역 조회', 
            'From: ' + t.sender.identity +
            '\n\nTo: ' + t.recipient.identity +
            '\n\nvalue: ' + str(t.value) + 
            '\n\nTransaction Hash: ' + t.txn_hash + 
            '\n\nTimestamp: ' + str(t.time))
            

if __name__ == '__main__':
    chain = Blockchain()
    incentive = 2.0
    sampleCreator = User(BlockchainClient(), 'sampleCreator')
    
    # dummy user makes transaction
    dummyUser1 = User(BlockchainClient(), 'dummy')
    transactions = []
    t = Transaction(
        sampleCreator.client,
        dummyUser1.client,
        incentive
    )
    t.sign_transaction()
    transactions.append(t)
    
    chain.add_block(transactions)
    chain.update_chain()
    
    # run the main gui app
    app = AppGUI()