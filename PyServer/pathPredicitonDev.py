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


def pathPredict(locHist,numPnts):
    lats = []
    longs = []
    elles = []

    locPred = []
    
    for loc in locHist:
        lats.append(loc["Latitude"])
        longs.append(loc["Longitude"])
        elles.append(loc["Elevation"])

    latDiffs = [abs(e[1] - e[0]) for e in itertools.permutations(lats, 2)]
    # avgLatDiff = sum(latDiffs)/len(latDiffs)
    avgLatDiff = np.std(latDiffs)

    lngDiffs = [abs(e[1] - e[0]) for e in itertools.permutations(longs, 2)]
    # avgLngDiff = sum(lngDiffs)/len(lngDiffs)
    avgLngDiff = np.std(lngDiffs)

    elDiffs = [abs(e[1] - e[0]) for e in itertools.permutations(elles, 2)]
    # avgElDiff = sum(elDiffs)/len(elDiffs)
    avgElDiff = np.std(elDiffs)

    latDiffSign =  1 if ((lats[1] - lats[0]) > 0) else 0
    lngDiffSign = 1 if ((longs[1] - longs[0]) > 0) else 0
    elDiffSign = 1 if ((elles[1] - elles[0]) > 0) else 0

    print("Averages")

    print(avgLatDiff)
    print(avgLngDiff)
    print(avgElDiff)

    print(latDiffSign)
    print(lngDiffSign)
    print(elDiffSign)


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

for f in history:
    print(str(f['Latitude']) + ',' + str(f['Longitude']) + "," + str(f['Latitude']) + ":" + str(f['Longitude']))

for f in future:
    print(str(f['Latitude']) + ',' + str(f['Longitude']) + "," + str(f['Latitude']) + ":" + str(f['Longitude']))