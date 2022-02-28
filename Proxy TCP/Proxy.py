from socket import *
from threading import *
import sys

self_port = 1234
self_server = '127.0.0.1'

port = 5678
server = '127.0.0.1'


def request_handler(buffer):
    return buffer


def response_handler(buffer):
    return buffer


def receive_from(connection):
    data = ""
    connection.settimeout(20)
    try:
        while True:
            data = connection.recv(2048)
            if not data:
                break
            data =+ data
    except Exception as e:
        print('error', e)
        pass
    return data


def proxy_handler(clientSocket, server, port):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect((server, port))

    while True:
        client_buffer = receive_from(clientSocket)
        server_buffer = receive_from(serverSocket)

        if len(client_buffer):
            print('[...] waiting for received request from client:')
            print('[<==] Received %d bytes from client' % (len(client_buffer)))
            message = client_buffer.decode('utf-8')
            print(message)

            client_buffer = request_handler(client_buffer)
            serverSocket.sendall(client_buffer)
            print('[==>] Sent request to server.')
            print('[...] waiting for received answer from server:')
            server_buffer = receive_from(serverSocket)

            if len(server_buffer):
                print('[<==] Received %d bytes from server' % (len(server_buffer)))
                print(server_buffer.decode('utf-8'))

                server_buffer = response_handler(server_buffer)
                clientSocket.sendall(server_buffer)
                print('[==>] Sent answer to client.')
            client_buffer = receive_from(clientSocket)

        if not len(client_buffer) or not len(server_buffer):
         
            print('[*] No more data in the buffer. Closing connections.')
            clientSocket.close()
            serverSocket.close()
            break


def server_loop(self_server, self_port, server, port):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    try:
        serverSocket.bind((self_server, self_port))
    except Exception as e:
        print(' [!!] Failed to listen on (%s) : (%d)' % (self_server, self_port))
        print(e)
        sys.exit(0)

    print('[*] Listening on (%s) : (%d)' % (self_server, self_port))
    serverSocket.listen(10)
    while True:
        connectionSocket, address = serverSocket.accept()
        print('> Received incoming connection from (%s):(%s)' % (address[0], address[1]))
     
        Thread(target=proxy_handler, args=(connectionSocket, server, port)).start()


server_loop(self_server, self_port, server, port)
