#!/usr/bin/env python3
import copy

validDir = ['up','right','bottom','left']
moveMap = {'up':(-1,0), 'right':(0,1), 'bottom':(1,0), 'left':(0,-1)}
charMap = {'up':'^','right':'>','bottom':'v','left':'<'}
dirChange = {'up':{'next':'right', 'previous':'left'},
            'right':{'next':'bottom', 'previous':'up'},
            'bottom':{'next':'left', 'previous':'right'},
            'left':{'next':'up', 'previous':'bottom'}}
gPos = (0,0)
gDirIdx = 0
gLeft = False
labMap = []
allLoop = []


def doMovement(labMap, gPos, gDirIdx):
    rotated = False
    gLeft = False
    move = moveMap[validDir[gDirIdx]]
    if labMap[gPos[0]+move[0]][gPos[1]+move[1]] == "#":
        gDirIdx = (gDirIdx+1)%4
        rotated = True
        labMap[gPos[0]][gPos[1]] = charMap[validDir[gDirIdx]]
    else:
        gchar = labMap[gPos[0]][gPos[1]]
        labMap[gPos[0]][gPos[1]] = '.'
        gPos = (gPos[0]+move[0],gPos[1]+move[1])
        labMap[gPos[0]][gPos[1]] = gchar
        
    move = moveMap[validDir[gDirIdx]]
    if not (0 <= gPos[0]+move[0] < len(labMap)) or not (0 <= gPos[1]+move[1] < len(labMap[0])):
        gLeft=True
    return labMap,gPos,gDirIdx,rotated,gLeft


def getAdjWalls(labMap, wPos, wDir):
    # On part de Top, si on a son next vector ensuite on utilise celui de right, puis bottom, puis left
    # On fait ça pour voir le 'prochain' mur et celui d'avant
    # To get previous, just do nWallVectorIdx+1%len(nWallVector)
    # t, r, b, l
    #nWallVector = [(1,'+'),('+',-1),(-1,'-'),('-',1)] # t->r, r->b, b->l, l->t
    wdirVector = {'up':0,'right':1,'bottom':2,'left':3}
    nWallVectorIdx = wdirVector[wDir]
    isWallFound={'next':False, 'previous':False}
    print("------------------", wDir, wPos, "------------------")
    for x in range(1,len(labMap)):
        for y in range(1,len(labMap[0])):
            nWallVector = [(1,y),(x,-1),(-1,-y),(-x,1)] # t->r, r->b, b->l, l->t
            for checkDir in isWallFound.keys():
                if not isWallFound[checkDir]:
                    vector = nWallVector[nWallVectorIdx] if checkDir == 'next' else nWallVector[(nWallVectorIdx+1)%len(nWallVector)]
                    nextWPos = (wPos[0]+vector[0], wPos[1]+vector[1])
                    #print(checkDir, " = checking:", nextWPos)
                    if (0 <= nextWPos[0] < len(labMap)) and (0 <= nextWPos[1]< len(labMap[0])):
                        if labMap[nextWPos[0]][nextWPos[1]] == "#" and nextWPos != wPos:
                            #print(checkDir, " = checking:", nextWPos, 'isValid')
                            isWallFound[checkDir] = nextWPos
    #print("adjwallFound", isWallFound)
    return isWallFound

def getFourthCoor(loopCoord):
    fourthDir = ''
    fourthCoor =  ''
    #print("loopCoord", loopCoord)
    for dir, coor in loopCoord.items():
        if coor == "":
            if dir == "up":
                fourthDir = dir
                fourthCoor = (loopCoord['right'][0]-1, loopCoord['left'][1]+1)
            elif dir == "right":
                fourthDir = dir
                fourthCoor = (loopCoord['up'][0]+1, loopCoord['bottom'][1]+1)
            elif dir == "bottom":
                fourthDir = dir
                fourthCoor = (loopCoord['left'][0]+1, loopCoord['right'][1]-1)
            else:
                fourthDir = dir
                fourthCoor = (loopCoord['bottom'][0]-1, loopCoord['up'][1]-1)
    return (fourthDir, fourthCoor)

