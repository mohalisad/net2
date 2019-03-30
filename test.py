import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(('127.0.0.1',1234))
sock.listen(10)
while True:
	(clientSocket, client_address) = sock.accept() 
	print(clientSocket.recv(10000))
