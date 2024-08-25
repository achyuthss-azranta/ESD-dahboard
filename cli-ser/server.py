import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server\n'))
    while True:
        data = connection.recv(2048)
        if not data:
            break
        message_from_client = data.decode('utf-8')
        print('Client Says: ' + message_from_client)
        
    connection.close()

def send_messages_to_client(connection):
    while True:
        # Sending a message to the client
        message_to_client = input('Enter your message to the client: ')
        connection.sendall(str.encode(message_to_client))

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    
    # Start a thread to handle client messages
    start_new_thread(threaded_client, (Client, ))

    # Start another thread to handle server messages
    start_new_thread(send_messages_to_client, (Client, ))
    
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()