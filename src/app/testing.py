"""Pytest related functions.

Functions:
    -   run_pytest: Run Pytest in a subprocess with MySQL credentials.
"""

# %% Imports
# Standard system imports
import subprocess

# Related third party imports

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
