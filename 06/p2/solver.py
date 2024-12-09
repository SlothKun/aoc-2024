#!/usr/bin/env python3
import time
start_time = time.time()

print("\n\n\n\n\n")

validDir = ['up','right','bottom','left']
moveMap = {'up':(-1,0), 'right':(0,1), 'bottom':(1,0), 'left':(0,-1)}
dirChange = {'up':'right',
            'right':'bottom',
            'bottom':'left',
            'left':'up'}
guardPos = (0,0)
guardDirIdx = 0
guardLeft = False
visitedPos = []
visitedPosDir = []
labMap = []
allLoops = []
maxLine = 0
maxCol = 0
wallDictX = {}
wallDictY = {}

def getCloserWall(gPos, gDir, wallCoord):
    closerSubPos = gPos
    for c in wallCoord:
        tmpSubPos = (gPos[0]-c[0], gPos[1]-c[1])

def loopFinder(gdirIdx, gPos, ifPrint=False):
    print(f"---------- Entering LoopFinder {gPos, validDir[gdirIdx]} -----------------") if ifPrint else None
    anchor = gPos
    anchorDir = validDir[gdirIdx]
    tmpwallCoord = []
    path = []
    moveVector = moveMap[validDir[gdirIdx]]
    wallCoord = [(gPos[0]+moveVector[0], gPos[1]+moveVector[1])]
    print(f"--> Imaginary wall at {wallCoord[0]}") if ifPrint else None
    # Add wall to Dict
    if wallCoord[0][0] not in wallDictX.keys():
        wallDictX[wallCoord[0][0]] = [(wallCoord[0][0],wallCoord[0][1])]
    else:
        wallDictX[wallCoord[0][0]].append((wallCoord[0][0],wallCoord[0][1]))
    if wallCoord[0][1] not in wallDictY.keys():
        wallDictY[wallCoord[0][1]] = [(wallCoord[0][0],wallCoord[0][1])]
    else:
        wallDictY[wallCoord[0][1]].append((wallCoord[0][0],wallCoord[0][1]))
    # Sort Dicts
    print(wallDictX[wallCoord[0][0]]) if ifPrint else None
    print(wallDictY[wallCoord[0][1]]) if ifPrint else None
    wallDictX[wallCoord[0][0]].sort(key=lambda tup: tup[0])
    wallDictY[wallCoord[0][1]].sort(key=lambda tup: tup[0])

    while True:
        # Rotate
        gdirIdx = (gdirIdx+1)%4
        gDir = validDir[gdirIdx]
        print(f"Current {gPos} Going {gDir}") if ifPrint else None
        moveVector = moveMap[gDir]
        gposUpdated = False
        # Check if wall present
        # If so TP to wall - moveVector
        # add wall to wallCoord
        if gDir in ['up','bottom']:
            print("Vertical Move") if ifPrint else None
            if gPos[1] in wallDictY.keys():
                if gDir == 'up':
                    print("WALLDICT : ", wallDictY[gPos[1]]) if ifPrint else None

                    for i in range(-1, -len(wallDictY[gPos[1]])-1,-1):
                        wallPos=wallDictY[gPos[1]][i]
                        if wallPos[0] < gPos[0]:
                            print("Wallpos coord :", wallPos) if ifPrint else None
                            gPos = (wallPos[0]-moveVector[0],wallPos[1]-moveVector[1])
                            gposUpdated = True
                            wallCoord.append((wallPos, gDir))
                            break
                elif gDir == 'bottom':
                    print("WALLDICT : ", wallDictY[gPos[1]]) if ifPrint else None
                    for i in range(len(wallDictY[gPos[1]])):
                        wallPos=wallDictY[gPos[1]][i]
                        if wallPos[0] > gPos[0]:
                            print("Wallpos coord :", wallPos) if ifPrint else None
                            gPos = (wallPos[0]-moveVector[0],wallPos[1]-moveVector[1])
                            gposUpdated = True
                            wallCoord.append((wallPos, gDir))
                            break
        elif gDir in ['left', 'right']:
            print("Horizontal Move") if ifPrint else None
            if gPos[0] in wallDictX.keys():
                if gDir == 'left':
                    print("WALLDICT : ", wallDictX[gPos[0]]) if ifPrint else None
                    for i in range(-1, -len(wallDictX[gPos[0]])-1, -1):
                        wallPos=wallDictX[gPos[0]][i]
                        if wallPos[1] < gPos[1]:
                            print("Wallpos coord :", wallPos) if ifPrint else None
                            gPos = (wallPos[0]-moveVector[0],wallPos[1]-moveVector[1])
                            gposUpdated = True
                            wallCoord.append((wallPos, gDir))
                            break
                if gDir == "right":
                    print("WALLDICT : ", wallDictX[gPos[0]]) if ifPrint else None
                    for i in range( len(wallDictX[gPos[0]])):
                        wallPos=wallDictX[gPos[0]][i]
                        if wallPos[1] > gPos[1]:
                            print("Wallpos coord :", wallPos) if ifPrint else None
                            gPos = (wallPos[0]-moveVector[0],wallPos[1]-moveVector[1])
                            gposUpdated = True
                            wallCoord.append((wallPos, gDir))
                            break

        # If Gpos not updated, then OOB -> No loop
        if not gposUpdated:
            print("gPosNotUpdated - No loop") if ifPrint else None
            # Del wall from Dict
            print(wallCoord[0]) if ifPrint else None
            wallDictX[wallCoord[0][0]].remove(wallCoord[0])
            wallDictY[wallCoord[0][1]].remove(wallCoord[0])
            return False
        # Check for loop (if current (wallPos,gdir) is present more than 1 time)
        if wallCoord.count((wallPos, gDir)) > 1:
            print("Loop detected!") if ifPrint else None
            # Del wall from Dict
            wallDictX[wallCoord[0][0]].remove(wallCoord[0])
            wallDictY[wallCoord[0][1]].remove(wallCoord[0])
            return set(wallCoord)

