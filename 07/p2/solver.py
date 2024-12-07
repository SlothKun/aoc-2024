import itertools

def compute(nbs, ops):
    #print(f"-- compute {nbs} | {ops} --")
    nbIdx = 0
    for op in ops:
        nbs[1] = str(eval(nbs[0]+op+nbs[1]))
        nbs.pop(0)
    #print("Result:", nbs[0])
    #print("".join(ops), nbs)
    return int(nbs[0])

def isResultValid(nbs, ops, expectedResult):
    result = compute(nbs[:], ops[:]) 
    return (True,result) if result == expectedResult else (False,0)

def getSolution(nbs, ops, expectedResult): 
    opsList = [list(i) for i in itertools.product(['+', '*', ''], repeat=len(ops))]
    for opsi in opsList:
        matched, result = isResultValid(nbs[:], opsi[:], expectedResult)
        if matched: return result
    return 0


def genOpList(ops):
    opList = []
    for x in range(0, len(ops)):
        #print(x)
        #print(''.join(ops))
        for y in range(x, len(ops)):
            ops[y] = "*"
            #print(''.join(ops))
            ops[y] = "+"
        ops[x] = "*"

total = 0
with open("../input",'r') as ofile:
    lNb = 0
    for line in ofile.readlines():
        matched = False
        line=line.strip("\n").split(": ")
        expectedResult = int(line[0])
        nbs = [nb for nb in line[1].split(" ")]
        ops = ['+' for i in range(len(nbs)-1)]
        #print(f"---- {nbs} - {expectedResult} -----")
        #genOpList(ops[:])
        total += getSolution(nbs[:], ops[:], expectedResult)
print(total)
