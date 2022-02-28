from socket import *
from threading import *

port = 5678
server = '127.0.0.1'

client_port = 1234
client_server = '127.0.0.1'

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((server, port))
serverSocket.listen(5)

print('[*] Server listening on (%s) : (%d)' % (server, port))


def handle_client(clientSocket):
    print('[...] waiting for received data from proxy:')
    received = clientSocket.recv(2048)
    print('[<==] Received %d bytes from proxy' % (len(received)))
    print(received.decode())
    clientSocket.sendall(b'ACK')
    print('[==>] Sent answer to proxy.')


while True:
    connectionSocket, address = serverSocket.accept()
    print('[*] Accepted connection from (%s):(%s)' % (address[0], address[1]))
    Thread(target=handle_client, args=(connectionSocket,)).start()

serverSocket.close()
