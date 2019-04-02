from socket import *
import base64
import time
class PostMan:
    def __init__(self):
        self.sender = 'moh.ali.sadraei@ut.ac.ir'
        self.base64 = b'AG1vaC5hbGkuc2FkcmFlaQBUdXM6MTU5MzU3'
    def send(self,subject,msg,receiver):
        mailserver = ("mail.ut.ac.ir", 25)
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(mailserver)
        clientSocket.send('HELO mail.ut.ac.ir\r\n'.encode())
        auth = "AUTH PLAIN ".encode()+self.base64+"\r\n".encode()
        clientSocket.send(auth)
        clientSocket.send("MAIL FROM:<{}>\r\n".format(self.sender).encode())
        clientSocket.send("RCPT TO:<{}>\r\n".format(receiver).encode())
        clientSocket.send("DATA\r\n".encode())
        clientSocket.send("From:<{}>\r\n".format(self.sender).encode())
        clientSocket.send("To:<{}>\r\n".format(receiver).encode())
        clientSocket.send("Subject: {}\r\n\r\n".format(subject).encode())
        clientSocket.send(msg.encode())
        clientSocket.send("\r\n.\r\n".encode())
        clientSocket.send("QUIT\r\n".encode())
        while True:
            r = clientSocket.recv(1024)
            if not  r:
                break
        clientSocket.close()
