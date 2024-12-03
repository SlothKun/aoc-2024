#!/usr/bin/env python3

reportList = []
safeReport = 0

def isEvoSafe(report):
   evoRef = ""
   evo = ""
   for nIdx in range(0,len(report)-1):
      if report[nIdx] < report[nIdx+1]:
         evo = "inc"
      elif report[nIdx] > report[nIdx+1]:
         evo = "dec"
      elif report[nIdx] == report[nIdx+1]: 
         evo = "eq"

      if evoRef == "":
         evoRef = evo
      elif evo != evoRef or evo == "eq":
         return False
   return True

def isDiffSafe(report):
   for i in range(0,len(report)-1):
      if not 1 <= abs(report[i] - report[i+1]) <= 3:
        return False
   return True

def genAltReports(report):
   allReport = [report]
   for i in range(0, len(report)):
      currentReport = []
      if i == 0:
         currentReport += report[i+1:]
      elif i == len(report)-1:
         currentReport += report[:i]
      else:
         currentReport += report[:i]
         currentReport += report[i+1:]
      allReport.append(currentReport)  
   return allReport


with open("../input", 'r') as ofile:
    for report in ofile.readlines():
        report = [int(nb) for nb in report.strip("\n").split()]
        reportList.append(report)

for report in reportList:
   altReports = genAltReports(report)
   for altReport in altReports:
      if isDiffSafe(altReport) and isEvoSafe(altReport):
         safeReport += 1
         break

print("TOTAL : ", safeReport)