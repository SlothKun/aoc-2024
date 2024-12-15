#!/usr/bin/env python3
import time
import numpy as np

def getTime(start_time):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"

start_time = time.time()
total = 0

def solve(claw):
    a = np.array([[claw['A'][0],claw['B'][0]],[claw['A'][1],claw['B'][1]]])
    b = np.array([claw['Prize'][0], claw['Prize'][1]])
    result = np.linalg.solve(a,b)
    result[0] = round(result[0])
    result[1] = round(result[1])
    if result[0]*claw['A'][0]+result[1]*claw['B'][0] == claw['Prize'][0] and \
       result[0]*claw['A'][1]+result[1]*claw['B'][1] == claw['Prize'][1]:
        print(result[0]*cost['A']+result[1]*cost['B'])
        return result[0]*cost['A']+result[1]*cost['B']
    else:
        return 0

# 100 presses max
# total => sum of all the fewest token
# some can be = 0 if need 100 presses
with open("../input",'r') as ofile:
    inputCount = 0
    claw = {'A': [], 'B': [], 'Prize':[]}
    cost = {'A':3,'B':1}
    for line in ofile.readlines():
        line = line.strip('\n').split(" ")
        if inputCount == 0:
            claw['A'] = [int(line[2][2:-1]), int(line[3][2:])]
            inputCount += 1
        elif inputCount == 1:
            claw['B'] = [int(line[2][2:-1]), int(line[3][2:])]
            inputCount += 1
        elif inputCount == 2:
            #claw['Prize'] = [int(line[1][2:-1]), int(line[2][2:])]
            claw['Prize'] = [int(line[1][2:-1])+10000000000000, int(line[2][2:])+10000000000000]
            inputCount += 1
        elif len(line) == 1:
            # Compute Prize
            print(claw)
            total += solve(claw)
            # Reset values
            inputCount = 0
            claw = {'A': [], 'B': [], 'Prize':[]}



print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
