class HTTPRequest:
    def __init__(self, httpReq, agent = None):
        host = ''
        loc = httpReq.find(b'\r\n\r\n')
        httpRequest = httpReq[:loc].decode().replace("HTTP/1.1","HTTP/1.0")
        lines = httpRequest.split('\r\n')
        self.fullURL = lines[0].split()[1]
        convertedReq = lines[0] + '\r\n'
        lines = lines[1:]
        for line in lines:
            pair = line.split(':')
            key = pair[0]
            if key == 'Host':
                host = pair[1].strip()
            if key != 'Proxy-connection' and key != 'Accept-Encoding' and key != 'If-Modified-Since' and key != 'If-None-Match':
                if key == 'User-Agent' and agent is not None:
                    convertedReq += 'User-Agent: ' + agent + '\r\n'
                else:
                    convertedReq += line + '\r\n'
        host = host.split(':')
        self.webserver = host[0]
        self.port = 80
        if len(host) > 1:
            self.port = int(host[1])
        self.httpRequest = convertedReq
        self.payload     = httpReq[loc+2:]

    def addToRequest(self,key,value):
        self.httpRequest += "{}: {}\r\n".format(key,value)

    def getWebServer(self):
        return self.webserver

    def getPort(self):
        return self.port

    def getFullURL(self):
        return self.fullURL

    def getHTTPRequest(self):
        return self.httpRequest

    def getEncodedRequest(self):
        return self.httpRequest.encode() + self.payload
