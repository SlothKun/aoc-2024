#!/usr/bin/env python3
import time


start_time = time.time()
rules = {}
total = 0

def isLineValid(line):
    for pIdx in range(len(line)):
        p = line[pIdx]
        if rules.get(p) != None:
            if len(set(rules[p]['after']) & set(line[:pIdx])) != 0 or \
                len(set(rules[p]['before']) & set(line[pIdx:])) != 0:
                return False
    return True

def getBadRuleIdx(line,p,pIdx,search):
    violatedRule = set(rules[p]['before']) & set(line[pIdx:]) if search == 'before' else set(rules[p]['after']) & set(line[:pIdx])
    vrIdx = []
    for r in violatedRule:
        vrIdx.append(line.index(r))
    vrIdx.sort()
    return vrIdx

with open("../input",'r') as ofile:
    ruleDone = False
    for line in ofile.readlines():
        line=line.strip("\n")
        if line == "":
            ruleDone=True
        elif not ruleDone: # Populate rules dict
            line=line.split("|")
            if rules.get(line[0]) == None:
                rules[line[0]] = {"after":[],"before":[]}
            if rules.get(line[1]) == None:
                rules[line[1]] = {"after":[],"before":[]}

            rules[line[0]]["after"].append(line[1])
            rules[line[1]]["before"].append(line[0])
        else:
            line=line.split(",")
            validLine = isLineValid(line)
            pIdx = 0
            movedRight=False
            movedLeft=False
            print(line if not validLine else "")
            while not validLine:
                lineChanged = False
                #print("new line:", line)
                #print(pIdx)
                p = line[pIdx]
                if not movedLeft:
                    badIdx = getBadRuleIdx(line,p,pIdx,'before')
                    if len(badIdx) !=0:
                        movedRight=True
                        lineChanged = True
                        line.pop(pIdx)
                        line.insert(badIdx[0], p)
                        #print("newline transfo bef: ", line)
                if not movedRight:
                    badIdx = getBadRuleIdx(line,p,pIdx,'after')
                    if len(badIdx) !=0:
                        movedLeft=True
                        lineChanged = True
                        line.pop(pIdx)
                        line.insert(badIdx[0], p)
                        #print("newline transfo aft: ", line)
                if isLineValid(line):
                    print("VALID")
                    validLine = True
                    total += int(line[int(len(line)/2)])
                elif lineChanged:
                    pIdx=0
                else:
                    movedRight=False
                    movedLeft=False
                    pIdx+=1

print(total)
print("--- %s sec ---" % (time.time() - start_time))