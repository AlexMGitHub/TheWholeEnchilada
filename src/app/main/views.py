"""Main blueprint routes and view functions.

Routes/view functions:
    -   index(): Main page of webapp.  Landing page after user logs in.
"""

# %% Imports
# Standard system imports
from pathlib import Path
import pickle

# Related third party imports
from bokeh.embed import server_session
from bokeh.util.token import generate_session_id
from flask import session, render_template, redirect, url_for, current_app
from flask_login import login_required

# Local application/library specific imports
from . import main
from ..testing import run_pytest
from .. import db
from utility.text_to_sql import IrisSQL, BostonSQL


# %% Routes and view functions
@main.route('/', methods=["GET", "POST"])
@login_required
def index():
    """Index page of webapp."""
    return render_template('index.html', username=session['username'])


@main.route('/datasets/', methods=["GET", "POST"])
# @login_required
def datasets():
    """Datasets sidemenu option."""
    dataset = session.get('dataset')
    datasets_path = Path('/twe/src/app/static/datasets')
    datasets = list(datasets_path.glob('*/'))
    data_names = [x.name for x in datasets]
    loaded = [db.query_table_exists(x) for x in data_names]
    loaded_names = [x for x, y in zip(data_names, loaded) if y]
    if dataset is None:
        return render_template('datasets.html', data_names=loaded_names)
    else:
        return redirect(url_for('main.dataset_preview', dataset=dataset))


@main.route('/summary/')
def query_summary():
    """"""
    summary = {}
    result = db.describe_table(session['dataset'])
    return f"<p>{result}</p>"
    for dictionary in result:
        for key, val in dictionary.items():
            if key not in summary:
                summary[key] = [val]
            else:
                summary[key].append(val)
    summary_table = []
    for key, val in summary.items():
        summary_table.append([key] + val)
    return f"<p>{summary_table}</p>"


@main.route('/datasets/<dataset>')
# @login_required
def dataset_preview(dataset):
    """"""
    session['dataset'] = dataset
    datasets_path = Path('/twe/src/app/static/datasets')
    datasets = list(datasets_path.glob('*/'))
    data_names = [x.name for x in datasets]
    loaded = [db.query_table_exists(x) for x in data_names]
    loaded_names = [x for x, y in zip(data_names, loaded) if y]
    summary = db.describe_table(session['dataset'])
    return render_template('dataset_preview.html', dataset=dataset,
                           data_names=loaded_names, summary=summary)


@main.route('/datasets/load/')
# @login_required
def load_datasets():
    """"""
    datasets_path = Path('/twe/src/app/static/datasets')
    app_path = datasets_path.parent.parent
    datasets = list(datasets_path.glob('*/'))
    idx = list(range(1, len(datasets)+1))
    data_paths = [list((x / 'data').glob('*.*'))[0].relative_to(app_path)
                  for x in datasets]
    data_names = [x.name for x in datasets]
    desc_paths = [list((x / 'desc').glob('*.*'))[0].relative_to(app_path)
                  for x in datasets]
    descrips = [x.name for x in desc_paths]
    sql_paths = [list((x / 'sql').glob('*.sql'))[0].relative_to(app_path)
                 for x in datasets]
    sql_names = [x.name for x in sql_paths]
    loaded = [db.query_table_exists(x) for x in data_names]
    loaded_names = [x for x, y in zip(data_names, loaded) if y]
    table_size = [db.query_table_size(x) for x in data_names]
    return render_template('load_datasets.html', zip=zip(idx,
                                                         data_paths,
                                                         data_names,
                                                         desc_paths,
                                                         descrips,
                                                         sql_paths,
                                                         sql_names,
                                                         loaded,
                                                         table_size
                                                         ),
                           data_names=loaded_names
                           )


@main.route('/data_file/static/datasets/<name>/<datatype>/<data>/display')
# @login_required
def data_file(name, datatype, data):
    """Return page containing specified data.

    Return a template that uses an iFrame to display a static data text file.
    """
    print("HERE")
    url = '/static/datasets/' + name + '/' + datatype + '/' + data
    page_name = data
    return render_template("data_file.html", url=url, page_name=page_name)


@main.route('/data_file/static/datasets/<name>/<datatype>/<data>/load_sql')
# @login_required
def load_sql(name, datatype, data):
    """Load specified SQL file into MySQL database as table."""
    if not data.endswith('.sql'):
        return
    sql_path = Path(f'static/datasets/{name}/{datatype}/{data}')
    db.create_table(sql_path)
    return redirect(url_for('main.datasets'))


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


@main.route('/bokeh/<dataset>')
# @login_required
def bokeh(dataset):
    """"""
    # Write data file to volume based on user-selected dataset
    dataset = session.get('dataset')
    if dataset is None:
        return redirect(url_for('main.datasets'))
    data = {}
    table = db.get_table(dataset)
    data['table'] = table
    if dataset == 'iris':
        data['metadata'] = {
            'dataset': 'iris',
            'type': 'classification',
            'target': 'class'
        }
    elif dataset == 'boston':
        data['metadata'] = {
            'dataset': 'boston',
            'type': 'regression',
            'target': 'CRIM'
        }
    elif dataset == 'autompg':
        data['metadata'] = {
            'dataset': 'autompg',
            'type': 'regression',
            'target': 'mpg'
        }
    data['metadata']['summary'] = db.describe_table(dataset)
    data_path = Path(f'/twe/src/bokeh_server/data/{dataset}.data')
    print(data_path)
    with open(data_path, 'wb') as data_file:
        pickle.dump(data, data_file)
    session_id = generate_session_id()
    script = server_session(url='http://bokeh:5006/eda/',
                            session_id=session_id)
    # Delete data file after receiving script
    # data_path.unlink()
    # Replace Docker alias in URL with localhost
    script = script.replace("http://bokeh:5006", "http://localhost:5006")
    # Use the script in the rendered page
    return render_template("dataset_preview.html", script=script)
