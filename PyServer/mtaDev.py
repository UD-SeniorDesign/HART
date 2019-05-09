import requests
import glob
import csv

from google.protobuf import json_format
from google.transit import gtfs_realtime_pb2

MTA_API_KEY = "d8d8bf77573b91e6462358cf6ec5a755"
MTA_FEED_IDS = ["1","26","16","21","2","11","31","36","51"]
MTA_ENDPOINT = "http://datamine.mta.info/mta_esi.php?key=" + MTA_API_KEY + "&feed_id="

# feed = gtfs_realtime_pb2.FeedMessage()

# response = requests.get(ENDPOINT+FEED_IDS[1])
# feed.ParseFromString(response.content)


def getMTAInfo():
  feed = gtfs_realtime_pb2.FeedMessage()
  response = requests.get(MTA_ENDPOINT+MTA_FEED_IDS[1])
  feed.ParseFromString(response.content)
  trainLst = []

  for entity in feed.entity:
    if entity.HasField('trip_update'):
      if ( entity.trip_update.stop_time_update):
        trainLst.append([entity.id,entity.trip_update.trip.trip_id, entity.trip_update.stop_time_update])
  
  return trainLst


# read in station info from file

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

def pprint(arr):
  for a in arr:
    print(a)

trainLst = getMTAInfo()
lines = readStations()
stations = parseStations(lines)


# print(stations[1])
# print(trainLst[0])


# def prepStations(stations, )

def parseMTA(trainLst,stations):
  stopsJSON = '{"id":"Public Transit","Type":"Train","Latitude":"0","Longitude":"0","Time":"0","Elevation":"0","UTME":"0","UTMN":"0","UTMZ":"0","TrueTrack":"0","stops":['#"{\"stops\":["
  for s in stations:
    tmpJSON = "{\"stationId\":\"" + s[0] + "\",\"stationName\":\"" + s[1] + "\",\"latitude\":\""+ s[2] + "\",\"longitude\":\""+ s[3] +"\",\"updates\":["
    for t in trainLst:
      tAttr = str(t).split(",")
      
      if (s[0] in tAttr[2]):
        # print(s[0], end=" | ")
        # print(tAttr[0],tAttr[1],tAttr[2])
        tmpInfo = tAttr[2].split("\n")
        arriveDepart = "{\"arrive\":\"" + tmpInfo[1][7:] + "\", \"depart\":\"" + tmpInfo[4][7:] + "\"}"
        # print(arriveDepart)
        tmpJSON += "{\"train\":\"" + tAttr[0].lstrip("[").replace("\'","") + "\",\"line\":\"" + tAttr[1].replace("'","") + "\",\"arriveDepart\":" + arriveDepart +"},"
        # print(tmpJSON)
        # input()
    tmpJSON = tmpJSON.rstrip(",")
    tmpJSON += "]},"
    # print("DONE")
    if ('[]' not in tmpJSON):
      stopsJSON += tmpJSON
  stopsJSON = stopsJSON[:-1] 
  stopsJSON += "]}"

  print(stopsJSON)
  return stopsJSON

parseMTA(trainLst,stations)

# 1. http://datamine.mta.info/mta_esi.php?key=<key>&feed_id=1
# This feed includes real-time data from the:
# 1 Subway2 Subway3 Subway4 Subway5 Subway6 SubwayS Subway Lines


# 2. http://datamine.mta.info/mta_esi.php?key=<key>&feed_id=26
# This feed includes real-time data from the:
# A SubwayC SubwayE SubwayH SubwayS Subway Line. ( Franklin Ave. Shuttle)


# 3. http://datamine.mta.info/mta_esi.php?key=<key>&feed_id=16
# This feed includes real-time data from the:
# N SubwayQ SubwayR SubwayW Subway Lines


# 4. http://datamine.mta.info/mta_esi.php?key=<key>&feed_id=21
# This feed includes real-time data from the:
# B SubwayD SubwayF SubwayM Subway Lines


# 5. http://datamine.mta.info/mta_esi.php?key=<key>&feed_id=2
# This feed includes real-time data from the:
# L Subway Line


# 6. http://datamine.mta.info/mta_esi.php?key=<key>&feed_id=11
# This feed includes real-time data from the:
# Staten Island Railway Staten Island Railway


# 7. http://datamine.mta.info/mta_esi.php?key=<key>&feed_id=31
# This feed includes real-time data from the:
# G Subway Line


# 8. http://datamine.mta.info/mta_esi.php?key=&feed_id=36
# This feed includes real-time data from the:
# J SubwayZ Subway Lines


# 9. http://datamine.mta.info/mta_esi.php?key=&feed_id=51
# This feed includes real-time data from the:
# 7 Subway Line