with open("../tinput",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        line=line.strip("\n")
        labMap.append(line)
        cIdx = 0
        for c in line:
            if c == "^":
               guardPos = (lIdx, cIdx)
               visitedPos.append(guardPos)
            if c == "#":
                if lIdx not in wallDictX.keys():
                    wallDictX[lIdx] = [(lIdx,cIdx)]
                else:
                    wallDictX[lIdx].append((lIdx,cIdx))
                if cIdx not in wallDictY.keys():
                    wallDictY[cIdx] = [(lIdx,cIdx)]
                else:
                    wallDictY[cIdx].append((lIdx,cIdx))
            cIdx += 1
        lIdx+=1
    maxLine = len(labMap)
    maxCol = len(labMap[0])
    #print(f"line {maxLine} - col {maxCol}")
    print(wallDictX)
    print(wallDictY)

while not guardLeft:
    isLoop = loopFinder(guardDirIdx, guardPos, False)
    if guardPos == (7,6):
        isLoop = loopFinder(guardDirIdx, guardPos, True)
    #print(isLoop)
    if isLoop:
        #loopFinder(guardDirIdx, guardPos, True)
        print("--- %s seconds ---" % (time.time() - start_time))
        allLoops.append(isLoop)

    move = moveMap[validDir[guardDirIdx]]
    if labMap[guardPos[0]+move[0]][guardPos[1]+move[1]] == "#":
        guardDirIdx=(guardDirIdx+1)%4
    else:
        guardPos = (guardPos[0]+move[0],guardPos[1]+move[1])
        if guardPos not in visitedPos:
            visitedPos.append((guardPos,validDir[guardDirIdx]))

    move = moveMap[validDir[guardDirIdx]]
    if not (0 <= guardPos[0]+move[0] < len(labMap)) or not (0 <= guardPos[1]+move[1] < len(labMap[0])):
        guardLeft=True

print("Total : ", len(allLoops))
#print("all loop", allLoops)
print("--- %s seconds ---" % (time.time() - start_time))
