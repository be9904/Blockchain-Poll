from socket import *

# set server ip and port
serverIP = '127.0.0.1'      # local host
serverPort = 12000

# create client socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# connect to server
clientSocket.connect((serverIP, serverPort))

# start loop
while True:
    # send message to server
    action = int(input('수행할 작업을 선택하세요:\n(1) 로그인\n(2) 로그아웃\n(3) 가입\n(4) 종료\n'))
    # login
    if action == 1:
        user_id = input('ID : ')
        user_pw = input('PW : ')
        msg = 'li ' + user_id + ' ' + user_pw
        clientSocket.send(msg.encode())
    # logout
    elif action == 2:
        msg = 'logout'
        clientSocket.send(msg.encode())
    # register
    elif action == 3:
        user_id = input('ID : ')
        user_pw = input('PW : ')
        msg = 'r ' + user_id + ' ' + user_pw
        clientSocket.send(msg.encode())
    # exit
    elif action == 4:
        clientSocket.send('disconnect'.encode())
    # close server from client (will be removed)
    elif action == 5:
        clientSocket.send('close server'.encode())
    # error, try again
    else:
        print('다시 선택하세요')
        print('------------------------------')
        continue

    # receive reply from server
    receivedMessage = clientSocket.recv(1024).decode()

    # disconnect reply
    if receivedMessage == 'disconnect@' + str(serverPort):
        # print(receivedMessage)
        break
    # server close reply
    if receivedMessage == 'close@' + str(serverPort):
        # print(receivedMessage)
        break

    print('Server:', receivedMessage)
    print('--------------------')

clientSocket.close()