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
ITER = 100

XT = 7
YT = 11

X = 103
Y = 101

X_MAX = X
Y_MAX = Y


with open("../input",'r') as ofile:
    robotCoord = {}
    for line in ofile.readlines():
        line = line.strip('\n').split(" ")
        c = [int(i) for i in line[0][2:].split(',')]
        v =[int(i) for i in line[1][2:].split(',')]
        cx = (c[1]+v[1]*ITER)%X_MAX
        cy = (c[0]+v[0]*ITER)%Y_MAX

        if (cx, cy) not in robotCoord.keys():
            robotCoord[(cx, cy)] = 1
        else: 
            robotCoord[(cx, cy)] += 1

map = ''
altMap = ''
print(robotCoord)


for x in range(X_MAX):
    for y in range(Y_MAX):
        if x == X_MAX//2 or y == Y_MAX//2:
            altMap += " "
        elif (x,y) in robotCoord.keys():
            altMap += str(robotCoord[(x,y)])
        else:
            altMap += '.'

        if (x,y) in robotCoord.keys():
            map += str(robotCoord[(x,y)])
        else:
            map += '.'
    map += "\n"
    altMap += "\n"

print(map)
print(altMap)


# Get solution
cadrant = [0,0,0,0] #tl,tr,bl,br
for c,v in robotCoord.items():
    if c[0] < X_MAX//2 and c[1] < Y_MAX//2: # topLeft
        cadrant[0] += v
    elif c[0] < X_MAX//2 and c[1] > Y_MAX//2: # topRight
        cadrant[1] += v
    elif c[0] > X_MAX//2 and c[1] < Y_MAX//2: # bottomLeft
        cadrant[2] += v
    elif c[0] > X_MAX//2 and c[1] > Y_MAX//2: # bottomRight
        cadrant[3] += v

print(cadrant)
total = cadrant[0]*cadrant[1]*cadrant[2]*cadrant[3]


print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
