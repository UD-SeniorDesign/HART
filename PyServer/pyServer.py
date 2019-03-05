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

##########################################################################################
# CONSTANTS
##########################################################################################
tick = 0
prevTickTime = dt.now()
demoLoopData = []
currentOpenSkyRecord = ""
lomin = 0
lomax = 0
lamin = 0
lamax = 0

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

class openSkyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global currentOpenSkyRecord
        while not self.stopped.wait(10):
            openSkyFetchThread()


def getOpenSkyInfo(lomin,lomax,lamin,lamax):
    laminStr = 'lamin=' + str(lamin) + '&'
    lamaxStr = 'lamax=' + str(lamax) + '&'
    lominStr = 'lomin=' + str(lomin) + '&'
    lomaxStr = 'lomax=' + str(lomax)

    r = requests.get('https://opensky-network.org/api/states/all?' + laminStr + lamaxStr + lominStr + lomaxStr)
    return r.json()


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

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(),"Server Stopped - %:%s" % (hostName,hostPort))

def parseOpenSky(osResult):
    payload = ""

    for i in osResult['states']:
    
        elevation = str(i[7])

        if ((elevation == "None") or (len(elevation) == 0)):
            elevation = str(i[13])

        if (elevation != "None"):
            payload += '{"id":"' + i[0] + "-" + i[1].rstrip() + '","Latitude":' + str(i[6]) + ',"Longitude":' + str(i[5]) + ',"Time":"' + str(i[4]) + '","Elevation":' + elevation + "},"

    return payload[:-1]


def payloadBuilder(optionDict,demoLoopData,demoDataLength,tick,currentOpenSkyRecord):
    #"http://localhost:9999/data?demoLoop=1&commercialFlights=1&lngMin=-76.623080&lngMax=-73.828576&latMin=38.938079&latMax=40.632118"
    payload = '{"tick":' + str(tick) + ',"targets":['


    if (optionDict['demoLoop'] == '1'):
        demoIndex = tick % demoDataLength
        payload += '{"id":"demoLoop",'
        payload += demoData[demoIndex].rstrip(",")[1:]

        #addinga second target
        demoIndex2 = (tick+30) % demoDataLength
        payload += ',{"id":"demoLoop2",'
        payload += demoData[demoIndex2].rstrip(",")[1:]

        
    # try:
    #     if (optionDict['commercialFlights'] == '1'):

    #         if ((tick%10) == 1):
    #             lomin = optionDict['lngMin']
    #             lomax = optionDict['lngMax']
    #             lamin = optionDict['latMin']
    #             lamax = optionDict['latMax']

    #             osResult = getOpenSkyInfo(lomin,lomax,lamin,lamax)
    #             payload += "," + parseOpenSky(osResult)
    #             currentOpenSkyRecord = payload
    #             print(osResult)

    #         else:
    #             payload += currentOpenSkyRecord
    # except:
    #     pass

    payload += "," + currentOpenSkyRecord
    payload += ']}'

    return payload

def openSkyFetchThread():
    global currentOpenSkyRecord
    print("OSFT")
    print(lomin,lomax,lamin,lamax)
    if (lomin+lomax+lamin+lamax != "0000"):
        osResult = getOpenSkyInfo(lomin,lomax,lamin,lamax)
        currentOpenSkyRecord = parseOpenSky(osResult)

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
        global lomin
        global lomax
        global lamin
        global lamax

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
            print("response sent:  bad format")

        else:
            try:
                # find where the variables start
                varStart = urlPath.find("?")

                # pull out variables from URL
                opts = urlPath[varStart + 1:].split("&")        
                print("OPTIONS RECEIVED: ",end="")
                print(opts)

                optionDict = dict()

                for o in opts:
                    tmpO = o.split("=")
                    optionDict[tmpO[0]] = tmpO[1]

                lomin = optionDict['lngMin']
                lomax = optionDict['lngMax']
                lamin = optionDict['latMin']
                lamax = optionDict['latMax']

                payload = payloadBuilder(optionDict,demoLoopData,demoDataLength,tick,currentOpenSkyRecord)

                print("still good")

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
                print("response sent:  bad format")

# Create a server instance
myServer = http.server.HTTPServer((hostName, hostPort), Serv)

# Run the server
run()