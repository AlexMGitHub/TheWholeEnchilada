"""Pytest related functions.

Functions:
    -   run_pytest: Run Pytest in a subprocess with MySQL credentials.

    -   last_run:  Returns date and time of last run of test reports.
"""

# %% Imports
# Standard system imports
from pathlib import Path
import re
import subprocess

# Related third party imports
from dateutil import parser

# Local application/library specific imports


# %% Testing functions
def run_pytest(test_type):
    """Run tests specified by test type.

    The variable test_type is used to determine the type of testing to be
    performed:  integration tests or unit tests.  Integration tests require
    MySQL root account credentials; unit tests only require a user account with
    admin privileges for the ml_data database.

    Pytest must be run as a subprocess, otherwise the results will never change
    upon subsequent testing.  This is due to Python caching modules inside the
    same process.
    """
    if test_type == 'integration':
        tests = 'integration'           # Run integration tests
        subpackage = 'murachs_mysql'    # Subpackage to check coverage for
    elif test_type == 'unit':
        tests = 'unit'                  # Run unit tests
        subpackage = 'app'              # Subpackage to check coverage for
    else:
        return  # Invalid test type
    file_path = 'src/app/static/test-report'
    subprocess.run(
        ["python", "-m", "pytest", "-v",            # Verbose mode
         f'tests/{tests}/',                         # Test directory to run
         f"--html={file_path}/{tests}_tests.html",  # HTML report
         f"--css={file_path}-css/my_report.css",    # Custom CSS
         "--self-contained-html",   # HTML and CSS in single file
         f"--cov={subpackage}",     # Subpackage to check code coverage for
         f"--cov-report=html:{file_path}/{tests}_coverage/"  # Coverage dir
         ], capture_output=False)


def find_date_time(file_path, pattern):
    """Extract date and time from test report."""
    with open(file_path, 'r') as report:
        test_report = report.read()
    m = re.search(pattern, test_report)
    return m.group(1), m.group(2)


def report_date_time():
    """Return date and time each test report was generated."""
    # Pytest reports
    unit_test_path = Path('src/app/static/test-report/unit_tests.html')
    integ_test_path = Path('src/app/static/test-report/'
                           'integration_tests.html')
    pytest_pattern = r'Report generated on (\d+-\w+-\d+) at (\d+:\d+:\d+)'
    # Create lists of paths and corresponding patterns
    file_paths = [unit_test_path, integ_test_path]
    # Get dates and times and parse into uniform format
    dates, times = [], []
    for fpath in file_paths:
        date, time = find_date_time(fpath, pytest_pattern)
        dates.append(str(parser.parse(date)).split(' ')[0])
        times.append(str(parser.parse(time)).split(' ')[1])
    return dates, times
