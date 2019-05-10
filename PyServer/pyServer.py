##########################################################################################
# By: J. K. Reynolds
##########################################################################################

# Import libraries
import http.server
import time
import sys, subprocess
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime as dt
from datetime import timedelta as td
import threading
from threading import Timer,Thread,Event
import glob
import csv
from google.protobuf import json_format
from google.transit import gtfs_realtime_pb2


##########################################################################################
# CONSTANTS
##########################################################################################
tick = 0
prevTickTime = dt.now()
demoLoopData = []
currentOpenSkyRecord = ""
currentSatelliteRecord = ""
currentMTARecord = ""
lomin = '0'
lomax = '0'
lamin = '0'
lamax = '0'

# Satellites
centerLat = '0'
centerLng = '0'
satRadius = '0'

# MTA stuff
CITY_GRIDS = [['newyork',40.492014,40.924276,-74.269512,-73.737244]]
MTA_API_KEY = "d8d8bf77573b91e6462358cf6ec5a755"
MTA_FEED_IDS = ["1","26","16","21","2","11","31","36","51"]
MTA_ENDPOINT = "http://datamine.mta.info/mta_esi.php?key=" + MTA_API_KEY + "&feed_id="

##########################################################################################
# FUNCTIONS
##########################################################################################
class tickThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global tick
        # global currentOpenSkyRecord
        while not self.stopped.wait(1):
            print(str(tick) + " | " + str(dt.now()))
            tick += 1
            #print(currentOpenSkyRecord)

class openSkyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global currentOpenSkyRecord
        while not self.stopped.wait(10):
            openSkyFetchThread()

class satelliteThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global currentSatelliteRecord
        while not self.stopped.wait(5):
            satelliteFetchThread()

class mtaThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global currentMTARecord
        while not self.stopped.wait(5):
            mtaFetchThread()

def getOpenSkyInfo(lomin,lomax,lamin,lamax):
    laminStr = 'lamin=' + str(lamin) + '&'
    lamaxStr = 'lamax=' + str(lamax) + '&'
    lominStr = 'lomin=' + str(lomin) + '&'
    lomaxStr = 'lomax=' + str(lomax)

    r = requests.get('https://opensky-network.org/api/states/all?' + laminStr + lamaxStr + lominStr + lomaxStr)
    return r.json()

def getSatInfo(cLat,cLng,satRad):
    r = requests.get("https://www.n2yo.com/rest/v1/satellite/above/" + cLat + "/" + cLng + "/0/" + satRad + "/0/&apiKey=J63CHM-KJQD9M-D3BECE-3YXH")
    return r.json()['above']

def getMTAInfo():
    print("GETTING MTA INFO")
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(MTA_ENDPOINT+MTA_FEED_IDS[1])
    feed.ParseFromString(response.content)
    trainLst = []

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            if ( entity.trip_update.stop_time_update):
                trainLst.append([entity.id,entity.trip_update.trip.trip_id, entity.trip_update.stop_time_update])


    # print(trainLst)
    return trainLst

def readStations():
    fin = open("MTA_stations.csv","r")
    lines = fin.readlines()
    fin.close()
    return lines    

def parseStations(lines):
    stationLocations = []
    for line in lines:
        tmpLine = line.strip('\n').split(",")
        stationLocations.append([tmpLine[2],tmpLine[5],tmpLine[-2],tmpLine[-1]])

    return stationLocations


def readDemoLoopDataFromFile():
    fin = open("Data/fly-madison_GPSsimV0_d2018-12-03_t22-20-2.json",'r')
    demoData = fin.read()
    fin.close()
    dd = demoData[1:-1].split('\n')
    ddl = len(dd)
    print("Read in " + str(ddl) + " lines of demo data.")
    return dd,ddl

# Reads in the error html
def readInNope():
    fin = open("nope.html")
    nope = fin.read()
    fin.close()
    # print(nope)
    return nope

# Reads in the readme html
def readInReadMe():
    fin = open("readme.html")
    readme = fin.read()
    fin.close()
    # print(readme)
    return readme

# Define run behavior
def run():
    print(time.asctime(),"Server Started - %s:%s" % (hostName,hostPort))
    print("server:",handler.server_version,"system:",handler.sys_version)

    tickStopFlag = Event()
    tThread = tickThread(tickStopFlag)
    tThread.start()

    openSkyStopFlag = Event()
    osThread = openSkyThread(openSkyStopFlag)
    osThread.start()

    satelliteStopFlag = Event()
    satThread = satelliteThread(satelliteStopFlag)
    satThread.start()

    mtaStopFlag = Event()
    mThread = mtaThread(mtaStopFlag)
    mThread.start()

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(),"Server Stopped - %:%s" % (hostName,hostPort))

