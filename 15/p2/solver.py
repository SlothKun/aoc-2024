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
moveVector = {'^':(-1,0),'>':(0,1),'v':(1,0),'<':(0,-1)}

def findNearBoxes(dir, boxIdx, boxToMove):
    vector = moveVector[dir]
    nBoxl = (boxesl[boxIdx][0]+vector[0], boxesl[boxIdx][1]+vector[1])
    nBoxr = (boxesr[boxIdx][0]+vector[0], boxesr[boxIdx][1]+vector[1])
    #print(nBoxl, nBoxr)
    #print(nBoxl in walls)
    #print(nBoxr in walls)
    #print(nBoxl in boxesr or nBoxl in boxesl)
    #print(nBoxr in boxesr or nBoxr in boxesl)
    #print(boxToMove)
    if nBoxl in walls or nBoxr in walls:
        return []
    if nBoxl in boxesr or nBoxl in boxesl:
        boxIdx = boxesl.index(nBoxl) if nBoxl in boxesl else boxesr.index(nBoxl)
        #print(boxId)
        if boxIdx not in boxToMove:
            boxToMove.append(boxIdx)
            boxToMove = findNearBoxes(dir, boxIdx, boxToMove)
            if len(boxToMove) == 0:
                return []
    if nBoxr in boxesr or nBoxr in boxesl:
        boxIdx = boxesl.index(nBoxr) if nBoxr in boxesl else boxesr.index(nBoxr)
        #print(boxId)
        if boxIdx not in boxToMove:
            boxToMove.append(boxIdx)
            boxToMove = findNearBoxes(dir, boxIdx, boxToMove)
            if len(boxToMove) == 0:
                return []
    return boxToMove

def move(robot, moves, walls, boxesl, boxesr):
    print(f"\n\n------ MOVING: START -----")
    for m in moves:
        dirV = moveVector[m]
        tmpRobot = (robot[0]+dirV[0], robot[1]+dirV[1])
        #print(f"tmp robot pos {tmpRobot} - Dir {m}")
        #print("dir ", m)
        oob = False
        emptySpace = False
        boxToMove = []
        while tmpRobot in boxesl or tmpRobot in boxesr or tmpRobot in walls and (not oob or not emptySpace):
            if tmpRobot in boxesl or tmpRobot in boxesr:
                boxIdx = boxesl.index(tmpRobot) if tmpRobot in boxesl else boxesr.index(tmpRobot)
                if boxIdx not in boxToMove:
                    boxToMove.append(boxIdx)
                    boxToMove = findNearBoxes(m, boxIdx, boxToMove)
                    if len(boxToMove) == 0:
                        oob = True
            elif tmpRobot in walls:
                oob = True
            else: 
                emptySpace = True
            tmpRobot = (tmpRobot[0]+dirV[0], tmpRobot[1]+dirV[1])

        if not oob:
            #print("box to move : ", boxToMove)
            for b in boxToMove:
                boxesl[b] = (boxesl[b][0]+dirV[0], boxesl[b][1]+dirV[1])
                boxesr[b] = (boxesr[b][0]+dirV[0], boxesr[b][1]+dirV[1])
            robot = (robot[0]+dirV[0], robot[1]+dirV[1])
            #print("robot new pos : ",robot)
            #print(f"boxesl : {boxesl}")
            #print(f"boxesr : {boxesr}")

    #print(f"\nrobot : {robot}")
    #print(f"boxesl : {boxesl}")
    #print(f"boxesr : {boxesr}")
    #print(f"------ MOVING: END -----")
    return robot, boxesl, boxesr

def getResult(boxesl):
    print(f"\n\n------ RESULT: START -----")
    result = 0
    for b in boxesl:
        result += 100 * b[0] + b[1]
    print(f"\n\n------ RESULT: END -----")    
    return result


with open("../input",'r') as ofile:
    moves = ''
    walls = []
    edgeWalls = {'up': [], 'down': [], 'left':[], 'right':[]}
    robot = (-1, -1)
    boxesl = []
    boxesr = []
    boxId = 0
    lineNb = 0
    mapped = False
    maxLine = 0
    maxCol = 0
    for line in ofile.readlines():
        line = line.strip('\n')
        if line == "":
            maxLine = lineNb
            mapped = True
        elif not mapped:
            maxCol = len(line)*2
            colNb = 0
            for item in line:
                if item == '#':
                    walls.append((lineNb,colNb))
                    walls.append((lineNb,colNb+1))
                elif item == 'O':
                    boxesl.append((lineNb,colNb))
                    boxesr.append((lineNb,colNb+1))
                    boxId += 1
                elif item == '@':
                    robot = (lineNb,colNb)
                colNb += 2
        else:
            moves += line
        lineNb+=1
    edgeWalls['up'] = [(0,y) for y in range(maxCol)]
    edgeWalls['down'] = [(maxLine-1,y) for y in range(maxCol)]
    edgeWalls['left'] = [(x,0) for x in range(maxCol)]
    edgeWalls['right'] = [(x,maxCol-1) for x in range(maxCol)]


#print(f"walls : {walls}")
#print(f"edgeWalls : {edgeWalls}")
#print(f"boxesl : {boxesl}")
#print(f"boxesr : {boxesr}")
#print(f"moves : {moves}")
#print(f"robot : {robot}")
#print(f"Max Line : {maxLine} - Max Col : {maxCol}")

robot, boxesl, boxesr = move(robot, moves, walls, boxesl, boxesr)
total = getResult(boxesl)


print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")