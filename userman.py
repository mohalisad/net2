class UserMan:
    def __init__(self,users):
        self.users = {}
        for user in users:
            self.users[str(user["IP"])] = int(user["volume"])
    def getRemainingTraffic(self,ip):
        if ip in self.users:
            return self.users[ip]
        return -1
    def useTraffic(self,ip,amount):
        if ip in self.users:
            self.users[ip] -= amount
