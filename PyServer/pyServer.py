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
readMe = ""

##########################################################################################
# FUNCTIONS
##########################################################################################
class tickThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global tick
        while not self.stopped.wait(1):
            print(str(tick) + " | " + str(dt.now()))
            tick += 1
            # call a function

def handleLiveTargetsRequests():
    return

def handleLoopTargerRequest():
    return

def getOpenSkyInfo(lomin,lomax,lamin,lamax):
    laminStr = 'lamin=' + str(lamin) + '&'
    lamaxStr = 'lamax=' + str(lamax) + '&'
    lominStr = 'lomin=' + str(lomin) + '&'
    lomaxStr = 'lomax=' + str(lomax)

    r = requests.get('https://opensky-network.org/api/states/all?' + laminStr + lamaxStr + lominStr + lomaxStr)
    # print(r.text)
    # print(r.json())
    return

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
    print(nope)
    return nope

# Reads in the readme html
def readInReadMe():
    fin = open("readme.html")
    readme = fin.read()
    fin.close()
    print(readme)
    return readme

# Define run behavior
def run():
    print(time.asctime(),"Server Started - %s:%s" % (hostName,hostPort))
    print("server:",handler.server_version,"system:",handler.sys_version)

    stopFlag = Event()
    thread = tickThread(stopFlag)
    thread.start()
    
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(),"Server Stopped - %:%s" % (hostName,hostPort))


def payloadBuilder(optionDict,demoLoopData,demoDataLength,tick):
    payload = '{"tick":' + str(tick) + ',"targets":['

    if (optionDict['demoLoop'] == '1'):
        demoIndex = tick % demoDataLength
        payload += '{"id":"demoLoop",'
        payload += demoData[demoIndex].rstrip(",")[1:]

        #addinga second target
        payload += ',{"id":"demoLoop2",'
        payload += demoData[demoIndex+30].rstrip(",")[1:]
    
    payload += ']}'

    return payload


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
readMe = readInReadMe()
nope = readInNope()

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
        urlPath = str(self.path)[1:]
        pathArr = []
                
        # ignore the favicon request from browsers
        if (urlPath == "favicon.ico"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

        elif ('readme' in urlPath):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(readMe,'utf-8'))
            print("response sent:  read me")

        elif (urlPath[:4]!='data'):
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

                # if (optionDict['demoLoop'] == '1'):
                #     demoIndex = tick % demoDataLength
                #     payload = demoData[demoIndex]

                payload = payloadBuilder(optionDict,demoLoopData,demoDataLength,tick)

                # payload = payloadBuilder(optionDict)
                # getOpenSkyInfo(-76.623080,-73.828576,38.938079,40.632118)
                # payload = 'tick: ' + str(tick)

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(bytes(payload,'utf-8'))
                print("response sent:  some damn message")
            
            except:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(bytes(nope,'utf-8'))
                print("response sent:  bad format")

# Create a server instance
myServer = http.server.HTTPServer((hostName, hostPort), Serv)

# Run the server
run()


# 40.632118, -76.623080
# 38.938079, -73.828576

# lamin	float	lower bound for the latitude in decimal degrees
# lomin	float	lower bound for the longitude in decimal degrees
# lamax	float	upper bound for the latitude in decimal degrees
# lomax	float	upper bound for the longitude in decimal degrees

# https://opensky-network.org/api/states/all?lamin=38.938079&lamax=40.632118&lomin=-76.623080&lomax=-73.828576


# Params for requests

# airlines
# prediction
# demoLoop