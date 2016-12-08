import csv
import math
import datetime
pathToFile = "WiFiDirectLocationLogCSV.csv"
secondsToMilli = 1000.0

def parseTime(floatingTime):
    return datetime.datetime.fromtimestamp(floatingTime).strftime('%M%S%f')

def isThresholdTimeDifference (timeOne, timeTwo):
    diff = (math.fabs(int(timeOne) - int(timeTwo)) / secondsToMilli)
    if diff >= 1:
        return True
    else:
        return False


def getTsAndRs (rawData):
    array = str(rawData).split(',')
    return array[0][2:], array[9]




speedLog = open ('WD_Speed_CSV.csv', 'w')
speedLog.write('Time(s),Speed(mi/hr)')
with open (pathToFile, 'rU') as csvfile:
    reader = csv.reader(csvfile, dialect=csv.excel_tab)

    totalSpeed = 0
    speedCounter = 0
    refTs= 0
    packetsInInterval = 0
    for row in reader:
        ts, rs = getTsAndRs(row)
        deltaTime = math.fabs(int(refTs) - int(ts)) / secondsToMilli
        isGreaterThanOne = isThresholdTimeDifference(refTs, ts)
        speedCounter += 1  # increment the speed counter
        totalSpeed += float(rs)

        if isGreaterThanOne:  # if the difference greater than one second?
            timeBin = int(refTs) / int(secondsToMilli)
            speedLog.write( str(timeBin) + ',' + str(totalSpeed/speedCounter) + '\n' )
            speedCounter = 0
            totalSpeed = 0
            packetsInInterval = 0
            refTs = ts
        else:
            packetsInInterval += 1  # Increase the number of packets in interval


speedLog.close()
