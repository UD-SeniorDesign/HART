import itertools
import numpy as np

history = [{ "Latitude" :40.79161316333334 , "Longitude" :-73.95754142916667 , "Elevation" :100.0},
{ "Latitude" :40.79159832666667 , "Longitude" :-73.95755585833334 , "Elevation" :100.0},
{ "Latitude" :40.79158349000001 , "Longitude" :-73.9575702875 ,"Elevation" :100.0},
{ "Latitude" :40.79156865333334 , "Longitude" :-73.95758471666667  , "Elevation" :100.0},
{ "Latitude" :40.79155381666668 , "Longitude" :-73.95759914583334 , "Elevation" :100.0},
{ "Latitude" :40.79153898000001 , "Longitude" :-73.95761357500001 , "Elevation" :100.0},
{ "Latitude" :40.79152414333335 , "Longitude" :-73.95762800416668 , "Elevation" :100.0},
{ "Latitude" :40.79150930666668 , "Longitude" :-73.95764243333335 , "Elevation" :100.0},
{ "Latitude" :40.79149447000002 , "Longitude" :-73.95765686250002 , "Elevation" :100.0},
{ "Latitude" :40.79147963333335 , "Longitude" :-73.95767129166668 , "Elevation" :100.0}]

history2 =[
{ "Latitude" :40.79136093999805 , "Longitude" :-73.9577867249977 , "Elevation" :100.0},
{ "Latitude" :40.79139061333138 , "Longitude" :-73.95775786666437 , "Elevation" :100.0},
{ "Latitude" :40.79142028666471 , "Longitude" :-73.95772900833103 , "Elevation" :100.0},
{ "Latitude" :40.79144995999804 , "Longitude" :-73.95770014999769 , "Elevation" :100.0},
{ "Latitude" :40.79147963333137 , "Longitude" :-73.95767129166435 , "Elevation" :100.0},
{ "Latitude" :40.7915093066647 , "Longitude" :-73.95764243333102 , "Elevation" :100.0},
{ "Latitude" :40.79153897999803 , "Longitude" :-73.95761357499768 , "Elevation" :100.0},
{ "Latitude" :40.79156865333136 , "Longitude" :-73.95758471666434 , "Elevation" :100.0},
{ "Latitude" :40.79159832666469 , "Longitude" :-73.957555858331 ,  "Elevation" :100.0},
{ "Latitude" :40.79162799999802 , "Longitude" :-73.95752699999767 , "Elevation" :100.0}]

def getAvgDistance(arr):
    difSum = 0
    
    for i in range(len(arr) - 1):
        difSum += abs(arr[i]-arr[i+1])
    
    avgDif = difSum / len(arr)

    return avgDif

def getPoint(xCo,yCo,zCo,t,d):
    predX = 0
    predY = 0 
    predZ = 0

    # for i in range(d,0,-1):
    for i in range(1,d+1):
        predX += xCo[i]*t**(d-i)
        predY += yCo[i]*t**(d-i)
        predZ += zCo[i]*t**(d-i)
        # print("i: " +str(i))
        # print("d-1: " +str(d-i))
        # print("xCoef: " + str(xCo[i]))
        # print("yCoef: " + str(yCo[i]))
        # print("zCoef: " + str(zCo[i]))
        # print(predX,predY,predZ)
    return predX,predY,predZ

def pathPredict(locHist,numPnts):
    lats = []
    longs = []
    elles = []

    locPred = []
    
    for loc in locHist:
        lats.append(loc["Latitude"])
        longs.append(loc["Longitude"])
        elles.append(loc["Elevation"])

    avgLatDiff = getAvgDistance(lats)
    avgLngDiff = getAvgDistance(longs)
    avgElDiff = getAvgDistance(elles)


    latDiffSign =  1 if ((lats[1] - lats[0]) > 0) else 0
    lngDiffSign = 1 if ((longs[1] - longs[0]) > 0) else 0
    elDiffSign = 1 if ((elles[1] - elles[0]) > 0) else 0

    # print("Averages")

    # print(avgLatDiff)
    # print(avgLngDiff)
    # print(avgElDiff)

    # print(latDiffSign)
    # print(lngDiffSign)
    # print(elDiffSign)

    curPosition = locHist[len(locHist)-1]

    for i in range(numPnts):
        
        tmpLat = curPosition["Latitude"] + avgLatDiff if latDiffSign > 0 else curPosition["Latitude"] - avgLatDiff
        tmpLng = curPosition["Longitude"] + avgLngDiff if lngDiffSign > 0 else curPosition["Longitude"] - avgLngDiff
        tmpEl = curPosition["Elevation"] + avgElDiff if elDiffSign > 0 else curPosition["Elevation"] - avgElDiff
        
        tmpLocPnt = '{"Latitude":' + str(tmpLat) +',"Longitude":' + str(tmpLng) + '"Elevation":' + str(tmpEl) + '}'
        
        curPosition = dict()

        curPosition['Latitude'] = tmpLat
        curPosition['Longitude'] = tmpLng
        curPosition['Elevation'] = tmpEl

        locPred.append(curPosition)
    
    return locPred

