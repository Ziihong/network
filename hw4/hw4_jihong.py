# socket 과 select 모듈 임포트
from os import read
from socket import *
from select import *
import sys

tcpPort = int(sys.argv[1])
userID = str(sys.argv[2])

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind( ('', tcpPort) )
serverSocket.listen()

connect_lst = [serverSocket, sys.stdin]
is_end = 0

while is_end != 1:

    print(userID+'>')

    read_sock, write_sock, error_sock = select(connect_lst, [], [])

    for sock in read_sock:
        # server
        if sock == serverSocket:

            clientSocket, addr = serverSocket.accept()

            IP = addr[0]
            PORT = addr[1]

            print("connection from host {}, port {}, socket {}" .format(IP, PORT, clientSocket.fileno()))
            
            connect_lst.append(clientSocket)
            
        
        elif sock == sys.stdin:
            message = sys.stdin.readline()
            input_cmd = message.split()
            cmd = input_cmd[0]

            # connect client
            if cmd == "@talk":

                chatt_PORT = int(input_cmd[2])

                chattSocket = socket(AF_INET, SOCK_STREAM)
                chattSocket.connect( ('', chatt_PORT) )

                connect_lst.append(chattSocket)

            # end chatt
            elif cmd == "@quit":
                is_end = 1
            
            # data send
            elif message:
                sendData = userID+" : "+message
                for sock in connect_lst:
                    if sock == sys.stdin or sock == serverSocket:
                        continue
                    # test
                    try:
                        sock.send(sendData.encode())
                    except:
                        sock.close()
                        connect_lst.remove(sock)

        else:
            recvData =  sock.recv(1024)

            if recvData:
                print(recvData.decode())

            else:
                print("Connection Closed {}".format(sock.fileno()))
                sock.close()
                connect_lst.remove(sock)                
            
                                                
serverSocket.close()
