import socket
import os
from thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 65432
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

def codebreaker(input): #breaks the code and returns the right string
    return str(int(input)+1)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    while True:
        data = connection.recv(2048).decode('utf-8')
        if not data:
            break
        page=codebreaker(data)
        connection.sendall(page.encode(encoding='UTF-8'))
    print('Closed connection')
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()