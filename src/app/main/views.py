"""Main blueprint routes and view functions.

Routes/view functions:
    -   index(): Main page of webapp.  Landing page after user logs in.
"""

# %% Imports
# Standard system imports
from pathlib import Path

# Related third party imports
from flask import render_template, redirect, url_for
from flask_login import login_required

# Local application/library specific imports
from . import main
from ..testing import run_pytest
from utility.text_to_sql import IrisSQL


# %% Routes and view functions
@main.route('/', methods=["GET", "POST"])
@login_required
def index():
    """Index page of webapp."""
    return render_template('index.html')


@main.route('/datasets/', methods=["GET", "POST"])
# @login_required
def datasets():
    """Datasets sidemenu option."""
    dataset_paths = list(Path('/twe/src/db/sql').glob('*.sql'))
    filenames = [x.name for x in dataset_paths]
    dataset_names = [x.stem.split('_')[-1] for x in dataset_paths]
    idx = list(range(1, len(filenames)+1))
    return render_template('datasets.html', zip=zip(idx, filenames,
                                                    dataset_names))


@main.route('/train/', methods=["GET", "POST"])
@login_required
def train():
    """Train sidemenu option."""
    return render_template('train.html')


@main.route('/charts/', methods=["GET", "POST"])
@login_required
def charts():
    """Charts sidemenu option."""
    return render_template('charts.html')


@main.route('/tests/', methods=["GET", "POST"])
@login_required
def tests():
    """Landing page for Pytest reports."""
    return render_template('tests.html')


@main.route('/settings/', methods=["GET", "POST"])
@login_required
def settings():
    """Settings sidemenu option."""
    return render_template('settings.html')


@main.route('/run_unit_tests/')
@login_required
def run_unit_tests():
    """Prompt user to login, and then run Pytest unit tests."""
    run_pytest('unit')
    return redirect(url_for('main.test_reports', report='unit'))


@main.route('/run_integration_tests/')
@login_required
def run_integration_tests():
    """Prompt user to login, and then run Pytest integration tests."""
    run_pytest('integration')
    return redirect(url_for('main.test_reports', report='integration'))


@main.route('/test_reports/<report>')
@login_required
def test_reports(report):
    """Return page containing specified test report.

    Return a template that uses an iFrame to display a static test report
    generated by Pytest.
    """
    if 'unit' in report:
        if 'coverage' in report:
            url = "/static/test-report/unit_coverage/index.html"
            page_name = 'Unit Tests Code Coverage'
        else:
            url = "/static/test-report/unit_tests.html"
            page_name = 'Unit Tests'
    elif 'integration' in report:
        if 'coverage' in report:
            url = "/static/test-report/integration_coverage/index.html"
            page_name = 'Integration Tests Code Coverage'
        else:
            url = "/static/test-report/integration_tests.html"
            page_name = 'Integration Tests'
    else:
        url = 'invalid'
        page_name = None
    return render_template("test_reports.html", url=url,
                           page_name=page_name)


@main.route('/utility/iris')
@login_required
def convert_sql():
    """Convert text file to SQL create table commands."""
    iris_sql = IrisSQL('bezdekIris.data').iris_to_sql()
    return f'<h1>{iris_sql}</h1>'
