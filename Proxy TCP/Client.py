from socket import *

proxy = '127.0.0.1'
port = 1234

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((proxy, port))

message = bytearray([15] * 5)
print('[==>] Sent request to proxy.')
clientSocket.send(message)

print('[...] Waiting for receive answer from server.')
response = clientSocket.recv(2048)
print('[<==] Receive answer from proxy.')
print(response.decode())

print('[*] Nothing to send. Closing conncection')
clientSocket.close()
