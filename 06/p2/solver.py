#!/usr/bin/env python3

validDir = ['up','right','bottom','left']
moveMap = {'up':(-1,0), 'right':(0,1), 'bottom':(1,0), 'left':(0,-1)}
guardPos = (0,0)
guardDirIdx = 0
guardLeft = False
visitedPos = []
labMap = []

with open("../input",'r') as ofile:
    lNb = 0
    for line in ofile.readlines():
        line=line.strip("\n")
        labMap.append(line)
        if line.find('^') != -1:
            guardPos = (lNb,line.find("^"))
            visitedPos.append(guardPos)
        lNb+=1
    print(guardPos)

while not guardLeft:
    # move all the way until obstacle or empty
    path = []

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

print("Total : ", len(visitedPos))
