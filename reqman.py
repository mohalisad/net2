from httprequest import HTTPRequest

def urlConvert(url):
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

class RequsetMan:
    def __init__(self,privacyMode,userAgent,restrictEnable,restrictList):
        self.privacyEnable = privacyMode
        self.userAgent     = userAgent
        self.restrict      = restrictEnable
        self.blockNotify   = []
        self.block         = []
        for item in restrictList:
            if str(item['notify']).lower() == 'true':
                self.blockNotify.append(urlConvert(item['URL']))
            else:
                self.block.append(urlConvert(item['URL']))
    def convert(self,httpReq):
        if self.privacyEnable:
            request = HTTPRequest(httpReq,self.userAgent)
        else:
            request = HTTPRequest(httpReq)

        convertedURL = urlConvert(request.getWebServer())
        if self.restrict:
            if convertedURL in self.blockNotify:
                raise ValueError(True ,convertedURL,'blocked url')
            if convertedURL in self.block:
                raise ValueError(False,convertedURL,'blocked url')
        return request
