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

##########################################################################################
# CONSTANTS
##########################################################################################
tick = 0
prevTickTime = dt.now()
demoLoopData = []

##########################################################################################
# FUNCTIONS
##########################################################################################

# Define run behavior
def run():
    print(time.asctime(),"Server Started - %s:%s" % (hostName,hostPort))
    print("server:",handler.server_version,"system:",handler.sys_version)

    t1 = threading.Thread(target=ticker)
    # t2 = threading.Thread(target=myServer.serve_forever)
    try:
        t1.start()
        # t2.start()
        t1.join()
        # t2.join()
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(),"Server Stopped - %:%s" % (hostName,hostPort))

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

def ticker():
    print("ticker called")
    global prevTickTime
    global tick

    tick += 1
    print("tick:" +str(tick))

    return

def readDemoLoopDataFromFile():
    fin = open("Data/fly-madison_GPSsimV0_d2018-12-03_t22-20-2.json",'r')
    demoData = fin.read()
    fin.close()
    # print(len(demoData))
    dd = demoData[1:-1].split('\n')
    # print(len(dd))
    return dd

##########################################################################################
# SERVER SETUP
##########################################################################################

# Pull in ip address and port from user command line
hostName = sys.argv[1] #"localhost"
hostPort = int(sys.argv[2]) #8000

# Define handler
handler = http.server.BaseHTTPRequestHandler

#Pull in demo loop data




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
        method = self.command
                
        # ignore the favicon request from browsers
        if (urlPath == "favicon.ico"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
        else:
            try:
                varStart = urlPath.find("?")
                opts = urlPath[varStart + 1:].split("&")
                
                print("VARIABLES START AT INDEX: " + str(varStart))
                print(opts)
                
                getOpenSkyInfo(-76.623080,-73.828576,38.938079,40.632118)
                
                ticker()

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(bytes('tick: ' + str(tick),'utf-8'))
                print("response sent:  some damn message")
            
            except:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(bytes('bad format','utf-8'))
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