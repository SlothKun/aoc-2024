#!/usr/bin/env python3

reportList = []
safeReport = 0

def getEvoStatus(nb1, nb2):
   if nb1 < nb2:
      return "inc"
   elif nb1 > nb2:
      return "dec"
   elif nb1 == nb2:
      return "eq"

def isDiffSafe(nb1, nb2):
    if 1 <= abs(nb1-nb2) <= 3:
        return True
    else:
        return False

with open("../input", 'r') as ofile:
    for report in ofile.readlines():
        report = [int(nb) for nb in report.strip("\n").split()]
        reportList.append(report)

for report in reportList:
    evo = getEvoStatus(report[0], report[1])
    diff = isDiffSafe(report[0], report[1])
    isSafe = 1 if evo != "eq" and diff else 0
    for lvlIdx in range(2, len(report)):
        if not isSafe:
            break
        if getEvoStatus(report[lvlIdx-1], report[lvlIdx]) != evo \
           or not isDiffSafe(report[lvlIdx-1], report[lvlIdx]):
            isSafe = 0
    safeReport += isSafe

print(safeReport)