def parseOpenSky(osResult):
    payload = ""

    try:
        for i in osResult['states']:
        
            elevation = str(i[7])

            if ((elevation == "None") or (len(elevation) == 0)):
                elevation = str(i[13])

            if (elevation != "None"):
                payload += '{"id":"' + i[0] + "-" + i[1].rstrip() + '","Type":"Aircraft","Latitude":' + str(i[6]) + ',"Longitude":' + str(i[5]) + ',"Time":"' + str(i[4]) + '","Elevation":' + elevation + ',"TrueTrack":' + str(i[10])+ "},"
    except:
        print(osResult)
    return payload[:-1]

def parseSat(satResult):
    parsed = ''

    for s in satResult:
        parsed += "{\"id\":\"" + s['satname'] + "\",\"Type\":\"Sat\",\"Latitude\":" + str(s['satlat']) +",\"Longitude\":" + str(s['satlng']) + ",\"Elevation\":" + str(s['satalt']) +"},"

    return parsed[:-1]

def parseMTA(trainLst,stations):
    print("PARSING MTA")
    stopsJSON = '{"id":"Public Transit","Type":"Train","Latitude":"0","Longitude":"0","Time":"0","Elevation":"0","UTME":"0","UTMN":"0","UTMZ":"0","TrueTrack":"0","stops":['#"{\"stops\":["
    for s in stations:
        tmpJSON = "{\"stationId\":\"" + s[0] + "\",\"stationName\":\"" + s[1] + "\",\"Latitude\":\""+ s[2] + "\",\"Longitude\":\""+ s[3] +"\",\"updates\":["
        for t in trainLst:
            tAttr = str(t).split(",")
      
            if (s[0] in tAttr[2]):
                tmpInfo = tAttr[2].split("\n")
                arriveDepart = "{\"arrive\":\"" + tmpInfo[1][7:] + "\", \"depart\":\"" + tmpInfo[4][7:] + "\"}"
                tmpJSON += "{\"train\":\"" + tAttr[0].lstrip("[").replace("\'","") + "\",\"line\":\"" + tAttr[1].replace("'","") + "\",\"arriveDepart\":" + arriveDepart +"},"
            
        tmpJSON = tmpJSON.rstrip(",")
        tmpJSON += "]},"
    
        if ('[]' not in tmpJSON):
            stopsJSON += tmpJSON
    stopsJSON = stopsJSON[:-1] 
    stopsJSON += "]}"

    # print(stopsJSON)
    return stopsJSON


def payloadBuilder(optionDict,demoLoopData,demoDataLength,tick,currentOpenSkyRecord,currentSatelliteRecord,currentMTARecord):
    #"http://localhost:9999/data?demoLoop=1&commercialFlights=1&lngMin=-76.623080&lngMax=-73.828576&latMin=38.938079&latMax=40.632118"
    payload = '{"tick":' + str(tick) + ',"targets":['

    if ('demoLoop' in optionDict):
        print("Evaluating demoLoop option...")
        if (optionDict['demoLoop'] == '1'):
            demoIndex = tick % demoDataLength
            payload += '{"id":"demoLoop","Type":"Demo",'
            payload += demoData[demoIndex].rstrip(",")[1:]

            #adding a second target
            demoIndex2 = (tick+30) % demoDataLength
            payload += ',{"id":"demoLoop2","Type":"Demo",'
            payload += demoData[demoIndex2].rstrip(",")[1:]
    else:
        print("No demoLoop option found.")

    if ('commercialFlights' in optionDict):
        print("Evaluating commercialFlights option")
        if (optionDict['commercialFlights'] == '1'):
            if (currentOpenSkyRecord != ""):
                payload += "," + currentOpenSkyRecord
    else:
        print("No commercialFlights option found")

    if ('satellite' in optionDict):
        print("Evaluating satellite option")
        if (optionDict['satellite'] == '1'):
            if (currentSatelliteRecord != ""):
                payload += "," + currentSatelliteRecord
    else:
        print("No satellite option found")

    if ('publicTransit' in optionDict):
        print("Evaluating publicTransit option")
        if (optionDict['publicTransit'] == '1'):
            # if inCity()
            if (currentMTARecord != ""):
                payload += "," + currentMTARecord
    else:
        print("No publicTransit option found")

    
    payload += ']}'

    return payload

