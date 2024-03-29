import socket
import threading
from logman       import LogMan
from reqman       import RequsetMan
from configman    import ConfigMan
from postman      import PostMan
from userman      import UserMan
from injectman    import InjectMan
from httpresponse import HTTPResponse
from cacheman     import CacheMan


REQUEST_LOG  = 'Proxy sent request to server with headers:\n\
----------------------------------------------------------------------\n{}\
----------------------------------------------------------------------'
RESPONSE_LOG  = 'Server sent response to proxy with headers:\n\
----------------------------------------------------------------------\n{}\
----------------------------------------------------------------------'
CONFIG_FILE  = 'config.json'
ADMIN_MAIL   = 'mohammadalisadraei@gmail.com'
RCV_MAX_SIZE = 10000
TIME_OUT     = 30

class ProxyMan:
    def __init__(self):
        conf          = ConfigMan(CONFIG_FILE)
        self.conf     = conf
        self.log      = LogMan(conf.getLogEnable(),conf.getLogFile())
        self.rqman    = RequsetMan(conf.getPrivacyEnable(),conf.getPrivacyAgent(),conf.getRestrictEnable(),conf.getRestrictTarget())
        self.post     = PostMan(ADMIN_MAIL)
        self.userMan  = UserMan(conf.getUsers())
        self.injector = InjectMan(conf.getInjectEnable(),conf.getInjectMsg())
        self.cache    = CacheMan(conf.getCacheEnable(),conf.getCacheSize())

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
                httpRequestBytes = clientSocket.recv(RCV_MAX_SIZE)
                if httpRequestBytes:
                    httpRequest = self.rqman.convert(httpRequestBytes)
                    cache_check = self.cache.isItInCache(httpRequest)
                    self.log.write('Proxy opening connection to server {} ... Connection opened.'.format(httpRequest.getWebServer()))
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(TIME_OUT)
                        s.connect((httpRequest.getWebServer(), httpRequest.getPort()))
                        s.sendall(httpRequest.getEncodedRequest())
                        self.log.write(REQUEST_LOG.format(httpRequest.getHTTPRequest()))
                        while True:
                            if self.userMan.getRemainingTraffic(clientAddress[0]) <= 0:
                                raise ValueError('no traffic')
                            data = s.recv(RCV_MAX_SIZE)
                            if (len(data) > 0):
                                rcvData += data
                                self.userMan.useTraffic(clientAddress[0],len(data))
                            else:
                                break
                        response = HTTPResponse(rcvData)
                        response = self.cache.addOrLoadCache(httpRequest,response)
                        response = self.injector.inject(response)
                        rcvData = response.getFullPacket()
                        clientSocket.send(rcvData)
                        self.log.write(RESPONSE_LOG.format(response.getFullHeader()))
                else:
                    break
        except ValueError as err:
            if len(err.args) == 3:
                if err.args[0] :
                    self.post.sendBlockedAccess(clientAddress[0],err.args[1])
        except:
            pass

        finally:
            clientSocket.close()


if __name__ == '__main__':
    ProxyMan().run()
