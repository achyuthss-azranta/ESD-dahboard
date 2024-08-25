import socket
from _thread import *

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
    print('Connected to the server')
except socket.error as e:
    print(str(e))

def receive_messages(ClientSocket):
    while True:
        try:
            # Receiving messages from the server
            Response = ClientSocket.recv(1024)
            if not Response:
                break
            print('\nServer Says: ' + Response.decode('utf-8'))
        except:
            # Handle any exceptions, such as connection closure
            break

# Start a thread to receive messages from the server
start_new_thread(receive_messages, (ClientSocket,))

while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    
    if Input.lower() == 'bye':
        break

ClientSocket.close()