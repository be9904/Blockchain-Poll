from socket import *
import json

class LocalServer:
    # constructor
    def __init__(self, path):
        # load server data from json
        self.path = path
        self.user_json = open(self.path)
        self.registered_users = json.load(self.user_json)
        self.user_data = json.load(open('./users.json'))

        # initial server settings
        self.serverHost = '127.0.0.1'
        self.serverPort = 12000
        self.connectionSocket = None
        self.addr = None
        
        # set server and connection booleans
        self.serverOpen = True       # is server running?
        self.isConnected = False     # is client connected?
        
        # define currently logged in id
        self.curUser = None

    def update_userinfo(self, new_balance):
         # open json as write mode
        user_json = open('./users.json', 'w')
        
        # add new user info
        self.user_data[self.curUser]['balance'] = new_balance
        
        # update json
        json.dump(self.user_data, user_json)

    # login check function
    def try_login(self, username, password):   
        # not registered
        if self.registered_users.get(username) is None:
            return (False, '가입되어 있지 않은 아이디입니다')
        
        # login success
        if self.registered_users[username] == password:
            self.curUser = username
            return (True, '로그인 성공')
        
        return (False, '비밀번호를 확인해주세요')
    
    def try_logout(self):
        # logout
        if self.curUser != None:
            logout_user = self.curUser
            self.curUser = None
            return (True, '로그아웃 됨: ' + logout_user)
        # try logout when not logged in
        elif self.curUser == None:
            return (False, '로그인 되어 있지 않습니다')

    # register check function
    def try_register(self, username, password, path):
        # check id pw validity
        if username == None or password == None:
            return (False, '사용할 수 없는 아이디 또는 비밀번호입니다')

        # already registered
        if self.registered_users.get(username) is not None:
            return (False, '이미 가입되어 있는 아이디입니다')
        # register new user
        else:
            # open json as write mode
            user_json = open(self.path, 'w')
            
            # add new user info
            self.registered_users[username] = password
            
            # update json
            json.dump(self.registered_users, user_json)
            self.curUser = username
            return (True, '가입 성공')

    def handle_login(self):
        while True:
            # receive message from client, log
            data = self.connectionSocket.recv(1024)
            print('message received from', self.addr)

            # decode received data
            data = data.decode()

            if data == 'close server':
                print('closing server... goodbye')

                # set server boolean
                self.serverOpen = False

                # send reply to client
                self.connectionSocket.send(return_msg.encode())

                # close socket connection
                self.connectionSocket.close()
                break

            data = data.split()

            if data[0] == 'update_userinfo':
                self.update_userinfo(float(data[1]))
                self.connectionSocket.send(data[1].encode())
                print('------------------------------')
                continue

            if data == [] or data[0] == 'disconnect':
                self.isConnected = False
                print(self.addr,'has disconnected')
                break

            # try login and set ret msg
            _trylogin = self.try_login(data[1], data[2])
            return_msg = _trylogin[1]

            self.connectionSocket.send(return_msg.encode())
            print('------------------------------')

    # handle client request
    def handle_request(self):
        # run server
        while True:
            # receive message from client, log
            data = self.connectionSocket.recv(1024)
            print('message received from', self.addr)

            # decode received data
            data = data.decode()

            ####################################################################
            ######################## Close Server ##############################
            ####################################################################
            if data == 'close server':
                # return msg and log
                return_msg = 'close@' + str(self.serverPort)
                print('closing server... goodbye')

                # set server boolean
                self.serverOpen = False

                # send reply to client
                self.connectionSocket.send(return_msg.encode())

                # close socket connection
                self.connectionSocket.close()
                break

            ####################################################################
            ###################### Disconnect Client ###########################
            ####################################################################
            elif data == 'disconnect':
                # return msg and log
                return_msg = 'disconnect@' + str(self.serverPort)
                print(self.addr,'has disconnected from server')

                # logout
                self.curUser = None

                # set connection boolean
                self.isConnected = False
                
                # send reply to client
                self.connectionSocket.send(return_msg.encode())

                # close socket connection
                self.connectionSocket.close()
                break

            ####################################################################
            ##################### Login, Logout, Register ######################
            ####################################################################
            else:
                # split client msg into tokens
                data = data.split()

                ############################ Logout ################################

                # logout
                if data[0] == 'logout':
                    _trylogout = self.try_logout()
                    return_msg = _trylogout[1]
                # client msg in wrong format
                elif len(data) != 3:
                    print('wrong client msg format')
                    return_msg = '잘못된 형식입니다'
                    continue

                ######################## Login/Register ############################
                
                # check client msg encoding (will be removed)
                print('client msg:', data)

                # not logged in
                if self.curUser == None:
                    # login
                    if data[0] == 'li':
                        # try login and set ret msg
                        _trylogin = self.try_login(data[1], data[2])
                        return_msg = _trylogin[1]
                    # register
                    if data[0] == 'r':
                        # try register and set ret msg
                        _tryregister = self.try_register(data[1], data[2], self.path)
                        return_msg = _tryregister[1]
                # already logged in
                else:
                    return_msg = '이미 로그인 되어 있습니다. (' + self.curUser + ')'

                ####################### Reply to Client ############################
                
                # send reply to client
                self.connectionSocket.send(return_msg.encode())
                print('------------------------------')
    
    ####################################################################
    ######################## Main Server App ###########################
    ####################################################################
    def server_main(self):
        # create socket
        serverSocket = socket(AF_INET, SOCK_STREAM)

        # exception handling
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print('socket created')

        # bind
        serverSocket.bind((self.serverHost, self.serverPort))
        print("socket binded to %s" %(self.serverPort))

        # listen
        serverSocket.listen()
        print('server is listening')
        print('------------------------------')

        # accept client connection
        while True:
            # connect client if none is connected
            if self.isConnected is False:
                self.connectionSocket, self.addr = serverSocket.accept()
                self.isConnected = True
                print(self.addr,'has connected')
            
            # handle client request
            self.handle_request()
            
            # if server close requested, terminate program
            if self.serverOpen is False:
                return

    def server_login(self):
        # create socket
        serverSocket = socket(AF_INET, SOCK_STREAM)

        # exception handling
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print('socket created')

        # bind
        serverSocket.bind((self.serverHost, self.serverPort))
        print("socket binded to %s" %(self.serverPort))

        # listen
        serverSocket.listen()
        print('server is listening')
        print('------------------------------')

        while True:
            if self.serverOpen is False:
                break

            # connect client if none is connected
            if self.isConnected is False:
                self.connectionSocket, self.addr = serverSocket.accept()
                self.isConnected = True
                print(self.addr,'has connected')

            self.handle_login()

        self.connectionSocket.close()
####################################################################
####################################################################
####################################################################

##################### Server main Test Run #########################

if __name__ == "__main__":
    server = LocalServer('./registered-users.json')
    server.server_login()