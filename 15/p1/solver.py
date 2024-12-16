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

def move(robot, moves, walls, boxes):
    print(f"\n\n------ MOVING: START -----")
    for m in moves:
        dirV = moveVector[m]
        tmpRobot = (robot[0]+dirV[0], robot[1]+dirV[1])
        #print(f"tmp robot pos {tmpRobot} - Dir {m}")
        print("dir ", m)
        oob = False
        emptySpace = False
        boxToMove = []
        while tmpRobot in boxes or tmpRobot in walls and (not oob or not emptySpace):
            if tmpRobot in boxes:
                #print('found box')
                boxToMove.append(boxes.index(tmpRobot))
            elif tmpRobot in walls:
                #print('hitting a wall')
                oob = True
            else: 
                emptySpace = True
            tmpRobot = (tmpRobot[0]+dirV[0], tmpRobot[1]+dirV[1])
            #print(f"tmp robot pos {tmpRobot} - Dir {m}")

        if not oob:
            for b in boxToMove:
                boxes[b] = (boxes[b][0]+dirV[0], boxes[b][1]+dirV[1])
            robot = (robot[0]+dirV[0], robot[1]+dirV[1])
            print("robot new pos : ",robot)

    print(f"\nrobot : {robot}")
    print(f"boxes : {boxes}")
    print(f"------ MOVING: END -----")
    return robot, boxes

def getResult(boxes):
    print(f"\n\n------ RESULT: START -----")
    result = 0
    for b in boxes:
        result += 100 * b[0] + b[1]
    print(f"\n\n------ RESULT: END -----")    
    return result


with open("../input",'r') as ofile:
    moves = ''
    walls = []
    edgeWalls = {'up': [], 'down': [], 'left':[], 'right':[]}
    robot = (-1, -1)
    boxes = []
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
            maxCol = len(line)
            for colNb in range(len(line)):
                if line[colNb] == '#':
                    walls.append((lineNb,colNb))
                elif line[colNb] == 'O':
                    boxes.append((lineNb,colNb))
                elif line[colNb] == '@':
                    robot = (lineNb,colNb)
        else:
            moves += line
        lineNb+=1
    edgeWalls['up'] = [(0,y) for y in range(maxCol)]
    edgeWalls['down'] = [(maxLine-1,y) for y in range(maxCol)]
    edgeWalls['left'] = [(x,0) for x in range(maxCol)]
    edgeWalls['right'] = [(x,maxCol-1) for x in range(maxCol)]


print(f"walls : {walls}")
print(f"edgeWalls : {edgeWalls}")
print(f"boxes : {boxes}")
print(f"moves : {moves}")
print(f"robot : {robot}")
print(f"Max Line : {maxLine} - Max Col : {maxCol}")

robot, boxes = move(robot, moves, walls, boxes)
total = getResult(boxes)


print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
