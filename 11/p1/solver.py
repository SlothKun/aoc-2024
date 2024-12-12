import copy
import time

start_time = time.time()
ITER = 25

def getTime(start_time):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"

with open("../input",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        line = line.strip("\n")
        stones = [int(s) for s in line.split()]
print(stones)


for i in range(ITER):
    tmpStones = stones
    stoneToChange = len(stones)
    sChanged = 0
    sIdx = 0
    while sChanged < stoneToChange:
        sInt = stones[sIdx]
        sStr = str(sInt)
        sLen = len(sStr)
        #print(s)
        if sInt == 0: # If stone == 0 : become 1
            tmpStones[sIdx] = 1
        elif sLen %2 == 0: # if len(str(stone))%2==0 : 2 stones -> left half / right half (without leading 0)
            mid = sLen//2
            #print(f"sIdx {sIdx} - s {s} : mid{mid}")
            halfnb = [sStr[:mid], sStr[mid:]]
            halfnbInt = [int(halfnb[0]),int(halfnb[1])]
            #print("half nb ")
            halfnbInt[1] = int(halfnb[1].lstrip('0')) if halfnbInt[1] != 0 else 0
            #print(f"halfs : {halfnb}")
            tmpStones[sIdx] = halfnbInt[1]
            tmpStones.insert(sIdx, halfnbInt[0]) # Insert first half before
            sIdx+=1 # Inc by one because we added 1 elem
            #print(tmpStones)
        else: # Else stone*2024
            tmpStones[sIdx] *= 2024
        sChanged+=1
        sIdx+=1
    stones = tmpStones
    print(f"{i}/{ITER} - {getTime(start_time)}")
    #print(f"Nb of stones after {i+1} blink: {len(stones)}")
    #print(f"stones after {i+1} blink: {stones}")
print(len(stones))
getTime(start_time)
