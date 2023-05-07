import json
import os
import subprocess

import pandas as pd
import pytest

from chind_eval.utils import get_engine

COMMANDS = [
    'python3 chind_eval evaluate',
    'python3 chind_eval analyze',
    'python3 chind_eval analyze -m mock',
    'python3 chind_eval evaluate -N 5 -o',
]
OUTPUT_FILES = [
    '#tmpdir#_output.csv',
    # 'output.parquet', # TODO Add support for parquet
    '#tmpdir#/#prefix#_output.json',
    'sqlite:///#tmpdir#/#prefix#_data.db',
]


@pytest.fixture(params=OUTPUT_FILES)
def output_file(request, ):
    output_file = request.param
    return output_file


@pytest.fixture(params=COMMANDS)
def command(request, output_file, tmpdir):
    cmd = request.param
    prefix = 'evaluation' if 'evaluation' in cmd else 'analysis'
    file = output_file.replace('#prefix#', prefix)
    file = file.replace('#tmpdir#', str(tmpdir))
    if '-o' in cmd:
        cmd = f'{cmd} {file}'
    yield cmd


def test_command_runs_without_error(command, tmpdir):
    try:
        subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command '{command}' failed with error: {e}")
    prefix = 'evaluation' if 'evaluation' in command else 'analysis'
    if 'sqlite' in command:
        uri = f'sqlite:///{tmpdir}/{prefix}_data.db'
        assert os.path.exists(f'{tmpdir}/{prefix}_data.db'), os.listdir(tmpdir)
        engine = get_engine(uri)
        df = pd.read_sql(f'select * from {prefix}_results;', engine)
    elif 'output.json' in command:
        with open(f"{tmpdir}/{prefix}_output.json", 'r') as file:
            results = json.load(file)
    elif 'output.csv' in command:
        df = pd.read_csv(f'{tmpdir}/{prefix}_output.csv')