def isLoopValid(loopCoord):
    isValid = True
    if 0 <= loopCoord['up'][0] < len(labMap) and 0 <= loopCoord['up'][1] < len(labMap[0]) and \
        0 <= loopCoord['right'][0] < len(labMap) and 0 <= loopCoord['right'][1] < len(labMap[0]) and \
        0 <= loopCoord['bottom'][0] < len(labMap) and 0 <= loopCoord['bottom'][1] < len(labMap[0]) and \
        0 <= loopCoord['left'][0] < len(labMap) and 0 <= loopCoord['left'][1] < len(labMap[0]):
        # get full gPath 
        # t -> r
        if "#" in labMap[loopCoord['right'][0]][loopCoord['up'][1]:loopCoord['right'][1]]:
            isValid = False
        # r -> b
        if "#" in [c[loopCoord['bottom'][1]] for c in labMap[loopCoord['right'][0]:loopCoord['bottom'][0]]]:
            isValid = False
        # b -> l
        if "#" in labMap[loopCoord['left'][0]][loopCoord['left'][1]+1:loopCoord['bottom'][1]]:
            isValid = False
        # l -> t
        if "#" in [c[loopCoord['up'][1]] for c in labMap[loopCoord['up'][0]+1:loopCoord['left'][0]]]:
            isValid = False
    return isValid

with open("../tinput",'r') as ofile:
    lNb = 0
    for line in ofile.readlines():
        line=line.strip("\n")
        labMap.append(list(line))
        if line.find('^') != -1:
            gPos = (lNb,line.find("^"))
        lNb+=1
    #print(gPos)

while not gLeft:
    loopCoord = {'up': '', 'right': '', 'bottom': '', 'left': ''}
    labMap, gPos, gDirIdx, rotated, gLeft = doMovement(labMap, gPos, gDirIdx)
    # When a wall is hit
    if rotated:
        wDir = validDir[gDirIdx-1]
        move = moveMap[wDir]
        wPos = (gPos[0]+move[0],gPos[1]+move[1])
        loopCoord[wDir] = wPos
        adjWalls = getAdjWalls(labMap, wPos, wDir)
        if adjWalls['next'] and adjWalls['previous']:
            loopCoord[dirChange[wDir]['next']] = adjWalls['next']
            loopCoord[dirChange[wDir]['previous']] = adjWalls['previous']
            fourthWall = getFourthCoor(loopCoord)
            print('fourth wall ', fourthWall)
            if labMap[fourthWall[1][0]][fourthWall[1][1]] != '#':
                loopCoord[fourthWall[0]] = fourthWall[1]
                #print('fourth wall ', fourthWall)
                #print(loopCoord)

        elif adjWalls['next'] and not adjWalls['previous']:
            loopCoord[dirChange[wDir]['next']] = adjWalls['next']
            scdWallDir = dirChange[wDir]['next']
            adjWalls = getAdjWalls(labMap, adjWalls['next'], scdWallDir)
            if adjWalls['next']:
                loopCoord[dirChange[scdWallDir]['next']] = adjWalls['next']
                fourthWall = getFourthCoor(loopCoord)
                print('fourth wall ', fourthWall)
                if labMap[fourthWall[1][0]][fourthWall[1][1]] != '#':
                    loopCoord[fourthWall[0]] = fourthWall[1]
                    #print('fourth wall ', fourthWall)
                    #print(loopCoord)

        elif not adjWalls['next'] and adjWalls['previous']:
            loopCoord[dirChange[wDir]['previous']] = adjWalls['previous']
            scdWallDir = dirChange[wDir]['previous']
            adjWalls = getAdjWalls(labMap, adjWalls['previous'], scdWallDir)
            if adjWalls['previous']:
                loopCoord[dirChange[scdWallDir]['previous']] = adjWalls['previous']
                fourthWall = getFourthCoor(loopCoord)
                print('fourth wall ', fourthWall)
                if labMap[fourthWall[1][0]][fourthWall[1][1]] != '#':
                    loopCoord[fourthWall[0]] = fourthWall[1]
                    #print('fourth wall ', fourthWall)
                    #print(loopCoord)
        
        # if 4 coor, check duplicates and clear path then +1
        if '' not in loopCoord.values() and list(loopCoord.values()) not in allLoop and isLoopValid(loopCoord):
            allLoop.append(list(loopCoord.values()))

print("Total : ", len(allLoop))

print(allLoop)