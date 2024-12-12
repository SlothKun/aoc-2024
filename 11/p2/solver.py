import copy
import time

start_time = time.time()
nbCount = {}
opCache = {}
ITER = 75
total = 0

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
        for n in line.split():
            n = int(n)
            if n not in nbCount.keys(): nbCount[n] = 0
            nbCount[n] += 1


# Train on 0,1,2,3,4,5,6,7,8,9 for 5 iter each
# Save the result of those iter in cache (merge them too)
# then ITER and only every 5 turn we deal with digit
# Need to ignore them anytime else


for i in range(ITER):
    startIter = time.time()
    tmpNbCount = copy.deepcopy(nbCount)
    for sInt in sorted(nbCount.keys()):
        sStr = str(sInt)
        sLen = len(sStr)
        if sInt == 0: # If stone == 0 : become 1
            if 1 not in tmpNbCount.keys(): tmpNbCount[1] = 0
            tmpNbCount[1] += nbCount[sInt] if sInt in nbCount.keys() else 1
        elif sLen %2 == 0: # if len(str(stone))%2==0 : 2 stones -> left half / right half (without leading 0)
            mid = sLen//2
            halfnb = [sStr[:mid], sStr[mid:]]
            halfnbInt = [int(halfnb[0]),int(halfnb[1])]
            halfnbInt[1] = int(halfnb[1].lstrip('0')) if halfnbInt[1] != 0 else 0

            if halfnbInt[0] not in tmpNbCount.keys(): tmpNbCount[halfnbInt[0]] = 0
            if halfnbInt[1] not in tmpNbCount.keys(): tmpNbCount[halfnbInt[1]] = 0
            tmpNbCount[halfnbInt[0]] += nbCount[sInt]
            tmpNbCount[halfnbInt[1]] += nbCount[sInt]
        else: # Else stone*2024
            newNb = sInt * 2024
            if newNb not in tmpNbCount.keys(): tmpNbCount[newNb] = 0
            tmpNbCount[newNb] += nbCount[sInt]
        tmpNbCount[sInt] -= nbCount[sInt]
    print(f"Iter : {i+1}/{ITER} - Took : {getTime(start_time)}")
    nbCount = {**nbCount, **tmpNbCount}
for v in nbCount.values():
    total+=v
print(f"\nResult: {total} - Took {getTime(start_time)}")
