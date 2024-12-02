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

def isReportSafe(report, evo, isSafe, firstIter=True, locked=False, srange=2):
   print(f"isSafe == {isSafe}, firstIter == {firstIter}, lock=={locked}")
   print(f"report : {report}")
   for lvlIdx in range(srange, len(report)):
         if isSafe == 0 and not firstIter and not locked:
            print("- - entered - -")
            newReport = report
            newReport.pop(lvlIdx-2)
            isSafe += isReportSafe(newReport, evo, isSafe, locked=True, srange=1)
            return isSafe
         elif isSafe <= -1:
            return -1
         if getEvoStatus(report[lvlIdx-1], report[lvlIdx]) != evo \
               or not isDiffSafe(report[lvlIdx-1], report[lvlIdx]):
            isSafe -= 1
         firstIter = False
   return 1

with open("../input", 'r') as ofile:
    for report in ofile.readlines():
        report = [int(nb) for nb in report.strip("\n").split()]
        reportList.append(report)

for report in reportList:
   print("--------")
   evo = getEvoStatus(report[0], report[1])
   diff = isDiffSafe(report[0], report[1])
   isSafe = 1 if evo != "eq" and diff else 0
   print("IS SAFE : ", isSafe)
   isSafe = isReportSafe(report, evo, isSafe, firstIter=False)
   print("ANSWER: ",isSafe)
   safeReport += 1 if isSafe == 1 else 0

print(safeReport)
