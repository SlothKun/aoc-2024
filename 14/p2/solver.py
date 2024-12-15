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

X = 103
Y = 101

X_MAX = X
Y_MAX = Y
ITER_MAX = X*Y


def drawMap(robotCoord):
    map = ''
    for x in range(X_MAX):
        for y in range(Y_MAX):
            if (x,y) in robotCoord.keys():
                map += str(robotCoord[(x,y)])
            else:
                map += '.'
    map += "\n"
    print(map)


with open("../input",'r') as ofile:
    robotManager = {}
    rbNb = 0
    for line in ofile.readlines():
        line = line.strip('\n').split(" ")
        c = [int(i) for i in line[0][2:].split(',')]
        v = [int(i) for i in line[1][2:].split(',')]
        robotManager[rbNb] = {'coor':c, 'velo':v}
        rbNb+=1

#print(robotManager)

for it in range(1, ITER_MAX):
    robotCoord = {}
    noOverlap = True
    OverlapNb = 0
    for rNb,carac in robotManager.items():
        c = carac['coor']
        v = carac['velo']
        cx = (c[1]+v[1]*it)%X_MAX
        cy = (c[0]+v[0]*it)%Y_MAX

        if (cx, cy) not in robotCoord.keys():
            robotCoord[(cx, cy)] = 1
        else: 
            robotCoord[(cx, cy)] += 1
            noOverlap = False
            break
    if noOverlap:
        print(it)
        drawMap(robotCoord)

print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
