import requests
import time

def getOpenSkyInfo(lomin,lomax,lamin,lamax):
    laminStr = 'lamin=' + str(lamin) + '&'
    lamaxStr = 'lamax=' + str(lamax) + '&'
    lominStr = 'lomin=' + str(lomin) + '&'
    lomaxStr = 'lomax=' + str(lomax)

    r = requests.get('https://opensky-network.org/api/states/all?' + laminStr + lamaxStr + lominStr + lomaxStr)
    # print(r.text)
    # print(r.json())
    return r.json()


os = getOpenSkyInfo(-76.623080,-73.828576,38.938079,40.632118)

def parseOpenSky(osResult):
    payload = ""

    for i in osResult['states']:
    
        elevation = str(i[7])

        if ((elevation == "None") or (len(elevation) == 0)):
            print(elevation)
            elevation = str(i[13])

        payload += '{"id":"' + i[0] + "-" + i[1].rstrip() + '","Latitude":' + str(i[6]) + ',"Longitude":' + str(i[5]) + ',"Time":"' + str(i[4]) + '","Elevation":' + elevation + "},"

    return payload[:-1]

for i in range(50):
    result = parseOpenSky(os)
    outFile = open("openSkyRecords.txt","a")
    outFile.write(result+"\n")
    outFile.close()
    time.sleep(10)
    print("record #" + str(i) + " logged.")
