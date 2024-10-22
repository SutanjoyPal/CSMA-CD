import random

class Station:
    def __init__(self, name, channel,frameSize):
        self.name = name
        self.frameSize = frameSize
        self.channel = channel
    
        self.readyToSend = True
        self.waitingTime = 0
        self.droppedOffTime = 0
        self.k = 0
        self.sendingJamSignal = False
        self.count = 0
        self.sending = False

    

    def canSend(self):
        if self.sending:
            return False
        elif self.droppedOffTime > 0:
            self.droppedOffTime -= 1
            return False
        elif self.waitingTime == 0 and not self.channel.busy:
            if random.random() < self.channel.p:  #p-persistence
                return True
            else:
                return False
        elif self.waitingTime > 0:
            self.waitingTime -= 1
            return False
        else:
            self.setExponentialBackoffTime()

    def pauseTransmission(self):
        self.channel.vulnerableTime = 0
        self.channel.sender = None
        self.sendingJamSignal = True
        self.sending = False
        self.setExponentialBackoffTime()

    def setExponentialBackoffTime(self):
        if self.k < 15:
            self.k += 1
            self.waitingTime = random.randint(0, 2 ** self.k - 1)
        else:
            self.k = 0
            self.droppedOffTime = 5