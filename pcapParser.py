import dpkt
import datetime
import math

pathToFile = "/Users/fawadahmad/Google Drive/PhD Courses/651-Advanced Computer Networking/" \
             "Research Project/Experiment Results/Relative_Car_Motion_Experiments/2nd_Dec_Combined_Experiments/" \
             "ReceiverApp/LTE/"

importFileName = "LTE_Only_Receiver_Dump.pcap"
exportFileName = 'LTE_Receiver_TcpLog.csv'



pcapFile = open (pathToFile + importFileName)
parsedFile = dpkt.pcap.Reader (pcapFile)
counter = 0
secondsToMilli = 1000000.0
packetsInInterval = 0

def parseTime(floatingtime):
    return datetime.datetime.fromtimestamp(floatingtime).strftime('%M%S%f')

def isThresholdTimeDifference (timeOne, timeTwo):
    diff = (math.fabs(int(timeOne) - int(timeTwo)) / secondsToMilli)
    if diff >= 1:
        #print "Diff for " + str(timeOne) + " and " + str(timeTwo) + " = " + str(diff)
        return True
    else:
        pass
        #print "Difference for " + str(timeOne) + " and " + str(timeTwo) + " = " + str(diff)


refTime = 0
outputLog = open (pathToFile + exportFileName, 'w')

outputLog.write('Time,Packets/Second')

for ts, buf in parsedFile:
    currentTimeStamp = parseTime(ts)
    deltaTime = math.fabs(int(refTime)-int(currentTimeStamp))/secondsToMilli

    isGreaterThanOne = isThresholdTimeDifference(refTime, currentTimeStamp)

    if isGreaterThanOne:  # if the difference greater than one second?
        timeBin = int(refTime) / int(secondsToMilli)
        outputLog.write( str(timeBin) + ',' + str(packetsInInterval) + '\n')
        packetsInInterval = 0
        refTime = currentTimeStamp
    else:
        packetsInInterval += 1 # Increase the number of packets in interval

    counter += 1

print "All done"
print counter

