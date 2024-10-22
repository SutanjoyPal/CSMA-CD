class Channel:
    def __init__(self, p,bandwidth, propagationTime):
        self.propagationTime = propagationTime
        self.bandwidth = bandwidth

        self.vulnerableTime = 0
        self.transmissionTime = 0

        self.busy = False
        self.sender = None
        self.p = p
    
    def reset(self):
        self.vulnerableTime = 0
        self.transmissionTime = 0
        self.busy = False
        self.sender = None
    
    