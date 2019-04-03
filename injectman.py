HTML       = '<div style="{}">{}</div>'
BACKGROUND = 'black'
FOREGROUND = 'yellow'
FONT_SIZE  = '20px'
STYLE = 'text-align:right;position: -webkit-sticky;\
position: sticky;top: 0;color:{};background-color:{};\
font-size:{};z-index: 999999;padding:10px;'

class InjectMan:
    def __init__(self,injectEnable,injectMsg):
        self.enable   = injectEnable
        self.msg      = injectMsg
        myStyle       = STYLE.format(FOREGROUND,BACKGROUND,FONT_SIZE)
        self.html_msg = HTML.format(myStyle,injectMsg).encode()

    def inject(self,response):
        if self.enable:
            if response.getResponseState() == 200:
                if response.getHeader('Content-Type').find('html') != -1:
                    payload = response.getPayload()
                    body_loc = payload.find(b'body')
                    if body_loc != -1:
                        length = response.getHeader('Content-Length')
                        if length != "":
                            try:
                                length = int(length) + len(self.html_msg)
                                response.setHeader('Content-Length',str(length))
                            except:
                                pass
                        body_loc += payload[body_loc:].find(b'>') + 1
                        payload = payload[:body_loc] + self.html_msg + payload[body_loc:]
                        response.setPayload(payload)
        return response
