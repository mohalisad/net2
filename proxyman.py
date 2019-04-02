import socket
import threading
from logman    import LogMan
from reqman    import RequsetMan
from configman import ConfigMan
from postman   import PostMan

CONFIG_FILE = 'config.json'
ADMIN_MAIL  = 'mohammadalisadraei@gmail.com'

class ProxyMan:
    def __init__(self):
        conf       = ConfigMan(CONFIG_FILE)
        self.conf  = conf
        self.log   = LogMan(conf.getLogEnable(),conf.getLogFile())
        self.rqman = RequsetMan(conf.getInjectEnable(),conf.getInjectMsg(),conf.getRestrictEnable(),conf.getRestrictTarget())
        self.post  = PostMan(ADMIN_MAIL)

        self.log.write('Proxy launched')
    def run(self):
        self.log.write('Creating server socket...')
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.log.write('Binding socket to port {}...'.format(self.conf.getPort()))
            sock.bind(('127.0.0.1',self.conf.getPort()))
            sock.listen(2500)
            self.log.write('Listening for incoming requests...')
            while True:
                (clientSocket, clientAddress) = sock.accept()
                t = threading.Thread(target=self.proxyAgent,args=(clientSocket, clientAddress))
                t.daemon = True
                t.start()
    def proxyAgent(self,clientSocket, clientAddress):
        self.log.write('Accepted a request from client!')
        try:
            while True:
                rcvData = bytes()
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
                                rcvData += data
                            else:
                                break
                        clientSocket.send(rcvData)
                else:
                    break
        except ValueError as err:
            if err.args[0] :
                self.post.sendBlockedAccess(clientAddress[0],err.args[1])
        except:
            pass
        finally:
            clientSocket.close()
if __name__ == '__main__':
    ProxyMan().run()
