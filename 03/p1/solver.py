#!/usr/bin/env python3
import re

def getAllMatches(instLine):
    return re.findall(r"mul\(([0-9]{1,3},[0-9]{1,3})\)", instLine)


with open("../input", 'r') as ofile:
    total = 0
    for instLine in ofile.readlines():
        instLine = instLine.strip("\n")
        result = getAllMatches(instLine)
        for r in result:
            nbList = r.split(',')
            total += int(nbList[0]) * int(nbList[1])
    print(total)
