class RequsetMan:
    def __init__(self,privacyMode,userAgent,restrictEnable,restrictList):
        self.privacyEnable = privacyMode
        self.userAgent     = userAgent
        self.restrict      = restrictEnable
        self.blockNotify   = []
        self.block         = []
        for item in restrictList:
            if str(item['notify']).lower() == 'true':
                self.blockNotify.append(self.__urlConvert(item['URL']))
            else:
                self.block.append(self.__urlConvert(item['URL']))
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
            if key != 'Proxy-connection' and key != 'Accept-Encoding':
                if key == 'User-Agent' and self.privacyEnable:
                    convertedReq += 'User-Agent: ' + self.userAgent + '\r\n'
                else:
                    convertedReq += line + '\r\n'
        host = host.split(':')
        url = host[0]
        port = 80
        if len(host) > 1:
            port = int(host[1])
        convertedURL = self.__urlConvert(url)
        if self.restrict:
            if convertedURL in self.blockNotify:
                raise ValueError(True ,convertedURL,'blocked url')
            if convertedURL in self.block:
                raise ValueError(False,convertedURL,'blocked url')
        return convertedReq.encode() + httpReq[loc+2:],url,port
    def __urlConvert(self,url):
        url     = str(url).lower()
        wwwLoc  = url.find('www.')
        httpLoc = url.find('http://')
        if wwwLoc != -1:
            wwwLoc += 4
            url = url[wwwLoc:]
        else:
            if httpLoc != -1:
                httpLoc += 7
                url = url[httpLoc:]
        end = url.find('/')
        if end != -1:
            url = url[:end]
        return url
