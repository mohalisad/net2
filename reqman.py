class RequsetMan:
    def __init__(self,privacyMode,userAgent):
        self.enable    = privacyMode
        self.userAgent = userAgent
    def convert(self,httpReq):
        convertedReq = ''
        host = ''
        loc = httpReq.find(b'\r\n\r\n')
        httpRequest = httpReq[:loc].decode().replace("HTTP/1.1","HTTP/1.0")
        lines = httpRequest.split('\r\n')
        for line in lines:
            key = line.split(':')[0]
            if key == 'Host':
                host = line[line.index(':')+1:].strip()
            if key != 'Proxy-connection':
                if key == 'User-Agent' and self.enable:
                    convertedReq += 'User-Agent: ' + self.userAgent + '\r\n'
                else:
                    convertedReq += line + '\r\n'
        host = host.split(':')
        url = host[0]
        port = 80
        if len(host) > 1:
            port = int(host[1])
        return convertedReq.encode() + httpReq[loc+2:],url,port
