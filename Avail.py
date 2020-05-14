class Avail(object):
    def __init__(self):
        self.AvailC = 0
        self.Temp = "t"

    def next(self):
        self.AvailC+=1
        return self.Temp + str(self.AvailC)

    def reset(self):
        self.AvailC = 0