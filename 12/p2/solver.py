#!/usr/bin/env python3
import time
from itertools import groupby
from operator import itemgetter

start_time = time.time()

def getTime(start_time):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"

# Letter = Plant
# Region = Bloc of Plant
# Area = Nb of Plant in region
# Perimeter = Nb of sides of plants that isnt the same plant
# Price = area x perimeter

# Create a map
# Add every region together
# For each region, compute area and perimeter and get price
# Add price to total
# Also create a list of already mapped Coord

farm = []
nonMappedCoord = []
mappedCoord = []
total = 0

def getRegion(plant, coord, mappedCoord, mappedEdge):
    mappedCoord.append(coord)
    #print(f"-- Checking : {coord} --")
    tCoord = (coord[0]-1,coord[1])
    bCoord = (coord[0]+1,coord[1])
    lCoord = (coord[0],coord[1]-1)
    rCoord = (coord[0],coord[1]+1)
    if tCoord[0] >= 0 and tCoord not in mappedCoord: # Check top
        if farm[tCoord[0]][tCoord[1]] == plant:
            getRegion(plant, tCoord, mappedCoord, mappedEdge)
        elif tCoord not in mappedCoord:
            mappedEdge['up'].append(tCoord)
    elif tCoord not in mappedCoord:
        mappedEdge['up'].append(tCoord)

    if bCoord[0] < len(farm) and bCoord not in mappedCoord: # check down
        if farm[bCoord[0]][bCoord[1]] == plant:
            getRegion(plant, bCoord, mappedCoord, mappedEdge) 
        elif bCoord not in mappedCoord:
            mappedEdge['down'].append(bCoord)
    elif bCoord not in mappedCoord:
        mappedEdge['down'].append(bCoord)

    if lCoord[1] >= 0 and lCoord not in mappedCoord: #Check left
        if farm[lCoord[0]][lCoord[1]] == plant:
            getRegion(plant, lCoord, mappedCoord, mappedEdge)
        elif lCoord not in mappedCoord:
            mappedEdge['left'].append(lCoord)
    elif lCoord not in mappedCoord:
        mappedEdge['left'].append(lCoord)

    if rCoord[1] < len(farm[0]) and rCoord not in mappedCoord:# check right
        if farm[rCoord[0]][rCoord[1]] == plant:
            getRegion(plant, rCoord, mappedCoord, mappedEdge) 
        elif rCoord not in mappedCoord:
            mappedEdge['right'].append(rCoord)
    elif rCoord not in mappedCoord:
        mappedEdge['right'].append(rCoord)
    return mappedCoord, mappedEdge

def checkContinuity(mapEdge, dir):
    perimeter = 0
    y = 0 if dir in ['left', 'right'] else 1
    x = 1 if dir in ['left', 'right'] else 0
    for key, coor in groupby(mapEdge, lambda c: c[x]):
        coor = sorted(list(coor))
        coorToCmp = coor[0][y]
        for i in coor[1:]:
            if i[y]-1 != coorToCmp:
                perimeter+=1
            coorToCmp = i[y]
        perimeter+=1
    return perimeter

def func(val):
    return val[1]


# Map the farm
with open("../input",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        line = line.strip("\n")
        farm.append(line)
    #print(farm)

for l in range(len(farm)):
    nonMappedCoord += [(l,c) for c in range(len(line))]
#print(nonMappedCoord)

mappedEdge = []
while len(nonMappedCoord) != 0:
    letter = farm[nonMappedCoord[0][0]][nonMappedCoord[0][1]]
    # Get region
    mappedCoord, mappedEdge = getRegion(letter, nonMappedCoord[0], [], {'up':[],'down':[],'left':[],'right':[]})
    perimeter = 0
    area = len(set(mappedCoord))
    perimeter += checkContinuity(sorted(mappedEdge['up']), 'up')
    perimeter += checkContinuity(sorted(mappedEdge['down']), 'down')
    mappedEdge['left'].sort(key=func)
    perimeter += checkContinuity(mappedEdge['left'], 'left')
    mappedEdge['right'].sort(key=func)
    perimeter += checkContinuity(mappedEdge['right'], 'right')
    print(f"{letter} : a{area} * p{perimeter} = {area*perimeter}")
    total += area*perimeter
    # remove mapped Coord from list (symmetric difference)
    nonMappedCoord = list(set(nonMappedCoord) ^ set(mappedCoord))
print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
