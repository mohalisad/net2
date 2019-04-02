from socket import *
import base64
import time

def send_mail(subject,msg,receiver):
    sender = 'moh.ali.sadraei@ut.ac.ir'
    mailserver = ("mail.ut.ac.ir", 25)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(mailserver)
    clientSocket.send('HELO mail.ut.ac.ir\r\n'.encode())
    base64_str = b'AG1vaC5hbGkuc2FkcmFlaQBUdXM6MTU5MzU3'
    auth = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    clientSocket.send(auth)
    clientSocket.send("MAIL FROM:<{}>\r\n".format(sender).encode())
    clientSocket.send("RCPT TO:<{}>\r\n".format(receiver).encode())
    clientSocket.send("DATA\r\n".encode())
    clientSocket.send("From:<{}>\r\n".format(sender).encode())
    clientSocket.send("To:<{}>\r\n".format(receiver).encode())
    clientSocket.send("Subject: {}\r\n\r\n".format(subject).encode())
    clientSocket.send(msg.encode())
    clientSocket.send("\r\n.\r\n".encode())
    clientSocket.send("QUIT\r\n".encode())
    clientSocket.close()
send_mail('hello asdsadworld','hiasdsaf2',"mohammadalisadraei@gmail.com")
