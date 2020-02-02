#
# Test Run Time Analysis
#
# Intent:
#      - Identify slow running tests for optimization
#      - Begin to define test threshold
# 
# usage: test_speed_analysis.py [-h] [-p PATH] [-m MAX] [-s]
# Process .log files generated when running Xcode Unit Tests.
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -p PATH, --path PATH  The location in which your .log files are located
#   -m MAX, --max MAX     The maximum time (in seconds) in which one Unit Test
#                         should take.
#   -s, --strict          Fail the run if tests are discovered over the
#                         threshold
# 
# Place .log files from successful CI run into a `logs` folder
#      Script will automatically detect & output stats
#      ex. `python test_speed_analysis.py`
#
# Jake Prickett
#

import os
import sys
import argparse
import traceback

class Analyzer:

    _timeAboveThreshold = 0.0

    def __init__(self, testThreshold=0.01, filePath="logs", strict=False):
        self.testThreshold = testThreshold
        self.filePath = filePath
        self.strict = strict

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
            if self.strict:
                print("\nFailure: Tests found with execution time greater than the provided threshold.")
                exit(1)
        else:
            print "No Tests Above Threshold"
    
    def analyze(self):
        files = os.listdir(self.filePath)

        self.printHeader()

        for file in files:
            self.analyzeFile(file, self.filePath)

        self.printTimeLost()

def main():
    parser = argparse.ArgumentParser(description='Process .log files generated when running Xcode Unit Tests.')
    
    parser.add_argument(
        '-p',
        '--path',
        default="logs", 
        help='The directory in which your .log files are located'
        )

    parser.add_argument(
        '-m',
        '--max', 
        default=0.01, 
        help='The maximum time (in seconds) in which one Unit Test should take.', 
        type=float
        )

    parser.add_argument(
        '-s', 
        '--strict',
        action='store_true',
        help='Fail the run if tests are discovered over the threshold'
        )

    args = parser.parse_args()
    
    analyzer = Analyzer(args.max, args.path, args.strict)
    analyzer.analyze()

if __name__ == "__main__":
    main()
