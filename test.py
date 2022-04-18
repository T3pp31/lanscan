import socket
hostname = socket.gethostbyaddr('192.168.1.1')[0]
print(hostname)