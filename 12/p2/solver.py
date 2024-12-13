#!/usr/bin/env python3
import time

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
                mappedEdge.append((tCoord[0],'up'))
    elif tCoord not in mappedCoord:
            mappedEdge.append((tCoord[0],'up'))

    if bCoord[0] < len(farm) and bCoord not in mappedCoord: # check down
        if farm[bCoord[0]][bCoord[1]] == plant:
            getRegion(plant, bCoord, mappedCoord, mappedEdge) 
        elif bCoord not in mappedCoord:
                mappedEdge.append((bCoord[0],'down'))
    elif bCoord not in mappedCoord:
            mappedEdge.append((bCoord[0],'down'))

    if lCoord[1] >= 0 and lCoord not in mappedCoord: #Check left
        if farm[lCoord[0]][lCoord[1]] == plant:
            getRegion(plant, lCoord, mappedCoord, mappedEdge)
        elif lCoord not in mappedCoord:
                mappedEdge.append((lCoord[1],'left'))
    elif lCoord not in mappedCoord:
            mappedEdge.append((lCoord[1],'left'))

    if rCoord[1] < len(farm[0]) and rCoord not in mappedCoord:# check right
        if farm[rCoord[0]][rCoord[1]] == plant:
            getRegion(plant, rCoord, mappedCoord, mappedEdge) 
        elif rCoord not in mappedCoord:
                mappedEdge.append((rCoord[1],'right'))
    elif rCoord not in mappedCoord:
            mappedEdge.append((rCoord[1],'right'))

    return mappedCoord, mappedEdge

# Map the farm
with open("../tinput3",'r') as ofile:
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
    mappedCoord, mappedEdge = getRegion(letter, nonMappedCoord[0], [], [])
    #getRegion(letter, nonMappedCoord[0], [], [])
    perimeter = len(set(mappedEdge))
    area = len(set(mappedCoord))
    print(f"{letter} : a{area} * p{perimeter} = {area*perimeter}")
    print(f"MappedCoord :", sorted(list(set(mappedCoord))))
    print(f"mappedEdge :", sorted(list(set(mappedEdge))))
    total += area*perimeter
    # remove mapped Coord from list (symmetric difference)
    nonMappedCoord = list(set(nonMappedCoord) ^ set(mappedCoord))
    #print("nonMappedCoord: ", nonMappedCoord)

print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
