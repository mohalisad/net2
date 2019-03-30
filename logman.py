from datetime import datetime

class LogMan:
    def __init__(self,fileName):
        self.fileName = fileName
    def __getLogTime(self):
        return datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
    def write(self,msg):
        with open(self.fileName,"a+") as logFile:
            logFile.write("[{}] {}\n".format(self.__getLogTime(),msg))
