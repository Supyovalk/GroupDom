import socket

HOST = '127.0.0.1'
PORT = 65432

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(s.recv(1024).decode())
s.send(b'123')
data = s.recv(1024)
s.close()

print('Received', repr(data))