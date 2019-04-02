HTML  = '<div style="{}">{}</div>'
STYLE = 'text-align:right;position: -webkit-sticky;\
position: sticky;top: 0;color: yellow;background-color: black;\
font-size: 20px;z-index: 999999;padding:10px;'

class InjectMan:
    def __init__(self,injectEnable,injectMsg):
        self.enable   = injectEnable
        self.msg      = injectMsg
        self.html_msg = HTML.format(STYLE,injectMsg).encode()

    def inject(self,packet):
        if self.enable:
            headerLoc   = packet.find(b'\r\n\r\n')
            header      = packet[:headerLoc].decode()
            payload     = packet[headerLoc+2:]
            html_loc    = header.find('html')
            if html_loc != -1:
                body_loc    = payload.find(b'body')
                if body_loc != -1:
                    header = header.split('\r\n')
                    if int(header[0].split()[1]) == 200:
                        new_header = ""
                        for line in header:
                            key = line.split(':')[0]
                            if key == 'Content-Length':
                                length =  int(line.split(':')[1])
                                length += len(self.html_msg)
                                new_header += 'Content-Length: {}\r\n'.format(length)
                            else:
                                new_header += line + '\r\n'
                        body_loc += payload[body_loc:].find(b'>') + 1
                        payload = payload[:body_loc] + self.html_msg + payload[body_loc:]
                        print(new_header)
                        return new_header.encode() + payload
        return packet
