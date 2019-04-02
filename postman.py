import socket
import time

BLOCK_URL_SUBJECT = 'Restrict Access'
BLOCK_URL_MESSAGE = 'User {} tried to access {}.'

class PostMan:
    def __init__(self,receiver):
        self.sender   = 'moh.ali.sadraei@ut.ac.ir'
        self.base64   = b'AG1vaC5hbGkuc2FkcmFlaQBUdXM6MTU5MzU3'
        self.receiver = receiver
        self.mailLog  = {}
    def send(self,subject,msg):
        mailserver = ("mail.ut.ac.ir", 25)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(mailserver)
        clientSocket.send('HELO mail.ut.ac.ir\r\n'.encode())
        auth = "AUTH PLAIN ".encode()+self.base64+"\r\n".encode()
        clientSocket.send(auth)
        clientSocket.send("MAIL FROM:<{}>\r\n".format(self.sender).encode())
        clientSocket.send("RCPT TO:<{}>\r\n".format(self.receiver).encode())
        clientSocket.send("DATA\r\n".encode())
        clientSocket.send("From:<{}>\r\n".format(self.sender).encode())
        clientSocket.send("To:<{}>\r\n".format(self.receiver).encode())
        clientSocket.send("Subject: {}\r\n\r\n".format(subject).encode())
        clientSocket.send(msg.encode())
        clientSocket.send("\r\n.\r\n".encode())
        clientSocket.send("QUIT\r\n".encode())
        while True:
            r = clientSocket.recv(1024)
            if not r:
                break
        clientSocket.close()
    def sendBlockedAccess(self,ip,url):
        msg = BLOCK_URL_MESSAGE.format(ip,url)
        t = time.time()
        sendFlag = True
        if msg in self.mailLog:
            if self.mailLog[msg] - t < 300:
                sendFlag = False
        if sendFlag:
            self.send(BLOCK_URL_SUBJECT,msg)
            self.mailLog[msg] = t
