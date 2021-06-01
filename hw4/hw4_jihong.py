# socket 과 select 모듈 임포트
from os import access, read
from socket import *
from select import *
import threading
import sys
import time

tcpPort = int(sys.argv[1])
userID = str(sys.argv[2])

print("Student ID: 20191572")
print("Name: Kimjihong")

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind( ('', tcpPort) )
serverSocket.listen()

connect_lst = [serverSocket, sys.stdin]


def send(sock, userID):
    while connect_lst:
        RealData = input()
        sendData = userID+' : '+RealData
        
        sock.send(sendData.encode('utf-8'))
        
        # if RealData == "@quit":
        #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #     try: 
        #         sock.close() 
        #         continue
        #     except: pass

def receive(sock):
    while True:
        try:
            recvData = sock.recv(1024)
            if recvData:
                print(recvData.decode('utf-8'))

        except:
            pass

        
while connect_lst:

    read_sock, write_sock, error_sock = select(connect_lst, [], [])

    for sock in read_sock:

        if sock == serverSocket:
            clientSocket, addr = serverSocket.accept()

            print("THIS IS SHERVER")

            IP = addr[0]
            PORT = addr[1]

            print("Connection from host {}, port {}, socket fd {}" .format(IP, PORT, clientSocket.fileno()))
            
            connect_lst.append(clientSocket)

            sender = threading.Thread(target=send, args=(clientSocket, userID,))
            receiver = threading.Thread(target=receive, args=(clientSocket,))

            sender.start()
            receiver.start()


            while True:
                time.sleep(1)
                pass

        elif sock == sys.stdin:
            message = sys.stdin.readline()

            if message[0] == '@':
                input_cmd = message.split()
                if input_cmd[0] == "@talk":

                    chattSocket = socket(AF_INET, SOCK_STREAM)
                    chattSocket.connect(('', int(input_cmd[2])))

                    sender = threading.Thread(target=send, args=(chattSocket, userID))
                    receiver = threading.Thread(target=receive, args=(chattSocket,))

                    connect_lst.append(chattSocket)

                    sender.start()
                    receiver.start()


                    while True:
                        time.sleep(1)
                        pass

        else: print("ELSE HERE!")
                    

                                                
serverSocket.close()
