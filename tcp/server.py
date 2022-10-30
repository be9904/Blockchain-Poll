from socket import *
import json

# login check function
def trylogin(registered_users, username, password):   
    # not registered
    if registered_users.get(username) is None:
        return False
    
    # login success
    if registered_users[username] == password:
        return True    

# register check function
def tryregister(registered_users, username, password):
    # check id pw validity
    if username == None or password == None:
        return False

    # already registered
    if registered_users.get(username) is not None:
        return False
    # register new user
    else:
        # open json as write mode
        user_json = open('./registered-users.json', 'w')
        
        # add new user info
        registered_users[username] = password
        
        # update json
        json.dump(registered_users, user_json)
        return True        

# load server data from json
user_json = open('./registered-users.json')
registered_users = json.load(user_json)

# open server
serverHost = '127.0.0.1'
serverPort = 12000

# create socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# exception handling
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
print('socket created')

# bind
serverSocket.bind((serverHost, serverPort))
print("socket binded to %s" %(serverPort))

# listen
serverSocket.listen()
print('server is listening')
print('------------------------------')

# set server and connection booleans
serverOpen = True       # is server running?
isConnected = False     # is client connected?

# define logged in id
curUser = None

while True:
    # connect client if none is connected
    if isConnected is False:
        connectionSocket, addr = serverSocket.accept()
        isConnected = True
        print(addr,'has connected')

    # run server
    while True:
        # receive message from client, log
        data = connectionSocket.recv(1024)
        print('message received from', addr)

        # decode received data
        data = data.decode()

        ####################################################################
        ######################## Close Server ##############################
        ####################################################################
        if data == 'close server':
            # return msg and log
            return_msg = 'close@' + str(serverPort)
            print('closing server... goodbye')

            # set server boolean
            serverOpen = False

            # send reply to client
            connectionSocket.send(return_msg.encode())

            # close socket connection
            connectionSocket.close()
            break

        ####################################################################
        ######################### Disconnect ###############################
        ####################################################################
        elif data == 'disconnect':
            # return msg and log
            return_msg = 'disconnect@' + str(serverPort)
            print(addr,'has disconnected from server')

            # logout
            curUser = None

            # set connection boolean
            isConnected = False
            
            # send reply to client
            connectionSocket.send(return_msg.encode())

            # close socket connection
            connectionSocket.close()
            break

        ####################################################################
        ###################### Login, Logout, Register #####################
        ####################################################################
        else:
            # split client msg into tokens
            data = data.split()

            ############################ Logout ################################

            # logout
            if data[0] == 'logout' and curUser != None:
                return_msg = '로그아웃 됨: ' + curUser
                curUser = None
            # try logout when not logged in
            elif data[0] == 'logout' and curUser == None:
                return_msg = '로그인 되어 있지 않습니다'
            # client msg in wrong format
            elif len(data) != 3:
                print('check client msg format')
                return_msg = '잘못된 형식입니다'
                continue

            ######################## Login/Register ############################
            
            # check client msg encoding (will be removed)
            print('client msg:', data)

            # not logged in
            if curUser == None:
                # login
                if data[0] == 'li':
                    # success
                    if trylogin(registered_users, data[1], data[2]):
                        return_msg = '로그인 성공'
                        curUser = data[1]
                    # fail
                    else:
                        return_msg = '로그인 실패'
                # register
                if data[0] == 'r':
                    # log in if register success
                    if tryregister(registered_users, data[1], data[2]):
                        return_msg = '가입 성공'
                        curUser = data[1]
                    # id exists
                    else:
                        return_msg = '이미 존재하는 아이디입니다'
            # already logged in
            else:
                return_msg = '이미 로그인 되어 있습니다. (' + curUser + ')'

            ####################### Reply to Client ############################
            
            # send reply to client
            connectionSocket.send(return_msg.encode())
            print('------------------------------')
    
    # if server close requested, terminate program
    if serverOpen is False:
        break