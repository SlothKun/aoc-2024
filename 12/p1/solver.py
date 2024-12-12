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

# Data struct :
# Dict :
#   plant Lettre :
#       regionX :
#           coordList = []
#           area = X
#           perimeter = Y
#           price = Z
farm = []
nonMappedCoord = []
plants = {}
total = 0

def getRegion(sCoord):
    pass

# Map the farm
with open("../tinput",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        line = line.strip("\n")
        farm.append(line)
    print(farm)

for l in range(len(farm)):
    nonMappedCoord += [(l,c) for c in range(len(line))]
print(nonMappedCoord)

while len(nonMappedCoord) != 0:
    # Get region
    mappedCoord, price = getRegion(nonMappedCoord[0])
    total += price
    # remove mapped Coord from list (symmetric difference)
    nonMappedCoord = list(set(nonMappedCoord) ^ set(mappedCoord))





print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
