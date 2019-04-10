#J63CHM-KJQD9M-D3BECE-3YXH
#("https://www.n2yo.com/rest/v1/satellite/above/41.702/-76.014/0/70/0/&apiKey=J63CHM-KJQD9M-D3BECE-3YXH")
#seniordesignudel
#password

import requests

def fetchSats():
    r = requests.get("https://www.n2yo.com/rest/v1/satellite/above/41.702/-76.014/0/70/0/&apiKey=J63CHM-KJQD9M-D3BECE-3YXH")
    return r.json()



sats = fetchSats()['above']


def parseSat(satResult):

    parsed = ''

    for s in satResult:
        parsed += "{\"id\":\"" + s['satname'] + "\",\"Type\":\"Sat\",\"Latitude\":" + str(s['satlat']) +",\"Longitude\":" + str(s['satlng']) + ",\"Elevation\":" + str(s['satalt']) +"},"

    return parsed[:-1]
    # {"id":"a3b87f-DAL2757","Latitude":39.9109,"Longitude":-74.4478,"Time":"1554825949","Elevation":6301.74,"TrueTrack":220.25}



print(parseSat(sats))