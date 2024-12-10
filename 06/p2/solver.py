#!/usr/bin/env python3
import time
start_time = time.time()

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

def getCloserWall(gPos, gDir, wallList, ifPrint=False):
    print(f"Wall list : {wallList}") if ifPrint else None
    closerWall = ((-1,-1),(-1,-1)) # WallCoor, delta
    for w in wallList:
        delta = (w[0]-gPos[0], w[1]-gPos[1])
        print(f"Delta {delta} - closer wall : {closerWall}") if ifPrint else None
        if gDir == 'up' and delta[0] < 0 and (delta[0] > closerWall[1][0] or closerWall == ((-1,-1),(-1,-1))):
            closerWall = (w, delta)
        elif gDir == 'left' and delta[1] < 0 and (delta[1] > closerWall[1][1] or closerWall == ((-1,-1),(-1,-1))):
            closerWall = (w, delta)
        elif gDir == 'bottom' and delta[0] > 0 and (delta[0] < closerWall[1][0] or closerWall == ((-1,-1),(-1,-1))):
            closerWall = (w, delta)
        elif gDir == 'right' and delta[1] > 0 and (delta[1] < closerWall[1][1] or closerWall == ((-1,-1),(-1,-1))):
            closerWall = (w, delta)
    if closerWall == ((-1,-1),(-1,-1)): # no change
        print("No close wall found") if ifPrint else None
        return False
    else:
        print(f"close wall found, its : {closerWall[0]}") if ifPrint else None
        return closerWall[0]

def loopFinder(gdirIdx, gPos, visitedPos, ifPrint=False):
    print(f"---------- Entering LoopFinder {gPos, validDir[gdirIdx]} -----------------") if ifPrint else None
    # Get imaginary wall info
    wallPos = False
    moveVector = moveMap[validDir[gdirIdx]]
    wallCoord = [((gPos[0]+moveVector[0], gPos[1]+moveVector[1]), validDir[gdirIdx])]
    print(f"--> Imaginary wall at {wallCoord[0]}") if ifPrint else None
    # check if iwall coord was already traversed
    print(f"{visitedPos[0]} - {wallCoord[0][0]} - {wallCoord[0][0] in visitedPos}") if ifPrint else None
    if wallCoord[0][0] in visitedPos:
        print(f"Cannot place imaginary wall, leaving") if ifPrint else None
        return False
    # Add wall to Dict
    if wallCoord[0][0][0] not in wallDictX.keys():
        wallDictX[wallCoord[0][0][0]] = [(wallCoord[0][0][0],wallCoord[0][0][1])]
    else:
        wallDictX[wallCoord[0][0][0]].append((wallCoord[0][0][0],wallCoord[0][0][1]))
    if wallCoord[0][0][1] not in wallDictY.keys():
        wallDictY[wallCoord[0][0][1]] = [(wallCoord[0][0][0],wallCoord[0][0][1])]
    else:
        wallDictY[wallCoord[0][0][1]].append((wallCoord[0][0][0],wallCoord[0][0][1]))

    while True:
        # Rotate
        gdirIdx = (gdirIdx+1)%4
        gDir = validDir[gdirIdx]
        print(f"Current {gPos} Going {gDir}") if ifPrint else None
        moveVector = moveMap[gDir]
        gposUpdated = False
        # Check if wall present
        # if so add closest wall to list
        if gDir == 'up':
            #print("WALLDICT : ", wallDictY[gPos[1]]) if ifPrint else None
            if gPos[1] in wallDictY.keys():
                wallPos = getCloserWall(gPos, gDir, wallDictY[gPos[1]], ifPrint)
        elif gDir == 'bottom':
            #print("WALLDICT : ", wallDictY[gPos[1]]) if ifPrint else None
            if gPos[1] in wallDictY.keys():
                wallPos = getCloserWall(gPos, gDir, wallDictY[gPos[1]], ifPrint)
        elif gDir == 'left':
            #print("WALLDICT : ", wallDictX[gPos[0]]) if ifPrint else None
            if gPos[0] in wallDictX.keys():
                wallPos = getCloserWall(gPos, gDir, wallDictX[gPos[0]], ifPrint)
        elif gDir == 'right':
            #print("WALLDICT : ", wallDictX[gPos[0]]) if ifPrint else None
            if gPos[0] in wallDictX.keys():
                wallPos = getCloserWall(gPos, gDir, wallDictX[gPos[0]], ifPrint)

        if wallPos: # If wall was found, add it
            print("Wallpos coord :", wallPos) if ifPrint else None
            gPos = (wallPos[0]-moveVector[0],wallPos[1]-moveVector[1])
            wallCoord.append((wallPos, gDir))
        else: # If Gpos not updated, then OOB -> No loop
            print("gPosNotUpdated - No loop") if ifPrint else None
            # Del wall from Dict
            print(wallCoord[0]) if ifPrint else None
            wallDictX[wallCoord[0][0][0]].remove(wallCoord[0][0])
            wallDictY[wallCoord[0][0][1]].remove(wallCoord[0][0])
            return False
        
        # Check for loop (if current (wallPos,gdir) is present more than 1 time)
        if wallCoord.count((wallPos, gDir)) > 1:
            print("Loop detected!") if ifPrint else None
            print(set(wallCoord)) if ifPrint else None
            # Del wall from Dict
            wallDictX[wallCoord[0][0][0]].remove(wallCoord[0][0])
            wallDictY[wallCoord[0][0][1]].remove(wallCoord[0][0])
            return set(wallCoord)

with open("../input",'r') as ofile:
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
    print(f"line {maxLine} - col {maxCol}")
    print(wallDictX)
    print(wallDictY)

while not guardLeft:
    isLoop = loopFinder(guardDirIdx, guardPos, visitedPos, False)

    if isLoop:
        isLoop = sorted(isLoop)
        if isLoop not in allLoops:
            #loopFinder(guardDirIdx, guardPos, visitedPos, True)
            print("--- %s seconds ---" % (time.time() - start_time))
            allLoops.append(isLoop)

    move = moveMap[validDir[guardDirIdx]]
    if labMap[guardPos[0]+move[0]][guardPos[1]+move[1]] == "#":
        guardDirIdx=(guardDirIdx+1)%4
    else:
        guardPos = (guardPos[0]+move[0],guardPos[1]+move[1])
        if guardPos not in visitedPos:
            visitedPos.append(guardPos)

    move = moveMap[validDir[guardDirIdx]]
    if not (0 <= guardPos[0]+move[0] < len(labMap)) or not (0 <= guardPos[1]+move[1] < len(labMap[0])):
        guardLeft=True

print("Total : ", len(allLoops))
print("--- %s seconds ---" % (time.time() - start_time))