import socket
import threading
from logman import LogMan
from reqman import RequsetMan

log = LogMan('aaa.log')
rqman = RequsetMan(True,'Hello World')
def proxyAgent(clientSocket, clientAddress):
	global log
	global rqman
	try:
		while True:
			httpRequest = clientSocket.recv(100000000)
			if httpRequest:
				httpRequest,webserver, port = rqman.convert(httpRequest)
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
					s.settimeout(50)
					s.connect((webserver, port))
					s.sendall(httpRequest)
					while True:
						data = s.recv(100000000)
						if (len(data) > 0):
							clientSocket.send(data)
						else:
							break
			else:
				break
	except:
		pass
	finally:
		print("dead")

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock.bind(('127.0.0.1',8080))
	sock.listen(2500)
	while True:
		(clientSocket, clientAddress) = sock.accept()
		print ("New user")
		t = threading.Thread(target=proxyAgent,args=(clientSocket, clientAddress))
		t.daemon = True
		t.start()
