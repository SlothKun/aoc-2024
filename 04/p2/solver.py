#!/usr/bin/env python3

RULE = {
    "A": {-1:"M", 0:"A", 1:"S"},
}

textBlock = []
validatedCoord = []
total = 0

with open("../input",'r') as ofile:
    for line in ofile.readlines():
        textBlock.append(list(line.strip("\n")))

for lIdx in range(len(textBlock)):
    for cIdx in range(len(textBlock[lIdx])):
        if textBlock[lIdx][cIdx] == "A":
            letterRules = RULE[textBlock[lIdx][cIdx]]
            letterRules = [[i for i in letterRules.keys()], [-i for i in letterRules.keys()]]

            for rule in letterRules:
                words={"d":"", "id":""}
                wordCoords={"d":[], "id":[]}
                for i in rule:
                    words['d'] += textBlock[lIdx+i][cIdx+i] if 0 <= cIdx+i < len(textBlock[lIdx]) and 0 <= lIdx+i < len(textBlock) else ""
                    wordCoords['d'].append((lIdx+i,cIdx+i))
                    words['id'] += textBlock[lIdx+i][cIdx-i] if 0 <= cIdx-i < len(textBlock[lIdx]) and 0 <= lIdx+i < len(textBlock) else ""
                    wordCoords['id'].append((lIdx+i,cIdx-i))
                print(words['d'], words['id'])
                if words['d'] in ["MAS", "SAM"] and words['id'] in ["MAS", "SAM"] and \
                wordCoords['d'] not in validatedCoord and wordCoords['id'] not in validatedCoord:
                        validatedCoord.append(wordCoords['d'])
                        validatedCoord.append(wordCoords['id'])
                        total+=1

print(len(validatedCoord))
print(total/2) # Coord counted x2


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