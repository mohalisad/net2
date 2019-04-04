from datetime import datetime
from time import mktime

class CacheMan:
    def __init__(self,enable,size):
        self.enable = enable
        self.size   = size
        cache = {}

    def cache(self, response, request):
        if self.enable and response.getHeader('pragma') != 'no-cache':
            if len(selfcache) == self.size:
                removeLRU()
            self.cache[request] = response, datetime.now()
    
    def removeLRU(self):
        min = float('Inf')
        key = None
        for k, val in self.cache.items():
            if val[1] < min:
                min = val[1]
                key = k
        del self.cache[key]
        
    def loadFromCache(self, request):
        if request in self.cache:
             expires = datetime.strptime(cache[request][0].getHeader('expires'), '%a, %d %b %Y %H:%M:%S %Z')
            if expires > datetime.now():
                cache[request] = cache[request][0], datetime.now()
                return cache[request][0]
            else:
                del cache[request]
                return 'EXPIRED'
        else:
            return 'NOT_FOUND'