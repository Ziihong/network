from socket import *
import os
import sys

myPort = int(sys.argv[1])

print("Student ID: 20191572")
print("Name: Kimjihong")

mySocket = socket(AF_INET,SOCK_STREAM)
mySocket.bind( ('', myPort) )
mySocket.listen(1)


while True:

    connectionSocket, addr = mySocket.accept()

    IP = addr[0]
    port = addr[1]

    req_header = connectionSocket.recv(1024)
    
    print("Connection: Host IP {}, Port {}, socket {}" .format(IP, port, connectionSocket.fileno()))
    print(req_header.decode())

    html_file = str(req_header.split(b'\r\n')[0].decode().replace('/',' ').split()[1])

    if os.path.isfile(html_file):

        file_data = os.path.getsize(html_file)

        res_header = "HTTP/1.0 200 OK\nConnection: close\nContent-Length:{}\nContent-Type: text/html\n\n".format(file_data)
        connectionSocket.send(res_header.encode())

        try:
            f = open(html_file, 'r')
        except:
            print("file open error")
            continue

        r = f.read()
        f.close()
        
        send_data = 0
        send_data += connectionSocket.send(r.encode())

        print("{} headers".format(req_header.decode().count('\r\n')-2))
        print("finish", send_data, file_data)    # 값 비교

    else:
        res_header = "HTTP/1.0 404 NOT FOUND\nConnection: close\nContent-Length: 0\nContent-Type: text/html\n\n"
        connectionSocket.send(res_header.encode())

        print("{} headers".format(req_header.decode().count('\r\n')-2))
        print("Server Error : No such file ./{}!" .format(html_file))
    

mySocket.close()