# Test Speed Analysis
Analyzes xcodebuild log for tests and determines if they are above specified threshold

Test Run Time Analysis

# Intent
     - Identify slow running tests for optimization
     - Begin to define test threshold stored in var - testThreshold
     - Identify how much time can be saved if all tests are below threshold

# Use
 Option 1) Place log files from successful CI run into a `logs` folder
               Script will automatically detect & output stats
           ex. `python test_speed_analysis.py`

 Option 2) Provide command line argument to specific folder path containing
               log files from CI build. Script will automatically detect &
               output stats
               `python test_speed_analysis.py __file_path_arg__`

           ex. `python test_speed_analysis.py /tmp/`
                added ability to integrate with CI

# TODO:
 - [ ] Dive deep into use options
 - [ ] Example running/output