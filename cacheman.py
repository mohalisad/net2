INFINITE = 9999999

class CacheMan:
    def __init__(self,enable,size):
        self.enable = enable
        self.size   = size
        self.length = 0
        self.useID  = 0
        self.cache  = {}

    def addOrLoadCache(self, request, response):
        if response.getResponseState() == 304:
            return self.cache[request.getFullURL()]
        if response.getHeader('Pragma') != 'no-cache' and response.getResponseState() == 200:
            url = request.getFullURL()
            if not url in self.cache:
                self.length += 1
            self.removeLRU()
            self.cache[url] = response
            self.cache[url].setUesID(self.getNextUseID())
        return response
    def getNextUseID(self):
        self.useID += 1
        return self.useID

    def removeLRU(self):
        if self.length > self.size:
            mini = INFINITE
            mini_key = ''
            for key,value in self.cache.items():
                useID = value.getUesID()
                if useID < mini:
                    mini     = useID
                    mini_key = key
            del self.cache[key]
            self.length -= 1

    def isItInCache(self, request):
        if request.getFullURL() in self.cache:
            date = self.cache[request.getFullURL()].getHeader('Date')
            if date != '':
                request.addToRequest('If-Modified-Since',date)
                return True
        return False