future = pathPredict(history,10)

# for f in history:
#     print(str(f['Latitude']) + ',' + str(f['Longitude'])) # + "," + str(f['Latitude']) + ":" + str(f['Longitude'])

# for f in future:
#     print(str(f['Latitude']) + ',' + str(f['Longitude'])) # + "," + str(f['Latitude']) + ":" + str(f['Longitude'])


def pathPredictPoly(locHist, numPnts):
    lats = []
    longs = []
    elles = []
    ticks = np.arange(len(locHist))

    locPred = []
    
    for loc in locHist:
        lats.append(loc["Latitude"])
        longs.append(loc["Longitude"])
        elles.append(loc["Elevation"])    

    fitx = np.polyfit(ticks,lats,3)
    fity = np.polyfit(ticks,longs,3)
    fitz = np.polyfit(ticks,elles,3)

    # print(ticks)
    # print(fitx)
    # print(fity)
    # print(fitz)
    return fitx,fity,fitz

# for f in history:
#     print(str(f['Latitude']) + ',' + str(f['Longitude'])) # + "," + str(f['Latitude']) + ":" + str(f['Longitude'])


# fX,fY,fZ = pathPredictPoly(history,10)

# for i in range(10,20):
#     ecks,whi,zee = getPoint(fX,fY,fZ,i,3)
#     print(ecks,end=", ")
#     print(whi)

# print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")

# for f in history2:
#     print(str(f['Latitude']) + ',' + str(f['Longitude'])) # + "," + str(f['Latitude']) + ":" + str(f['Longitude'])

# fX,fY,fZ = pathPredictPoly(history2,10)

# for i in range(10,20):
#     ecks,whi,zee = getPoint(fX,fY,fZ,i,3)
#     print(ecks,end=", ")
#     print(whi)


################################################################################################
###### For testing against commercial flight data
################################################################################################

fin = open("openSkyRecords.txt",'r')
osr = fin.readlines()
fin.close()

osArr = []

for i in osr:
    # print(i)
    OSRsplit = i.split('},{')
    adjustedOSR = []

    for o in OSRsplit:
        tmpLine = ''
        if o[0] != "{":
            tmpLine += "{"
        tmpLine += o
        if o[-1] != "}":
            tmpLine += "}"
        adjustedOSR.append(tmpLine)
    # print(adjustedOSR)
    osArr.append(adjustedOSR)

osHistory = []

for a in osArr:
    hArr = []
    for i in a:
        tmpArr = []
        x = i.split(",")
        tmpArr.append(x[1].split(":")[1])
        tmpArr.append(x[2].split(":")[1])
        tmpArr.append(x[4].split(":")[1].replace("}","").replace("\n",""))
        hArr.append(tmpArr)
    # print(hArr[0])
    osHistory.append(hArr)

testFlight =  []

for o in osHistory:
    dictArr = []
    for i in o:
        if i[2] != 'None':
            lat = i[0]
            lon = i[1]
            ell = i[2]
            tmpDict = dict()
            tmpDict['Latitude'] = float(lat)
            tmpDict['Longitude'] = float(lon)
            tmpDict['Elevation'] = float(ell)
            dictArr.append(tmpDict)
    testFlight.append(dictArr)


planeOneHist = []

for i in testFlight:
    planeOneHist.append(i[0])


fX,fY,fZ = pathPredictPoly(planeOneHist[:10],10)

for i in range(10):
    ecks,whi,zee = getPoint(fX,fY,fZ,i,3)
    print(ecks,end=", ")
    print(whi,end=", ")
    print(zee)

for i in range(10,20):
    print(planeOneHist[i])

print("########################################")

for i in range(10):
    print(planeOneHist[i])