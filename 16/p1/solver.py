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
nodeGraph = {}
end = (-1,-1)
rein = (-1,-1)
maxLine = 0
maxCol = 0

with open("../tinput",'r') as ofile:
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
            cIdx+=1
        maze.append(line)
        visited.append([False for i in range(cIdx)])
        lIdx+=1
    maxLine=lIdx
    maxCol=len(line)

#print(walls)
#print(rein)
#print(end)
#print(maxLine)
#print(maxCol)




# Build graph
"""
for lIdx in range(1, maxLine-1):
    for cIdx in range(1, maxCol-1):
        if (lIdx, cIdx) not in walls:
            nodeGraph[(lIdx, cIdx)] = {'cost': [],'coor':[], 'dirIdx':[]}
            # Create a set of unvisited node
            visited.append((lIdx, cIdx))
            for vIdx in range(len(dirVector)):
                v = dirVector[vIdx]
                if (lIdx+v[0], lIdx+v[1]) not in walls:
                    nodeGraph[(lIdx, cIdx)]['coor'].append((lIdx+v[0], lIdx+v[1]))
                    nodeGraph[(lIdx, cIdx)]['dirIdx'].append(vIdx)
                    nodeGraph[(lIdx, cIdx)]['cost'].append(-1)
"""


# Find shortest Path using Dijkstra
def dijkstra(maze, visited, start, end):
    solution = []
    queue = []
    visited[start[0]][start[1]] = True




print(nodeGraph)
print(visited)
print(maze)
#dijkstra(maze, visited, start, end)

print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
