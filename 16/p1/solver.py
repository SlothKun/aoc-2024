#!/usr/bin/env python3
import time

# https://tschinz.github.io/days-of-algo/content/notebooks/010-maze-solver-dijkstra.html
# https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Related_problems_and_algorithms

def getTime(start_time):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"

start_time = time.time()

total = 0
allDir = ['up', 'right', 'down', 'left']
dirV = [(-1,0), (0,1), (1,0), (0,-1)]
visited = []
reinDirIdx = 1
walls = []
end = (-1,-1)
rein = (-1,-1)
maxLine = 0
maxCol = 0
junctions = {}
corner = {}
empty = []
lines = []
goodPaths = {}
deadEnds = []


def getDir(cc, nc):
    #print((nc[0]-cc[0], nc[1]-cc[1]))
    return dirV.index((nc[0]-cc[0], nc[1]-cc[1]))

def getNewPos(cp, vIdx):
    return (cp[0]+dirV[vIdx][0], cp[1]+dirV[vIdx][1])

def updatePathDict(cId, cPos, vIdx, rotation, new=False, nId=-1):
    if not new:
        goodPaths[cId]['path'].append(cPos)
        goodPaths[cId]['dir'] = vIdx
        goodPaths[cId]['cost'] += 1001 if rotation else 1
    else:
        goodPaths[nId] = {'cost': 0, 'dir': -1,'path':[]}
        goodPaths[nId]['path']= goodPaths[cId]['path'][:] + [cPos]
        goodPaths[nId]['dir'] = vIdx
        goodPaths[nId]['cost'] += 1001+goodPaths[cId]['cost']




with open("../input",'r') as ofile:
    lIdx = 0
    maze = []
    for line in ofile.readlines():
        cIdx = 0
        line = line.strip('\n')
        for c in line:
            if c == '#':
                walls.append((lIdx, cIdx))
            elif c == 'E':
                end = (lIdx, cIdx)
            elif c == 'S':
                rein = (lIdx, cIdx)
                empty.append((lIdx, cIdx))
            else:
                empty.append((lIdx, cIdx))
            cIdx+=1
        maze.append(line)
        visited.append([False for i in range(cIdx)])
        lIdx+=1
    maxLine=lIdx
    maxCol=len(line)

print()
#print(rein)
#print(end)
#print(maxLine)
#print(maxCol)

# Get junctions
for e in empty:
    tmpJ = []
    for v in dirV:
        if (e[0]+v[0],e[1]+v[1]) not in walls:
            tmpJ.append((e[0]+v[0],e[1]+v[1]))
    if len(tmpJ) > 2:
        junctions[e] = tmpJ
        empty.remove(e)
    elif len(tmpJ) == 2 and ((tmpJ[0][0]-e[0],tmpJ[0][1]-e[1]) != (-(tmpJ[1][0]-e[0]),-(tmpJ[1][1]-e[1]))):
        corner[e] = tmpJ


print(f"Walls : {walls} - {len(walls)}\n")
print(f"Junctions : {junctions} - {len(junctions)}\n")
print(f"Empty : {empty} - {len(empty)}\n")
print(f"Corner : {corner} - {len(corner)}\n")

cPos = rein
cDirIdx = reinDirIdx 
pId = 0
altPath = [pId]
cPath = [cPos]

goodPaths[pId] = {'cost': 0, 'dir':cDirIdx, 'path':cPath[:]}
pId+=1

if cPos in corner.keys():
    if corner[cPos][0] == (cPos[0]+dirV[cDirIdx][0], cPos[1]+dirV[cDirIdx][1]):
        updatePathDict(pId-1, corner[cPos][1], getDir(cPos, corner[cPos][1]), True, new=True, nId=pId)
        updatePathDict(pId-1, corner[cPos][0], cDirIdx, False)
    else:
        updatePathDict(pId-1, corner[cPos][0], getDir(cPos, corner[cPos][0]), True, new=True, nId=pId)
        updatePathDict(pId-1, corner[cPos][1], cDirIdx, False)
    altPath.append(pId)
    pId+=1
elif (cPos[0]+dirV[cDirIdx][0], cPos[1]+dirV[cDirIdx][1]) in walls:
    cDirIdx -= 1
    updatePathDict(pId-1, getNewPos(cPos, cDirIdx), cDirIdx, True)
else:
    updatePathDict(pId-1, getNewPos(cPos, cDirIdx), cDirIdx, False)

print(f"Good path at init : {goodPaths}")
print(f"Alt paths at init : {altPath}")

test = False
while len(altPath) != 0:
    cId = altPath[0]
    cDirIdx = goodPaths[cId]['dir']
    cPos = goodPaths[cId]['path'][-1]
    #print(f"Current Path ID : {cId} | \
#Current Path Direction '{allDir[cDirIdx]}' | \
#Current Position {cPos}")
    #if test: break
    if goodPaths[cId]['path'].count(cPos) >= 2 or cPos in walls: # Loop or Deadend
        #print(f"    Path {cId} - Loop or deadEnd detected at '{cPos}'")
        del goodPaths[cId]
        altPath.pop(0)
    elif cPos in corner.keys(): # Corner detected
        nPos = corner[cPos][0] if corner[cPos][0] not in goodPaths[cId]['path'] else corner[cPos][1]
        updatePathDict(cId, nPos, getDir(cPos, nPos), True)
        #print(f"    Path {cId} - corner detected at '{cPos}' - Going to '{nPos}' - new Dir '{allDir[goodPaths[cId]['dir']]}'")
    elif cPos in junctions.keys(): # Junction detected
        tmpJ = junctions[cPos][:]
        tmpJ.remove(goodPaths[cId]['path'][-2])
        rotOnce = False
        for j in tmpJ:
            rotated = True if getDir(cPos, j) != cDirIdx else False
            if rotated and not rotOnce:
                rotOnce = True
                updatePathDict(cId, j, getDir(cPos, j), rotated, new=True, nId=pId)
                altPath.append(pId)
                pId+=1
            else:
                updatePathDict(cId, j, getDir(cPos, j), rotated)
        #print(f"    Path {cId} - Junction detected at '{cPos}' - New Path '{pId-1}' added")
        test = True
    elif cPos == end: # Got to the End
        #print(f"    Path {cId} - End detected at '{cPos}'")
        altPath.pop(0)
        updatePathDict(cId, cPos, cDirIdx, False)
    else: # Move ahead
        updatePathDict(cId, getNewPos(cPos, cDirIdx), cDirIdx, False)


#print(goodPaths)
for gpId, gpVal in goodPaths.items():
    if total == 0 or gpVal['cost'] < total:
        total = gpVal['cost']

# -2 because idk
print(f"\nAnswer : {total-2} - Program took : {getTime(start_time)} to run.")
