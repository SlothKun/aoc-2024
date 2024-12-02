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

def isReportSafe(report, evo):
   for lvlIdx in range(1, len(report)):
      print(lvlIdx-1, " - ", lvlIdx)
      if getEvoStatus(report[lvlIdx-1], report[lvlIdx]) != evo \
            or not isDiffSafe(report[lvlIdx-1], report[lvlIdx]):
         print("OCCURED ON : ", report[lvlIdx-1])
         return lvlIdx-1
   return None

with open("../input", 'r') as ofile:
    for report in ofile.readlines():
        report = [int(nb) for nb in report.strip("\n").split()]
        reportList.append(report)

for report in reportList:
   print("--------")
   evo = getEvoStatus(report[0], report[1])
   isSafe = isReportSafe(report, evo)
   print("ANSWER: ",isSafe)
   if isSafe != None:
      newReport = report
      newReport.pop(isSafe)
      evo = getEvoStatus(newReport[0], newReport[1])
      print("newReport", newReport)
      isSafe = isReportSafe(newReport, evo)
   print("ANSWER: ",isSafe)
   safeReport += 1 if isSafe == None else 0

print(safeReport)
