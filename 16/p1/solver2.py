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

def updatePathDict(cId, cPos, vIdx, cost, lastJunc, rotated, new=False, nId=-1, nPath=[]):
    if rotated:
        cost+=1000
    if not new:
        if len(nPath) == 0:
            goodPaths[cId]['path'].append(cPos)
        else:
            goodPaths[cId]['path'] = nPath[:] + [cPos]
        goodPaths[cId]['dir'] = vIdx
        goodPaths[cId]['cost'] += cost
        goodPaths[cId]['lastJunc'] = lastJunc
    else:
        goodPaths[nId] = {}
        goodPaths[nId]['path']= goodPaths[cId]['path'][:] + [cPos] if len(nPath) == 0 else nPath[:] + [cPos]
        goodPaths[nId]['dir'] = vIdx
        goodPaths[nId]['cost'] = cost
        goodPaths[nId]['lastJunc'] = lastJunc

def isDeadEnd(cId):
    if goodPaths[cId]['path'].count(goodPaths[cId]['path'][-1]) >= 2: # Loop
        return True
    elif goodPaths[cId]['lastJunc'] == (-1,-1): # in a wall
        return True
    else: 
        return False
    
    

# Get:
#   wall coord
#   Empty space coord
#   End Coor
#   Start Coor
with open("../tinput9",'r') as ofile:
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
        maze.append(line.strip(" "))
        lIdx+=1

for e in empty:
    tmpJ = []
    for v in dirV:
        if (e[0]+v[0],e[1]+v[1]) not in walls and 0 <= e[0]+v[0] < len(maze) and 0 <= e[1]+v[1] < len(maze[0]):
            tmpJ.append((e[0]+v[0],e[1]+v[1]))
    if len(tmpJ) > 2 or e == start: # Get all junctions
        junctions[e] = {}
        for p in tmpJ:
            junctions[e][p] = {'nextJ':(-1,-1), 'cost':0}
        #junctions[e] = tmpJ
        empty.remove(e)
    elif len(tmpJ) == 2 and ((tmpJ[0][0]-e[0],tmpJ[0][1]-e[1]) != (-(tmpJ[1][0]-e[0]),-(tmpJ[1][1]-e[1]))): # Get all Corners
        corner[e] = tmpJ

cPos = start
cDirIdx = startDirIdx 
pId = 0
altPath = []
cPath = [cPos]

print("corner: ",corner)
print("\nJunctions: ", junctions)
# Junction
#   jCoor : {
#       (path1,path1): {'nextJ':(nj,nj), cost:''}
#       (path2,path2): {'nextJ':(nj,nj), cost:''}
#       (path3,path3): {'nextJ':(nj,nj), cost:''}
#   }
print("\n")
for jc, nc in junctions.items():
    wPath = []
    print(f"- - Junction {jc} - Mult path : {nc}\n")
    for cc, cd in nc.items():
        tmpC = cc
        tmpPath = [cc]
        tmpDir = getDir(jc,cc)
        tmpCost = 0
        print(f"\n- Path {cc} - Data: {cd}")
        print(f"path currently taking {tmpPath}")

        while tmpPath[-1] not in list(junctions.keys()) and (tmpPath[-1] != end or tmpPath[-1] != start):
            print(f"TMP COOR : {tmpC} - START : {start}")
            if tmpC == start:
                tmpCost += 1
                tmpPath.append(tmpC)
                break
            elif tmpC in corner:
                tnPos = corner[tmpC][1] if tmpPath[-1] == corner[tmpC][0] else corner[tmpC][0]
                tmpCost += 1001
                tmpDir = getDir(tmpC,tnPos)
                tmpPath.append(tnPos)
            elif tmpC == end:
                tmpCost += 1
                break
            elif tmpC in walls:
                # dead end, we remove the path
                tmpPath = []
                break
            else:
                tmpPath.append(tmpC)
                tmpCost += 1
            tmpC = getNewPos(tmpC, tmpDir)
        
        if len(tmpPath) != 0:
            cd['nextJ'] = tmpPath[-1]
            cd['cost'] = tmpCost
            print(f"After run : {cd}")
    print("\n\n")
print(f"All Junction : {junctions}\n")
print(f"All Junction key: {list(junctions.keys())}\n")

# Delete all path that lead to (-1,-1) Or dont idc


# Setup Starting PATH | Path only contain START - Junctions - End
for p, pd in junctions[start].items():
    print(f"{p} -- {pd}")
    rotated = False if getDir(start, p) == startDirIdx else True
    updatePathDict(pId, pd['nextJ'], getDir(start, p), pd['cost'], pd['nextJ'], rotated, new=True, nId=pId, nPath=cPath)
    altPath.append(pId)
    pId+=1

print("goodPath: ", goodPaths)
print(f"altPath: {altPath}\n\n")

# Don't stop until Queue is empty (all path taken)
while len(altPath) != 0:
    # Get id Data
    cId = altPath[0]
    cDirIdx = goodPaths[cId]['dir']
    cPos = goodPaths[cId]['path'][-1]
    print(f"\nCurrent Path ID : {cId} | \
Current Path Direction '{allDir[cDirIdx]}' | \
Current Position '{cPos}' | \
Cost '{goodPaths[cId]['cost']}' | \
Queue {altPath}")
    
    firstPathTaken = False
    for p, pd in junctions[cPos].items(): # for each branch in junction
        print(f"P : {p} -- PData : {pd}")
        rotated = False if getDir(cPos, p) == cDirIdx else True
        if not firstPathTaken: # If it's the first time we move, update current branch
            firstPathTaken = True
            updatePathDict(cId, pd['nextJ'], getDir(cPos, p), pd['cost'], pd['nextJ'], rotated, new=False)
            if isDeadEnd(cId): # if after update, it's a dead end, remove it and go to the next ID
                print(f"{cId} is dead end")
                print(goodPaths[cId])
                del goodPaths[cId]
                altPath.pop(0)
            elif goodPaths[cId]['path'][-1] == end: # If after update, we got to the end, go it the next ID
                print(f"{cId} got to the end - path {goodPaths[cId]}")
                altPath.pop(0)
        else: # not the first time, then create new branch
            updatePathDict(cId, pd['nextJ'], getDir(cPos, p), pd['cost'], pd['nextJ'], rotated, new=True, nId=pId, nPath=cPath)
            if not isDeadEnd(pId): # if after update, it's NOT a dead end, we add it to the altPath and increase Pid
                print(f"Creating new alt path n°{pId} - goodPaths {goodPaths[pId]}")
                altPath.append(pId)
                pId+=1
            else:
                print(f"Not creating new path")
    time.sleep(2)




# get the lower score
scores = {}
for gpId, gpVal in goodPaths.items():
    if gpVal['cost'] not in list(scores.keys()):
        scores[gpVal['cost']] = 1
    else:
        scores[gpVal['cost']] += 1

print(f"\n\ngoodPaths: {goodPaths}\n")

winnerScore = min(list(scores.keys()))

print(f"\nAnswer : {total} - Program took : {getTime(start_time)} to run.")

# 153613 Too High
# 153606 too High

