import socket
import threading

def proxyAgent(clientSocket, clientAddress):
	try:
		while True:
			httpRequest = clientSocket.recv(100000000).decode()
			if httpRequest:

				httpRequest = httpRequest.replace("1.1","1.0")

				first_line = httpRequest.split('\r\n')[0]
				url = first_line.split(' ')[1]
				http_pos = url.find("://") # find pos of ://
				if (http_pos==-1):
					temp = url
				else:
					temp = url[(http_pos+3):] # get the rest of url

				port_pos = temp.find(":") # find the port pos (if any)

				# find end of web server
				webserver_pos = temp.find("/")
				if webserver_pos == -1:
					webserver_pos = len(temp)

				webserver = ""
				port = -1
				if (port_pos==-1 or webserver_pos < port_pos):

					# default port
					port = 80
					webserver = temp[:webserver_pos]

				else: # specific port
					port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
					webserver = temp[:port_pos]
				print((webserver, port))


				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
					s.settimeout(50)
					s.connect((webserver, port))
					s.sendall(httpRequest.encode())
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
