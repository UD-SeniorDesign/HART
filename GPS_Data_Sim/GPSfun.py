# GPSsim
# By: Jason Reynolds
# 
# Punchlist: make time increment adjustable to fit sample times.
# 

# Importing dependencies
from math import sin, cos, sqrt, atan2, radians
import pprint as pp
import datetime
import time
import csv
import sys, traceback
import json
import re


# Function definitions
def isValidTimeFormat(userDate,userTime):
    """ Confirms that string passed in is of valid format.
        Parameter(s): userDate (string), a string representing date, expected to be formatted as: YYYY-MM-DD
                      userTime (string), a string representing time, expected to be formatted as: HH:MM:SS
        Return(s): True (boolean) or exits program with message displaying expected datetime format.
    """

    try:
        # checking for date validity 
        if (userDate[4] != '-'):
            sys.exit("Invalid datetime format. Should be: YYYY-MM-DD HH:MM:SS |0")
        if (userDate[7] != "-"):
            sys.exit("Invalid datetime format. Should be: YYYY-MM-DD HH:MM:SS |1")

        # checking for time validity
        if (userTime[2] != ':'):
            sys.exit("Invalid datetime format. Should be: YYYY-MM-DD HH:MM:SS |2")
        if (userTime[5] != ":"):
            sys.exit("Invalid datetime format. Should be: YYYY-MM-DD HH:MM:SS |3")

    except Exception as e:
        # if any errors, exit
        sys.exit("Invalid datetime format. Should be: YYYY-MM-DD HH:MM:SS |5")
        # sys.exit(traceback.print_tb(e.__traceback__))
    return True

def getTime():
    """ Gets initial time to use for the GPS path.
        Parameter(s): none
        Return(s): currentTime, string. datetime representation in form YYYY-MM-DD HH:MM:SS
    """
    # Check user input option for time
    if ('-t' in sys.argv):
        userTimeInputIndex = sys.argv.index('-t')+2
        userDateInputIndex = sys.argv.index('-t')+1
        currentTime = sys.argv[userTimeInputIndex]
        currentDate = sys.argv[userDateInputIndex]
        isValidTimeFormat(currentDate,currentTime)
    else:
        currentDate = str(datetime.datetime.now())[:10]
        currentTime = str(datetime.datetime.now())[11:-7]
    return currentDate,currentTime

def incrDay(theDate):
    """ Increments the value of a date ***DOES NOT SUPPORT MONTH OR YEAR ROLLOVER*** 
        Parameter(s): theDate, string, of format YYYY-MM-DD
        Return(s): newDate, string, of format YYYY-MM-DD
    """
    thirties = {4,6,9,11}
 
    year = int(theDate[:4])
    month = int(theDate[5:7])
    day = int(theDate[-2:])  
    day += 1
    
    if ((day == 29) and (month == 2)):
        day = 1
        month += 1

    elif ((month in thirties) and (day == 31)):
        day = 1
        month += 1

    elif ((month not in thirties) and (day == 32)):
        day = 1
        if (month != 12):
            month += 1

        else:
            month = 1
            year += 1

    if (month<10):
        month = '0'+str(month)

    if (day < 10):
        newDate = str(year)+"-"+str(month)+"-"+"0"+str(day)
    elif (day > 10):
        newDate = str(year)+"-"+str(month)+"-"+str(day)
    return newDate

def pullInCSV(filename):
    """ Pulls in lat, long and datetime from csv.
        Parameter(s): filename, string, specifies the file to be read in.
        return(s): dataArr, array of strings. An array of the data read in from the csv.
    """

    dataArr = []
    
    with open(filename,'r') as trainingData:
        new_reader = csv.reader(trainingData)
        for line in new_reader:
            dataArr.append(line)
        for record in dataArr:
            for i in range(len(record)):
                if i<2:
                    record[i]=float(re.sub('[^0-9,\-,\.]','',record[i]))
                else:
                    record[i]=int(record[i])
        trainingData.close()

        return dataArr
    

def timeIncrement(currentTime,currentDate):
    """ Increments the time value by one second.
        Parameter(s): currentTime, string, represents time in the format: HH:MM:SS
        Return(s): currentDate, string, represents date in the format: YYYY-MM-DD
    """
    tempSec = int(currentTime[-2:])
    tempMin = int(currentTime[-5:-3])
    tmpHr = int(currentTime[-8:-6])
    
    tempSec+=1

    if (tempSec==60):
        tempMin+=1
        tempSec = 0
        if (tempMin==60):
            tmpHr+=1
            tempMin=0
            if(tmpHr==24):
                tmpHr=0
                currentDate=incrDay(currentDate)
            
    
    if (tempSec<10):
        tempSec = "0"+str(tempSec)
    if (tempMin<10):
        tempMin = "0"+str(tempMin)
    if (tmpHr<10):
        tmpHr = "0"+str(tmpHr)


    returnTimeString = (str(tmpHr) + ":" + str(tempMin) + ":" + str(tempSec))

    return(returnTimeString,currentDate)



def genGPSdata(numStops,stopLocationArray,startDate,startTime,samplesPerHour):
    GPSdataArray = []
    locOne = [0,0,0] #lat,long, speed after this point
    locTwo = [0,0,0]
    latDif = 0
    longDif = 0
    latSampleIncr = 0
    longSampleIncr = 0
    sampleLat = 0
    sampleLong = 0
    # distance = 0 #km
    time = 0 #in minutes
    numSample = 0
    currentTime = startTime
    currentDate = startDate
    timeSample = 0
    timeIncr = 1

    for stop in range(1,numStops):
        locOne = stopLocationArray[stop-1]
        locTwo = stopLocationArray[stop]
        # distance = getDistance(locOne[0],locOne[1],locTwo[0],locTwo[1])
        time = locOne[2]
        numSample = round(time*samplesPerHour)

        latDif = locTwo[0]-locOne[0]
        longDif = locTwo[1]-locOne[1]

        latSampleIncr = latDif/numSample
        longSampleIncr = longDif/numSample
        
        sampleLat = locOne[0]
        sampleLong = locOne[1]
        
        for s in range(numSample):
            currentTime,currentDate=timeIncrement(currentTime,currentDate)
            sampleLat += latSampleIncr
            sampleLong += longSampleIncr
            timeSample += timeIncr
            GPSdataArray.append([sampleLat,sampleLong,currentTime])
    
    # print(GPSdataArray)
    return GPSdataArray



def getDistance(latOne,longOne,latTwo,longTwo):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(latOne)
    lon1 = radians(longOne)
    lat2 = radians(latTwo)
    lon2 = radians(longTwo)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


# Gather neccesary inputs and establish global variables
inFile = sys.argv[1]
date,time = getTime()
stopArr = pullInCSV(inFile)
numStops = len(stopArr)
samples = 60

finalTrainingDataOut = genGPSdata(numStops,stopArr,date,time,samples)
# pp.pprint(finalTrainingDataOut)

outFile = str(datetime.datetime.now())[:-4].replace(" ","_t").replace(":","-").replace(".","-")+ inFile.replace("dataIn/","_")

fOut = open('dataOut/CSV/GPSsimV0_d'+ outFile,'w')
for line in finalTrainingDataOut:
    fOut.write(str(line).replace("[","").replace("]","")+"\n")
fOut.close()



csvfile = open('dataOut/CSV/GPSsimV0_d'+ outFile, 'r')
jsonfile = open('dataOut/JSON/GPSsimV0_d'+outFile[:-4]+'.json', 'w')

fieldnames = ("Latitude","Longitude","Time")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')