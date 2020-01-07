#
# Test Run Time Analysis
#
# Intent:
#      - Identify slow running tests for optimization
#      - Begin to define test threshold stored in var - testThreshold
#
# Use:
# Option 1) Place log files from successful CI run into a `logs` folder
#               Script will automatically detect & output stats
#           ex. `python test_speed_analysis.py`
#
# Option 2) Provide command line argument to specific folder path containing
#               log files from CI build. Script will automatically detect &
#               output stats
#               `python test_speed_analysis.py __file_path_arg__`
#
#           ex. `python test_speed_analysis.py /tmp/`
#                added ability to integrate with CI
#
# Jake Prickett
#

import os
import sys
import traceback

testThreshold = 0.7
timeAboveThreshold = 0.0

def printHeader():
    print "\n------------------------------------"
    print "| Test Speed Analysis              |"
    print "| Test Threashold: %.1fs            |" % testThreshold
    print "------------------------------------"

def addTimeLost(value):
    diff = value - testThreshold
        
    global timeAboveThreshold
    timeAboveThreshold += diff

def cleanup(fLine):
    fLine = fLine.replace("(", "")
    fLine = fLine.replace(")", "")
    fLine = fLine.split()
    
    return ("%s %s" % (fLine[2], fLine[3]), float(fLine[5]))

def printOutput(fileName, fileTests):
    print "\n--------------- %s ---------------" % fileName
    print "Tests with runtime greater than %.1f s: %d" % (testThreshold, len(fileTests))
    
    for (testName, runTime) in fileTests:
        addTimeLost(runTime)
        print "%s - %.3fs" % (testName, runTime)

def analyzeFile(fName, fPath):
    tests = []
    path = "%s/%s" % (fPath, fName)
    
    with open(path, "r") as file:
        for line in file:
            if "started" in line: continue
            if "Test Case" in line and "passed" in line:
                tests.append(cleanup(line))

    tests = sorted(tests, key=lambda x: x[1], reverse=True)
    tests = filter(lambda x: x[1] > testThreshold, tests)

    printOutput(fName, tests)

def printTimeLost():
    print "\n---------------------------"
    
    if timeAboveThreshold > 0.0:
        print "\nTotal Time Lost: %.2f mins" % (timeAboveThreshold/60)
    else:
        print "No Tests Above Threshold"


def main():
    filePath = ""
    
    if ( len(sys.argv) - 1 ) == 1:
        filePath = str(sys.argv[1])
    else:
        filePath = "logs"

    files = os.listdir(filePath)

    printHeader()

    for file in files:
        analyzeFile(file, filePath)

    printTimeLost()

try:
    main()
except:
    print "\n!! ERROR! Issue Processing Log Files :( !!"
    print "------------------------------------------"
    print traceback.print_exc()
