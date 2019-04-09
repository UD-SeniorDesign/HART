#J63CHM-KJQD9M-D3BECE-3YXH
#("https://www.n2yo.com/rest/v1/satellite/above/41.702/-76.014/0/70/0/&apiKey=J63CHM-KJQD9M-D3BECE-3YXH")
#seniordesignudel
#password

import requests

def fetchSats():
    r = requests.get("https://www.n2yo.com/rest/v1/satellite/above/41.702/-76.014/0/70/0/&apiKey=J63CHM-KJQD9M-D3BECE-3YXH")
    return r.json()

sats = fetchSats()['above']
for s in sats:
    parsed = "{\"id\":\"" + s['satname'] + "\",\"Latitude\":" + str(s['satlat']) +",\"Longitude\":" + str(s['satlng']) + ",\"Elevation\":" + str(s['satalt']) +"}"
    print(parsed)


    # {"id":"a3b87f-DAL2757","Latitude":39.9109,"Longitude":-74.4478,"Time":"1554825949","Elevation":6301.74,"TrueTrack":220.25}