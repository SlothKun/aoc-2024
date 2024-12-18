#!/usr/bin/env python3
import time

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
startDirIdx = 1
walls = []
end = (-1,-1)
start = (-1,-1)
junctions = {}
corner = {}
empty = []
lines = []
goodPaths = {}


def getDir(cc, nc):
    return dirV.index((nc[0]-cc[0], nc[1]-cc[1]))

def getNewPos(cp, vIdx):
    return (cp[0]+dirV[vIdx][0], cp[1]+dirV[vIdx][1])

def updatePathDict(cId, cPos, vIdx, rotation, lastInter=(-1,-1), new=False, nId=-1):
    if cPos in goodPaths[cId]['path']:
        print(f"     DUPLICATE coor {cPos}")
    if not new: 
        goodPaths[cId]['path'].append(cPos)
        goodPaths[cId]['dir'] = vIdx
        goodPaths[cId]['cost'] += 1001 if rotation else 1
        goodPaths[cId]['lastInter'] = goodPaths[cId]['lastInter']
    else:
        goodPaths[nId] = {'cost': 0, 'dir': -1,'path':[]}
        goodPaths[nId]['path']= goodPaths[cId]['path'][:] + [cPos]
        goodPaths[nId]['dir'] = vIdx
        goodPaths[nId]['cost'] += 1001+goodPaths[cId]['cost']
        goodPaths[nId]['lastInter'] = lastInter

# Get:
#   wall coord
#   Empty space coord
#   End Coor
#   Start Coor
with open("../tinput6",'r') as ofile:
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
                start = (lIdx, cIdx)
                empty.append((lIdx, cIdx))
            else:
                empty.append((lIdx, cIdx))
            cIdx+=1
        maze.append(line)
        lIdx+=1

for e in empty:
    tmpJ = []
    for v in dirV:
        if (e[0]+v[0],e[1]+v[1]) not in walls:
            tmpJ.append((e[0]+v[0],e[1]+v[1]))
    if len(tmpJ) > 2: # Get all junctions 
        junctions[e] = tmpJ
        empty.remove(e)
    elif len(tmpJ) == 2 and ((tmpJ[0][0]-e[0],tmpJ[0][1]-e[1]) != (-(tmpJ[1][0]-e[0]),-(tmpJ[1][1]-e[1]))): # Get all Corners
        corner[e] = tmpJ

cPos = start
cDirIdx = startDirIdx 
pId = 0
altPath = [pId]
cPath = [cPos]

goodPaths[pId] = {'cost': 0, 'dir':cDirIdx, 'path':cPath[:], 'lastInter': (-1,-1)}
pId+=1

# Get starting Paths - OK
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
#print(f"Alt paths at init : {altPath}\n")


# Don't stop until Queue is empty (all path taken)
while len(altPath) != 0:
    cId = altPath[0]
    cDirIdx = goodPaths[cId]['dir']
    cPos = goodPaths[cId]['path'][-1]
    print(f"\nCurrent Path ID : {cId} | \
Current Path Direction '{allDir[cDirIdx]}' | \
Current Position '{cPos}' | \
Cost '{goodPaths[cId]['cost']}'")

    if goodPaths[cId]['path'].count(cPos) >= 2 or cPos in walls: # Loop or Deadend
        print(f"    Path {cId} - Loop or deadEnd detected at '{cPos}'")
        if cPos in walls:
            goodPaths[cId]['cost'] -= 1

        if goodPaths[cId]['lastInter'] != (-1,-1):
            lastInterIdx = goodPaths[cId]['path'].index(goodPaths[cId]['lastInter'])
            if goodPaths[cId]['path'][lastInterIdx+1] in junctions[goodPaths[cId]['lastInter']]:
                junctions[goodPaths[cId]['lastInter']].remove(goodPaths[cId]['path'][lastInterIdx+1])
        del goodPaths[cId]
        altPath.pop(0)


    elif cPos in corner.keys(): # Corner detected
        nPos = corner[cPos][0] if corner[cPos][0] not in goodPaths[cId]['path'] else corner[cPos][1]
        updatePathDict(cId, nPos, getDir(cPos, nPos), True)
        print(f"    Path {cId} - corner detected at '{cPos}' - Going to '{nPos}' - new Dir '{allDir[goodPaths[cId]['dir']]}'")
    
    
    elif cPos in junctions.keys(): # Junction detected
        tmpJ = junctions[cPos][:]
        if goodPaths[cId]['path'][-2] in tmpJ:
            tmpJ.remove(goodPaths[cId]['path'][-2])
        rotOnce = False
        if len(tmpJ) == 0:
            print(f"    Path {cId} - Junction at '{cPos}' is dead End")
            del goodPaths[cId]
            altPath.pop(0)
        oldBeforeNew = 0
        for j in tmpJ:
            rotated = True if getDir(cPos, j) != cDirIdx else False
            if rotated and not rotOnce and len(tmpJ) != 1:
                rotOnce = True
                updatePathDict(cId, j, getDir(cPos, j), rotated, lastInter=cPos, new=True, nId=pId)
                for x in range(oldBeforeNew):
                    goodPaths[pId]['path'].pop(-2)
                    goodPaths[pId]['cost'] -= 1
                print(f"{cId} - {pId}")
                altPath.append(pId)
                pId+=1
            else:
                updatePathDict(cId, j, getDir(cPos, j), rotated, lastInter=cPos)
                oldBeforeNew+=1
        print(f"    Path {cId} - Junction detected at '{cPos}' - New Path '{pId-1}' added")
    
    
    elif cPos == end: # Got to the End
        print(f"    Path {cId} - End detected at '{cPos}' - Cost {goodPaths[cId]['cost']}")
        altPath.pop(0)



    else: # Move ahead
        updatePathDict(cId, getNewPos(cPos, cDirIdx), cDirIdx, False)


for gpId, gpVal in goodPaths.items():
    if total == 0 or gpVal['cost'] < total:
        winId = gpId
        winner = gpVal
        total = gpVal['cost']

print()
print()
print()
print()
print(goodPaths)
print()
print()
print()
print()

print(winId, winner)
print(f"\nAnswer : {total} - Program took : {getTime(start_time)} to run.")

# 153613 Too High
# 153606 too High