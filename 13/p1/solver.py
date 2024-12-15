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

def solve(claw):
    for b in range(0,101):
        a = ((claw['Prize'][0] - claw['B'][0]*b)/claw['A'][0])
        if a.is_integer() and a <= 100 and b <= 100 and \
            (a*claw['A'][0]+b*claw['B'][0]) == claw['Prize'][0] and \
            (a*claw['A'][1]+b*claw['B'][1]) == claw['Prize'][1]:
            print(f"A = {a} | B = {b} ")
            return a*cost['A']+b*cost['B']
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
        print
        if inputCount == 0:
            claw['A'] = [int(line[2][2:-1]), int(line[3][2:])]
            inputCount += 1
        elif inputCount == 1:
            claw['B'] = [int(line[2][2:-1]), int(line[3][2:])]
            inputCount += 1
        elif inputCount == 2:
            claw['Prize'] = [int(line[1][2:-1]), int(line[2][2:])]
            inputCount += 1
        elif len(line) == 1:
            # Compute Prize
            print(claw)
            total += solve(claw)
            # Reset values
            inputCount = 0
            claw = {'A': [], 'B': [], 'Prize':[]}



print(f"Answer : {total} - Program took : {getTime(start_time)} to run.")
