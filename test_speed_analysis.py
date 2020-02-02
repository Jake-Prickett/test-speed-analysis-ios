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

class Analyzer:

    _timeAboveThreshold = 0.0

    def __init__(self, testThreshold=0.01, filePath="logs"):
        self.testThreshold = testThreshold
        self.filePath = filePath

    def printHeader(self):
        print "\n------------------------------------"
        print "| Test Speed Analysis              |"
        print "| Test Threashold: %.3fs           |" % self.testThreshold
        print "------------------------------------"

    def addTimeLost(self, value):
        diff = value - self.testThreshold

        self._timeAboveThreshold += diff

    def cleanup(self, fLine):
        fLine = fLine.replace("(", "")
        fLine = fLine.replace(")", "")
        fLine = fLine.split()
        
        return ("%s %s" % (fLine[2], fLine[3]), float(fLine[5]))

    def printOutput(self, fileName, fileTests):
        print "\n--------------- %s ---------------" % fileName
        print "Tests with runtime greater than %.1f s: %d" % (self.testThreshold, len(fileTests))
        
        for (testName, runTime) in fileTests:
            self.addTimeLost(runTime)
            print "%s - %.3fs" % (testName, runTime)

    def analyzeFile(self, fName, fPath):
        tests = []
        path = "%s/%s" % (fPath, fName)
        
        with open(path, "r") as file:
            for line in file:
                if "started" in line: continue
                if "Test Case" in line and "passed" in line:
                    tests.append(self.cleanup(line))

        tests = sorted(tests, key=lambda x: x[1], reverse=True)
        tests = filter(lambda x: x[1] > self.testThreshold, tests)

        self.printOutput(fName, tests)

    def printTimeLost(self):
        print "\n---------------------------"
        
        if self._timeAboveThreshold > 0.0:
            print "\nTotal Time Lost: %.2f mins" % (self._timeAboveThreshold/60)
        else:
            print "No Tests Above Threshold"
    
    def analyze(self):
        files = os.listdir(self.filePath)

        self.printHeader()

        for file in files:
            self.analyzeFile(file, self.filePath)

        self.printTimeLost()

def main():
    filePath = ""
    
    if ( len(sys.argv) - 1 ) == 1:
        filePath = str(sys.argv[1])
    else:
        filePath = "logs"

    analyzer = Analyzer()
    analyzer.analyze()

if __name__ == "__main__":
    try:
        main()
    except:
        print "\n!! ERROR! Issue Processing Log Files :( !!"
        print "------------------------------------------"
        print traceback.print_exc()
