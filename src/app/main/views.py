"""Main blueprint routes and view functions.

Routes/view functions:
    -   index(): Main page of webapp.  Landing page after user logs in.
"""

# %% Imports
# Standard system imports
from pathlib import Path

# Related third party imports
from bokeh.embed import server_session
from bokeh.util.token import generate_session_id
from flask import session, render_template, redirect, url_for, current_app
from flask_login import login_required

# Local application/library specific imports
from . import main
from .dataset_manager import DatasetManager
from ..testing import run_pytest, report_date_time
from .. import db
from utility.text_to_sql import IrisSQL, BostonSQL


# %% Globals
mgr = DatasetManager(session)


# %% Routes and view functions
@main.route('/', methods=["GET", "POST"])
@login_required
def index():
    """Index page of webapp."""
    return render_template('index.html', username=session['username'])


# %% Datasets section
@main.route('/datasets/', methods=["GET", "POST"])
@login_required
def datasets():
    """Datasets sidemenu option."""
    dataset = mgr.current_dataset()
    if dataset is None:
        loaded_names = mgr.list_loaded()
        return render_template('datasets.html', data_names=loaded_names)
    else:
        return redirect(url_for('main.eda'))


@main.route('/datasets/eda/')
@login_required
def eda():
    """Return page containing Bokeh visualizations for EDA."""
    dataset = mgr.current_dataset()
    if dataset is None:
        return redirect(url_for('main.datasets'))
    loaded_names = mgr.list_loaded()
    mgr.dump_data(dataset)  # Pickle data and write to Docker volume
    # Generate session ID and obtain JavaScript from Bokeh server
    session_id = generate_session_id()
    script = server_session(url='http://bokeh:5006/eda/',
                            session_id=session_id)
    # Replace Docker alias in URL with localhost
    script = script.replace("http://bokeh:5006", "http://localhost:5006")
    # Use the script in the rendered page
    return render_template("dataset_preview.html", script=script,
                           data_names=loaded_names)


@main.route('/datasets/load/')
@login_required
def load_datasets():
    """Show user datasets available to be loaded into the MySQL database."""
    idx, data_paths, data_names, desc_paths, descrips, sql_paths, \
        sql_names, loaded, table_size, \
        loaded_names = mgr.build_datasets_table()
    return render_template('load_datasets.html',
                           zip=zip(idx, data_paths, data_names, desc_paths,
                                   descrips, sql_paths, sql_names, loaded,
                                   table_size),
                           data_names=loaded_names)


@main.route('/data_file/static/datasets/<name>/<datatype>/<data>/display')
@login_required
def data_file(name, datatype, data):
    """Return page containing specified data.

    Return a template that uses an iFrame to display a static data text file.
    """
    url = f'/static/datasets/{name}/{datatype}/{data}'
    page_name = data
    return render_template("data_file.html", url=url, page_name=page_name)


@main.route('/data_file/static/datasets/<name>/<datatype>/<data>/load_sql')
@login_required
def load_sql(name, datatype, data):
    """Load specified SQL file into MySQL database as table."""
    if not data.endswith('.sql'):
        return
    sql_path = Path(f'static/datasets/{name}/{datatype}/{data}')
    db.create_table(sql_path)
    return redirect(url_for('main.datasets'))


# %% Train Section
@main.route('/train/', methods=["GET", "POST"])
@login_required
def train():
    """Load Bokeh training visualization to train model."""
    dataset = mgr.current_dataset()
    if dataset is None:
        return redirect(url_for('main.datasets'))
    # Generate session ID and obtain JavaScript from Bokeh server
    session_id = generate_session_id()
    script = server_session(url='http://bokeh:5006/train/',
                            session_id=session_id)
    # Replace Docker alias in URL with localhost
    script = script.replace("http://bokeh:5006", "http://localhost:5006")
    # Use the script in the rendered page
    return render_template("train.html", script=script)


# %% Results Section
@main.route('/results/', methods=["GET", "POST"])
@login_required
def results():
    """Results sidemenu option."""
    dataset = mgr.current_dataset()
    if dataset is None:
        return redirect(url_for('main.datasets'))
    # Generate session ID and obtain JavaScript from Bokeh server
    session_id = generate_session_id()
    script = server_session(url='http://bokeh:5006/results/',
                            session_id=session_id)
    # Replace Docker alias in URL with localhost
    script = script.replace("http://bokeh:5006", "http://localhost:5006")
    # Use the script in the rendered page
    return render_template('results.html', script=script)


# %% Tests Section
@main.route('/tests/', methods=["GET", "POST"])
@login_required
def tests():
    """Landing page for Pytest reports."""
    dates, times = report_date_time()
    return render_template('tests.html',
                           unit_date=dates[0], unit_time=times[0],
                           integ_date=dates[1], integ_time=times[1])


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


# %% Temporary routes
@main.route('/utility/<data>')
# @login_required
def convert_sql(data):
    """Convert text file to SQL create table commands."""
    if data == 'iris':
        iris_sql = IrisSQL().iris_to_sql()
        return f'<h1>{iris_sql}</h1>'
    elif data == 'boston':
        boston_sql = BostonSQL().boston_to_sql()
        return f'<h1>{boston_sql}</h1>'
