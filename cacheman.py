INFINITE = 9999999

class CacheMan:
    def __init__(self,enable,size):
        self.enable = enable
        self.size   = size
        self.length = 0
        self.useID  = 0
        self.cache  = {}

    def cache(self, request, response):
        if response.getHeader('Pragma') != 'no-cache' and response.getResponseState() == 200:
            if not url in self.cache:
                self.length += 1
            self.removeLRU()
            self[request.getFullURL()] = response
            self[request.getFullURL()].setUesID(self.getNextUseID())
            print("cached")
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

    def loadFromCache(self, request):
        pass
