import json

DEFAULT_PORT       = 8080
DEFAULT_LOG_FILE   = "proxy.log"
DEFAULT_CACHE_SIZE = 100
DEFAULT_USER_AGENT = "My Proxy Server"
DEFAULT_INJECT_MSG = "DEFAULT_INJECT_MSG"

class ConfigMan:
    def __init__(self,fileName):
        with open(fileName) as confFile:
            self.data = json.load(confFile)

    def getPort(self):
        try:
            return int(self.data['port'])
        except:
            return DEFAULT_PORT

    def getLogEnable(self):
        try:
            return bool(self.data['logging']['enable'])
        except:
            return False

    def getLogFile(self):
        try:
            return str(self.data['logging']['logFile'])
        except:
            return DEFAULT_LOG_FILE

    def getCacheEnable(self):
        try:
            return bool(self.data['caching']['enable'])
        except:
            return False

    def getCacheSize(self):
        try:
            return int(self.data['caching']['size'])
        except:
            return DEFAULT_CACHE_SIZE

    def getPrivacyEnable(self):
        try:
            return bool(self.data['privacy']['enable'])
        except:
            return False

    def getPrivacyAgent(self):
        try:
            return str(self.data['privacy']['userAgent'])
        except:
            return DEFAULT_USER_AGENT

    def getRestrictEnable(self):
        try:
            return bool(self.data['restriction']['enable'])
        except:
            return False

    def getRestrictTarget(self):
        try:
            return list(self.data['restriction']['targets'])
        except:
            return []

    def getUsers(self):
        try:
            return list(self.data['accounting']['users'])
        except:
            return []

    def getInjectEnable(self):
        try:
            return bool(self.data['HTTPInjection']['enable'])
        except:
            return False

    def getInjectMsg(self):
        try:
            return str(self.data['HTTPInjection']['post']['body'])
        except:
            return DEFAULT_INJECT_MSG
