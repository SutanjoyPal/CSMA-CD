from channel import Channel

from station import Station

def perform_csma_cd(channel,stations, time):
    Time = time * 100

    total_bits_transmitted = 0
    collisionCount = 0
    total_transmissions = 0
    total_transmissions_started = 0

    with open('TransmissionDetails.txt', 'w') as TransmissionDetails:
        idleCnt = 0
        while Time > 0:
            channelJammed = False

            for _, station in stations.items():                                    #Station started sending Jam Signal
                if station.sendingJamSignal:
                    channelJammed  = True
                    TransmissionDetails.write(f"Jam Singal sent by {station.name}\n")
                    station.sendingJamSignal = False
                    break

            if channelJammed :                                                       
                Time-=1
                continue

            if not channel.busy:
                if channel.vulnerableTime > 0:
                    channel.vulnerableTime -= 1

                if channel.transmissionTime > 0:
                    channel.transmissionTime -= 1

                if channel.vulnerableTime == 0 and channel.sender:
                    channel.busy = True
                    TransmissionDetails.write("Enabling the busy bit \n")

                stationsReadyToSendList = []
                for _, station in stations.items():
                    if station.canSend():
                        stationsReadyToSendList.append(station)

                if channel.sender is None and len(stationsReadyToSendList) == 1:   #Only One station sending and channel is not sending 
                    total_transmissions_started+=1
                    channel.vulnerableTime = channel.propagationTime
                    channel.transmissionTime = stationsReadyToSendList[0].frameSize // channel.bandwidth#Calculation of transmissiontime

                    channel.sender = stationsReadyToSendList[0].name
                    stationsReadyToSendList[0].sending = True

                    TransmissionDetails.write(f"{stationsReadyToSendList[0].name} started sending packets in channel\n")

                elif stationsReadyToSendList:                                       #Collision happening here
                    if channel.sender:
                        TransmissionDetails.write(f"{channel.sender} paused transmission due to collision. ")
                        collisionCount+=1
                        stations[channel.sender].pauseTransmission()

                    TransmissionDetails.write("Exponential backoffs for: ")
                    for station in stationsReadyToSendList:
                        station.setExponentialBackoffTime()
                        TransmissionDetails.write(f"{station.name} ")
                    TransmissionDetails.write("\n")
                else:
                    idleCnt += 1
                    TransmissionDetails.write("----------------------------------Channel Idle-------------------------------------\n")
            else:
                if channel.transmissionTime > 0:                                 #Ongoing Transmission    
                    channel.transmissionTime -= 1

                if channel.transmissionTime == 0:
                    stations[channel.sender].count += 1
                    stations[channel.sender].sending = False
                    stations[channel.sender].droppedOffTime = 1

                    total_bits_transmitted += stations[channel.sender].frameSize
                    total_transmissions += 1

                    channel.sender = None
                    channel.busy = False                        #Disable busy bit
                    TransmissionDetails.write("Transmission successful!\n")  
                else:
                    idleCnt += 1
                    TransmissionDetails.write("----------------------------------Channel Idle-------------------------------------\n")

            Time -= 1
        
        simulation_time = time * 1000  
        throughput = total_bits_transmitted / simulation_time 
        print('\n')
        print(f"Throughput: {throughput} bits/ms")
        percentIdle = idleCnt / simulation_time
        print(f"Percentage of idle time: {percentIdle * 100}%")
        CollisionProbability = collisionCount / total_transmissions_started
        print(f"Probability of collision: {CollisionProbability}")
        print('\n')

         

probability = float(input("Enter probability of p-persistent CSMA/CD (between 0 and 1):"))
channel = Channel(p=probability,bandwidth=2000, propagationTime=10)
stations = {}


n = int(input("Enter number of stations: "))
while(n > 0):
    name = input("Enter Station Name: ")
    frameSize = int(input("Enter frame size in bits: "))
    stations[name] = Station(name=name,channel=channel,frameSize=frameSize)
    n =  n - 1
perform_csma_cd(channel,stations, time=5)

for name, station in stations.items():
    print(f'{name} successfully transmitted {station.count} packets')