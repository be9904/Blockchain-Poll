from socket import *

class LocalClient:
    # constructor
    def __init__(self, bclient):
        # set server ip and port
        self.serverIP = '127.0.0.1'      # local host
        self.serverPort = 12000
        self.bclient = bclient

    ####################################################################
    ######################## Define Functions ##########################
    ####################################################################

    # login msg func
    def login_msg(self, id, pw):
        return 'li ' + id + ' ' + pw

    # register msg func
    def register_msg(self, id, pw):
        return 'r ' + id + ' ' + pw

    def try_login(self, clientSocket, username, password):
        isSuccess = True

        clientSocket.send(self.login_msg(username, password).encode())

        receivedMessage = clientSocket.recv(1024).decode()
        
        # log server reply
        print('----------------------')
        print(' received message from server')
        print('----------------------')

        if receivedMessage == '가입되어 있지 않은 아이디입니다' or receivedMessage == '비밀번호를 확인해주세요':
            isSuccess = False

        return (isSuccess, receivedMessage)

    # start screen as function
    # generates login, logout, register, exit, close server messages
    def start_screen(self, action, socket):
        # login
        if action == '1':
            user_id = input('ID : ')
            user_pw = input('PW : ')
            socket.send(self.login_msg(user_id, user_pw).encode())
        # logout
        elif action == '2':
            socket.send('logout'.encode())
        # register
        elif action == '3':
            user_id = input('ID : ')
            user_pw = input('PW : ')
            socket.send(self.register_msg(user_id, user_pw).encode())
        # exit
        elif action == '4':
            socket.send('disconnect'.encode())
        # close server from client (will be removed)
        elif action == '5':
            socket.send('close server'.encode())
        # error, try again
        else:
            print('다시 선택하세요')
            print('------------------------------')
            return False
        
        return True

    ####################################################################
    ######################## Main Client App ###########################
    ####################################################################
    def client_main(self):

        # create client socket
        clientSocket = socket(AF_INET, SOCK_STREAM)

        # connect to server
        clientSocket.connect((self.serverIP, self.serverPort))

        # start loop
        while True:
            # send message to server
            action = input('수행할 작업을 선택하세요:\n(1) 로그인\n(2) 로그아웃\n(3) 가입\n(4) 종료\n')
            
            # run start screen functionalities
            if self.start_screen(action, clientSocket) is False:
                continue

            # receive reply from server
            receivedMessage = clientSocket.recv(1024).decode()

            # disconnect reply
            if receivedMessage == 'disconnect@' + str(self.serverPort):
                # print(receivedMessage)
                break
            # server close reply
            if receivedMessage == 'close@' + str(self.serverPort):
                # print(receivedMessage)
                break

            # log server reply
            print('----------------------')
            print(' <Server>', receivedMessage)
            print('----------------------')

        clientSocket.close()

####################################################################
####################################################################
####################################################################

###################### Client main Test Run ########################

if __name__ == "__main__":
    client = LocalClient()
    client.client_main()