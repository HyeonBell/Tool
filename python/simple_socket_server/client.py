import socket
import json


HOST = '127.0.0.1'
PORT = 8820
CLIENT_IP = socket.gethostbyname(socket.getfqdn())
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

send_data = "IP : " + CLIENT_IP + " data : " + "안녕하세요"

client_socket.sendall(send_data.encode())

data = client_socket.recv(1024)
print("Received", repr(data.decode()))

client_socket.close()