# socket 과 select 모듈 임포트
from socket import *
from select import *
import sys

myPort = int(sys.argv[1])

print("Student ID: 20191572")
print("Name: Kimjihong")

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind( ('', myPort) )
serverSocket.listen()

connect_lst = [serverSocket]
descriptor_dict = {}

while connect_lst:

    #select로 요청 받기
    read_socket, write_socket, error_socket = select(connect_lst, [], [])

    for sock in read_socket:
        # 새로운 client 접속
        if sock == serverSocket:
            clientSocket, addr = serverSocket.accept()

            IP = addr[0]
            PORT = addr[1]

            print("Connection from host {}, port {}, socket fd {}" .format(IP, PORT, clientSocket.fileno()))

            connect_lst.append(clientSocket)
            descriptor_dict[clientSocket] = clientSocket.fileno() # dic[clientSocket] : descriptor

            
        # 기존 client send message 
        else:
            message = sock.recv(1024)
            if message:
                for socket_item in connect_lst:
                    # serverSocket과 자신의 Socket이 아니라면
                    if socket_item != serverSocket and socket_item != sock:
                        socket_item.send(message)

            else:
                descriptor = descriptor_dict.get(sock)
                sock.close()
                connect_lst.remove(sock)
                del descriptor_dict[sock]
                print('Connection closed {}'.format(descriptor))

serverSocket.close()
