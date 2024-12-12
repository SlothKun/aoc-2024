import copy
import time

start_time = time.time()
cacheMult = {}
cacheSplit = {} 
ITER = 10

def getTime(start_time):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"

with open("../tinput2",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        line = line.strip("\n")
        stones = [int(s) for s in line.split()]
print(f"Starting with {stones}\n")


# Train on 0,1,2,3,4,5,6,7,8,9 for 5 iter each
# Save the result of those iter in cache (merge them too)
# then ITER and only every 5 turn we deal with digit
# Need to ignore them anytime else


for i in range(ITER):
    tmpStones = stones
    stoneToChange = len(stones)
    sChanged = 0
    sIdx = 0
    startIter = time.time()
    while sChanged < stoneToChange:
        sInt = stones[sIdx]
        sStr = str(sInt)
        sLen = len(sStr)
        if sInt == 0: # If stone == 0 : become 1
            tmpStones[sIdx] = 1
        elif sLen %2 == 0: # if len(str(stone))%2==0 : 2 stones -> left half / right half (without leading 0)
            if sInt not in cacheSplit.keys():
                mid = sLen//2
                #print(f"sIdx {sIdx} - s {s} : mid{mid}")
                halfnb = [sStr[:mid], sStr[mid:]]
                halfnbInt = [int(halfnb[0]),int(halfnb[1])]
                #print("half nb ")
                halfnbInt[1] = int(halfnb[1].lstrip('0')) if halfnbInt[1] != 0 else 0
                #print(f"halfs : {halfnb}")
                #tmpStones[sIdx] = halfnbInt[1]
                #tmpStones.insert(sIdx, halfnbInt[0]) # Insert first half before
                cacheSplit[sInt] = halfnbInt
            tmpStones[sIdx] = cacheSplit[sInt][1]
            tmpStones.insert(sIdx, cacheSplit[sInt][0]) # Insert first half before
            sIdx+=1 # Inc by one because we added 1 elem
        else: # Else stone*2024
            if sInt not in cacheMult.keys():
                cacheMult[sInt] = tmpStones[sIdx] * 2024
            tmpStones[sIdx] = cacheMult[sInt]
        sChanged+=1
        sIdx+=1
    stones = tmpStones
    print(f"{i+1}/{ITER} - Length : {len(stones)} - Total : {getTime(start_time)}")
    print(stones)
    print(f"Iter time: {getTime(startIter)}")

print(len(stones))
getTime(start_time)
