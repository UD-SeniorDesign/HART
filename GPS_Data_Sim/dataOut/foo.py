import json

with open('JSON/GPSsimV0_d2018-10-01_t18-01-53-79_newarkWalk_2.json') as json_data:
    d = json.load(json_data)
    print(d)
