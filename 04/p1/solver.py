#!/usr/bin/env python3

RULE = {
    "X": {0: "X" ,1: "M", 2:"A", 3:"S"},
    "M": {-1: "X", 0:"M", 1:"A", 2:"S"},
    "A": {-2: "X", -1:"M", 0:"A", 1:"S"},
    "S": {-3: "X", -2:"M", -1:"A", 0:"S"},
}

textBlock = []
validatedCoord = []
total = 0

with open("../input",'r') as ofile:
    for line in ofile.readlines():
        textBlock.append(list(line.strip("\n")))

for lIdx in range(len(textBlock)):
    for cIdx in range(len(textBlock[lIdx])):
        letterRules = RULE[textBlock[lIdx][cIdx]]
        letterRules = [[i for i in letterRules.keys()], [-i for i in letterRules.keys()]]

        for rule in letterRules:
            words={"h": "", "v": "", "d":"", "id":""}
            wordCoords={"h":[],"v":[],"d":[], "id":[]}
            for i in rule:
                words['h'] += textBlock[lIdx][cIdx+i] if 0 <= cIdx+i < len(textBlock[lIdx]) else ""
                wordCoords['h'].append((lIdx,cIdx+i))
                words['v'] += textBlock[lIdx+i][cIdx]  if 0 <= lIdx+i < len(textBlock) else ""
                wordCoords['v'].append((lIdx+i,cIdx))
                words['d'] += textBlock[lIdx+i][cIdx+i] if 0 <= cIdx+i < len(textBlock[lIdx]) and 0 <= lIdx+i < len(textBlock) else ""
                wordCoords['d'].append((lIdx+i,cIdx+i))
                words['id'] += textBlock[lIdx+i][cIdx-i] if 0 <= cIdx-i < len(textBlock[lIdx]) and 0 <= lIdx+i < len(textBlock) else ""
                wordCoords['id'].append((lIdx+i,cIdx-i))
            for cat, w in words.items():
                if w in ["XMAS", "SAMX"] and wordCoords[cat] not in validatedCoord:
                    validatedCoord.append(wordCoords[cat])
                    total+=1
print(len(validatedCoord))
print(total)


print("------DRAWING-----\n")
coordList = []

for x in validatedCoord:
    for y in x:
        coordList.append(y)

for lIdx in range(len(textBlock)):
    for cIdx in range(len(textBlock[lIdx])):
        if (lIdx, cIdx) not in coordList:
            textBlock[lIdx][cIdx] = "."

txt=""
for x in textBlock:
    txt+=''.join(x)+"\n"

print(txt)