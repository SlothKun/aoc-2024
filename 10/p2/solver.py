import copy
sPosList = []
defaultTrail = {'0': {'next':'1','coord': []},
        '1': {'next':'2','coord': []},
        '2': {'next':'3','coord': []},
        '3': {'next':'4','coord': []},
        '4': {'next':'5','coord': []},
        '5': {'next':'6','coord': []},
        '6': {'next':'7','coord': []},
        '7': {'next':'8','coord': []},
        '8': {'next':'9','coord': []},
        '9': {'next':'','coord': []}
         }
trailMap = []
bigTotal = 0
nineHit={}

with open("../tinput5",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        line = line.strip("\n")
        sPosList += [(lIdx,pos) for pos, char in enumerate(line) if char == '0']
        lIdx+=1
        trailMap.append(line)
    print(sPosList)


def hike(coord, currentNb, total):
    if currentNb == 9:
        nineHit[coord] = 1 if coord not in nineHit.keys() else nineHit[coord]+1
        return total+1

    # verify top
    if coord[0] != 0:
        if trailMap[coord[0]-1][coord[1]] == str(currentNb+1):
            total = hike((coord[0]-1,coord[1]), currentNb+1, total)
    # bottom
    if coord[0] != len(trailMap)-1:
        if trailMap[coord[0]+1][coord[1]] == str(currentNb+1):
            total = hike((coord[0]+1,coord[1]), currentNb+1, total)
    # left
    if coord[1] != 0:
        if trailMap[coord[0]][coord[1]-1] == str(currentNb+1):
            total = hike((coord[0],coord[1]-1), currentNb+1, total)
    # right
    if coord[1] != len(trailMap[0])-1:
        if trailMap[coord[0]][coord[1]+1] == str(currentNb+1):
            total = hike((coord[0],coord[1]+1), currentNb+1, total)
    return total

for zCoord in sPosList:
    print("zcoord: ", zCoord)
    tmpTotal = hike(zCoord, 0, 0)
    print("tmp : ", tmpTotal)
    bigTotal += tmpTotal
print(bigTotal)
print(nineHit)
