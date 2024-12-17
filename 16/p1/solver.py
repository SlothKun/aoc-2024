#!/usr/bin/env python3
import time

# https://tschinz.github.io/days-of-algo/content/notebooks/010-maze-solver-dijkstra.html
# https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Related_problems_and_algorithms

def getTime(start_time):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"

start_time = time.time()
total = 0

allDir = ['up', 'right', 'down', 'left']
dirVector = [(-1,0), (0,1), (1,0), (0,-1)]
visited = []
reinDirIdx = 1
walls = []
end = (-1,-1)
rein = (-1,-1)
maxLine = 0
maxCol = 0
junctions = {}
corner = {}
empty = []
lines = {}
paths = {}

with open("../tinput1",'r') as ofile:
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
                rein = (lIdx, cIdx)
                empty.append((lIdx, cIdx))
            else:
                empty.append((lIdx, cIdx))
            cIdx+=1
        maze.append(line)
        visited.append([False for i in range(cIdx)])
        lIdx+=1
    maxLine=lIdx
    maxCol=len(line)

print()
#print(rein)
#print(end)
#print(maxLine)
#print(maxCol)

# Get junctions
for e in empty:
    tmpJ = []
    for v in dirVector:
        if (e[0]+v[0],e[1]+v[1]) not in walls:
            tmpJ.append((e[0]+v[0],e[1]+v[1]))
    if len(tmpJ) > 2:
        junctions[e] = tmpJ
        empty.remove(e)
    elif len(tmpJ) == 2:
        corner[e] = tmpJ
    else:
        pass


print(f"Walls : {walls} - {len(walls)}\n")
print(f"Junctions : {junctions} - {len(junctions)}\n")
print(f"Empty : {empty} - {len(empty)}\n")
print(f"Corner : {corner} - {len(corner)}\n")

cPos = rein
pathId = 0
#while True:
    #nPos =



    


print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