def openSkyFetchThread():
    global currentOpenSkyRecord
    print("OSFT")
    print(lomin,lomax,lamin,lamax)
    if (lomin+lomax+lamin+lamax != "0000"):
        osResult = getOpenSkyInfo(lomin,lomax,lamin,lamax)
        currentOpenSkyRecord = parseOpenSky(osResult)
        print("############################################### NEW FLIGHT UPDATE ###############################################")

def satelliteFetchThread():
    global currentSatelliteRecord
    print("satFT")
    print(centerLat,centerLng,satRadius)
    if (centerLat+centerLng+satRadius != "000"):
        satResult = getSatInfo(centerLat,centerLng,satRadius)
        currentSatelliteRecord = parseSat(satResult)
        print("############################################# NEW SATELLITE UPDATE ###############################################")

def mtaFetchThread():
    global currentMTARecord
    global stations
    print("mtaFT")
    print(lomin,lomax,lamin,lamax)
    if (lomin+lomax+lamin+lamax != "0000"):
        # print("getting train list")
        trainLst = getMTAInfo()
        # print("parsing trainlist")
        currentMTARecord = parseMTA(trainLst,stations)
        # print(currentMTARecord)
        print("############################################# NEW MTA UPDATE ###############################################")
    print("yup")

def isBetween(check,mn,mx,):
    if (((check > mn) and (check < mx)) or ((check > mn) and (check < mx))):
        return True
    else:
        return False

def inCity(mapGrid,cityGrids):
    for c in cityGrids:
        latChk = False
        lngChk = False
        for line in range(2):
            if (isBetween(mapGrid[line],c[1],c[2])):
                latChk = True
            print("lat:" + str(latChk))
        for line in range(2,4):
            if (isBetween(mapGrid[line],c[3],c[4])):
                lngChk = True
            print("lng:" + str(lngChk))
        
        if (latChk and lngChk):
            return c[0]

    return False

##########################################################################################
# SERVER SETUP
##########################################################################################

# Pull in ip address and port from user command line
hostName = sys.argv[1] #"localhost"
hostPort = int(sys.argv[2]) #8000

# Define handler
handler = http.server.BaseHTTPRequestHandler

# Pull in demo loop data
demoData,demoDataLength = readDemoLoopDataFromFile()

# Pull in the read me

# Create class and specify how to handle GET requests
class Serv(handler):
    def _set_headers(self):
        self.send_header('Content-type','text/html')
        self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        # gets information about the request from the path used
        global currentOpenSkyRecord
        global currentSatelliteRecord
        global currentMTARecord
        global lomin
        global lomax
        global lamin
        global lamax
        global centerLat
        global centerLng
        global satRadius

        urlPath = str(self.path)[1:]
        pathArr = []
                
        # ignore the favicon request from browsers
        if (urlPath == "favicon.ico"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

        elif ('readme' in urlPath):
            readMe = readInReadMe()

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(readMe,'utf-8'))
            print("response sent:  read me")

        elif (urlPath[:4]!='data'):
            nope = readInNope()

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(nope,'utf-8'))
            print("response sent: missing 'data'")

        else:
            try:

                print(self.headers)
                
                optionDict = self.headers
                print("length of dict: " + str(len(optionDict)))

                numOpt = len(optionDict)
                print("option dictionary created with " + str(numOpt) + " options.")

                if ('commercialFlights' in optionDict):
                    print("Updating lats and longs")
                    print(lomin,lomax,lamin,lamax)
                    lomin = optionDict['lngMin']
                    lomax = optionDict['lngMax']
                    lamin = optionDict['latMin']
                    lamax = optionDict['latMax']
                    print(lomin,lomax,lamin,lamax)
                
                if ('satellite' in optionDict):
                    print("Updating lat/long center point and radius for satellites")
                    centerLat = optionDict['centerLat']
                    centerLng = optionDict['centerLng']
                    satRadius = optionDict['satRadius']
                    print(centerLat,centerLng,satRadius)

                if('publicTransit' in optionDict):
                    print("public transit in options")

                payload = payloadBuilder(optionDict,demoLoopData,demoDataLength,tick,currentOpenSkyRecord,currentSatelliteRecord,currentMTARecord)

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(bytes(payload,'utf-8'))
                print("response sent:  some damn message")
            
            except:
                nope = readInNope()

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(bytes(nope,'utf-8'))
                print("response sent: error")

# Create a server instance
myServer = http.server.HTTPServer((hostName, hostPort), Serv)

lines = readStations()
stations = parseStations(lines)

# Run the server
run()
