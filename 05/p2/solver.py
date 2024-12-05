#!/usr/bin/env python3

rules = {}
total = 0

with open("../tinput",'r') as ofile:
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
            validLine = True
            for pIdx in range(len(line)):
                p = line[pIdx]
                if rules.get(p) != None:
                    if len(set(rules[p]['after']) & set(line[:pIdx])) != 0 or \
                       len(set(rules[p]['before']) & set(line[pIdx:])) != 0:
                        validLine=False
            if validLine:
                total += int(line[int(len(line)/2)])

print(total)
