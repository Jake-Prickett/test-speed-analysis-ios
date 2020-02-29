# Test Speed Analysis
Analyzes xcodebuild log for tests and determines if they are above specified threshold

Test Run Time Analysis

# Intent
     - Identify slow running tests for optimization
     - Begin to define test threshold stored in var - testThreshold
     - Identify how much time can be saved if all tests are below threshold

# Use

Works with one `.log` file, or as many as you'd like in a directory! 

These are typically found in `~/Library/Logs/scan` or if you'd like to specify the path through Fastlane [Scan's buildlog_path command](https://docs.fastlane.tools/actions/scan/#parameters).

```
usage: test_analysis.py [-h] [-p PATH] [-m MAX] [-s]

Process .log files generated when running Xcode Unit Tests.

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The directory in which your .log files are located
  -m MAX, --max MAX     The maximum time (in seconds) in which one Unit Test
                        should take.
  -s, --strict          Fail the run if tests are discovered over the
                        threshold
```
