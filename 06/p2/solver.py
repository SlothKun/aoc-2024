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

def loopFinder(gdirIdx, gPos, ifPrint=False):
    looped=False
    if ifPrint:
        print("----------- Entering loopFinder :", gPos, validDir[gdirIdx], "-----------")
    anchor = gPos
    anchorDir = validDir[gdirIdx]
    tmpwallCoord = []
    path = []
    moveVector = moveMap[validDir[gdirIdx]]
    wallCoord = [(gPos[0]+moveVector[0], gPos[1]+moveVector[1])]
    if ifPrint:
        print("---> Imaginary wall at", wallCoord[0])
    while not looped:
        #if ifPrint:
            #print(set(path))
            #print(wallCoord[0] in path)
            #print("ANCHOR!", anchor)
            #print("---> Imaginary wall at", wallCoord[0])
            #print("wallCoord", set(wallCoord))

        gdirIdx = (gdirIdx+1)%4
        gdir = validDir[gdirIdx]
        moveVector = moveMap[gdir]
        gPos = path[-1][0] if len(path) != 0 else gPos
        if ifPrint:
            print("New position at", gPos)
            print("pos :", labMap[gPos[0]][gPos[1]])
            print("Now going", gdir)
        for i in range(1,max(maxLine, maxCol)):
            visited = (gPos[0]+moveVector[0]*i, gPos[1]+moveVector[1]*i)
            #print(visited)
            if 0 <= visited[0] < maxLine and 0 <= visited[1] < maxCol:
                if labMap[visited[0]][visited[1]] == '#':
                    if ifPrint:
                        print('Hit wall at', visited)
                    wallCoord.append(visited)
                    #path.append((visited, gdir))
                    break
                else:
                    #print(visited)
                    #path.append(visited, gdir)
                    if (visited == anchor and gdir == anchorDir) or \
                        ((visited,gdir) in path):
                        looped = True
                        break
                path.append((visited, gdir))
            else:
                # out of band
                if ifPrint:
                    print("oob at :", visited)
                return False
    if ifPrint:
        print("loopFinder: ", wallCoord)
    return wallCoord


with open("../input",'r') as ofile:
    lNb = 0
    for line in ofile.readlines():
        line=line.strip("\n")
        labMap.append(line)
        if line.find('^') != -1:
            guardPos = (lNb,line.find("^"))
            visitedPos.append(guardPos)
        lNb+=1
    maxLine = len(labMap)
    maxCol = len(labMap[0])
    #print(f"line {maxLine} - col {maxCol}")


while not guardLeft:
    isLoop = loopFinder(guardDirIdx, guardPos, False)
    #print(isLoop)
    #if isLoop:
    #    loopFinder(guardDirIdx, guardPos, True)
    if isLoop:
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