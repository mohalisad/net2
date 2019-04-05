class HTTPResponse:
    def __init__(self, packet):
        self.header  = {}
        headerLoc    = packet.find(b'\r\n\r\n')
        header       = packet[:headerLoc].decode().split('\r\n')
        self.header0 = header[0]
        header       = header[1:]
        for line in header:
            parts = line.split(';')
            for part in parts:
                pair = part.split(':')
                self.header[pair[0].strip()] = pair[1].strip()
        self.payload = packet[headerLoc+4:]ß
    def getHeader(self, key):
        if key in self.header:
            return self.header[key]
        return ""
    def setHeader(self, key, value):
        self.header[key] = value
    def getPayload(self):
        return self.payload
    def setPayload(self,payload):
        self.payload = payload
    def getEncodedHeader(self):
        header = self.header0 + '\r\n'
        for key,value in self.header.items():
            header += '{}: {}\r\n'.format(key,value)
        header += '\r\n'
        return header.encode()
    def getFullPacket(self):
        return self.getEncodedHeader() + self.payload
    def getResponseState(self):
        return int(self.header0.split()[1])
    def setUesID(self,useID):
        self.useID = useID
    def getUesID(self):
        return useID
