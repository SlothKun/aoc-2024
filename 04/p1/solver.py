#!/usr/bin/env python3

RULE = {
    "X": {0: "X" ,1: "M", 2:"A", 3:"S"},
    "M": {-1: "X", 0:"M", 1:"A", 2:"S"},
    "A": {-2: "X", -1:"M", 0:"A", 1:"S"},
    "S": {-3: "X", -2:"M", -1:"A", 0:"S"},
}

textBlock = []

with open("../input",'r') as ofile:
    for line in ofile.readlines():
        textBlock.append(line.strip("\n"))

total = 0
for lIdx in range(len(textBlock)):
    for cIdx in range(len(textBlock[lIdx])):
        letterRules = RULE[textBlock[lIdx][cIdx]]
        letterRules = [[i for i in letterRules.keys()], [-i for i in letterRules.keys()]]
        for rule in letterRules:
            words={"h": "", "v": "", "d":""}
            for i in rule:
                words['h'] += textBlock[lIdx][cIdx+i] if 0 <= cIdx+i < len(textBlock[lIdx]) else ""
                words['v'] += textBlock[lIdx+i][cIdx]  if 0 <= lIdx+i < len(textBlock) else ""
                words['d'] += textBlock[lIdx+i][cIdx+i] if 0 <= cIdx+i < len(textBlock[lIdx]) and 0 <= lIdx+i < len(textBlock) else ""
            for w in words.values():
                if w in ["XMAS", "SAMX"]:
                    print("Word : ", w)
                    print("Coord :", lIdx, " - ", cIdx)
                    total+=1
print(total)
