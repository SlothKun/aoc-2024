#!/usr/bin/env python3
import re

def getAllMatches(instLine, isDo):
    regex = re.compile("(mul\(([0-9]{1,3},*)+\))|(do\(\))|(don't\(\))")
    result=[]
    for m in regex.finditer(instLine):
        print(m)
        if "mul(" in m.group() and isDo:
            result.append(m.group().strip("mul(").strip(")"))
        elif "don't()" in m.group() and isDo:
            isDo = False
        elif "do()" in m.group() and not isDo:
            isDo = True
    return result, isDo


with open("../input", 'r') as ofile:
    total = 0
    isDo = True
    for instLine in ofile.readlines():
        instLine = instLine.strip("\n")
        result, isDo = getAllMatches(instLine, isDo)
        for r in result:
            nbList = r.split(',')
            total += int(nbList[0]) * int(nbList[1])
    print(total)
