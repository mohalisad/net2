import socket
import threading
from logman import LogMan
from reqman import RequsetMan
from configman import ConfigMan

CONFIG_FILE = 'config.json'

class ProxyMan:
    def __init__(self):
        self.conf = ConfigMan(CONFIG_FILE)
        self.log = LogMan(self.conf.getLogEnable(),self.conf.getLogFile())
        self.rqman = RequsetMan(self.conf.getInjectEnable(),self.conf.getInjectMsg())
    def run(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            sock.bind(('127.0.0.1',self.conf.getPort()))
            sock.listen(2500)
            while True:
                (clientSocket, clientAddress) = sock.accept()
                t = threading.Thread(target=self.proxyAgent,args=(clientSocket, clientAddress))
                t.daemon = True
                t.start()
    def proxyAgent(self,clientSocket, clientAddress):
        try:
            while True:
                httpRequest = clientSocket.recv(100000000)
                if httpRequest:
                    httpRequest,webserver, port = self.rqman.convert(httpRequest)
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
            pass
if __name__ == '__main__':
    ProxyMan().run()
