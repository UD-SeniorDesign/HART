def isBetween(check,mn,mx,):
    if (((check > mn) and (check < mx)) or ((check > mn) and (check < mx))):
        return True
    else:
        return False

def inCity(mapGrid,cityGrids):
    for c in cityGrids:
        latChk = False
        lngChk = False
        for line in range(2):
            if (isBetween(mapGrid[line],c[1],c[2])):
                latChk = True
            print("lat:" + str(latChk))
        for line in range(2,4):
            if (isBetween(mapGrid[line],c[3],c[4])):
                lngChk = True
            print("lng:" + str(lngChk))
        
        if (latChk and lngChk):
            return c[0]

    return False

cGrid = [['sanfran',40,41,70,72],['whur',-50,-48,-72,-70]]
mGrids = [[38,39,68,69],[38,40.5,68,69],[38,39,71,78],[36,40.5,71,78]]

for m in mGrids:
    x = inCity(m,cGrid)
    print(x)
