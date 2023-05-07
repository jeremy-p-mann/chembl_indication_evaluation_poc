import json
import subprocess

import pandas as pd
import pytest

from chind_eval.utils import get_engine

COMMANDS = [
    'python3 chind_eval evaluate -N 5 -o',
    'python3 chind_eval evaluate',
    'python3 chind_eval analyze',
]
OUTPUT_FILES = [
    'output.csv',
    # 'output.parquet', # TODO Add support for parquet
    'output.json',
    'sqlite:///data.db',
]


@pytest.fixture(params=OUTPUT_FILES)
def output_file(request, ):
    output_file = request.param
    try:
        subprocess.check_output(f'rm {output_file}', shell=True)
    except:
        pass
    return output_file


@pytest.fixture(params=COMMANDS)
def command(request, output_file):
    cmd = request.param
    if '-o' in cmd:
        return f'{cmd} {output_file}'
    return cmd


def test_command_runs_without_error(command):
    try:
        subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command '{command}' failed with error: {e}")
    if 'sqlite' in command:
        engine = get_engine('sqlite:///data.db')
        df = pd.read_sql('select * from evaluation_results;', engine)
        subprocess.check_output('rm data.db', shell=True)
        assert 5 == len(df)
    if 'output.json' in command:
        with open("output.json", 'r') as file:
            results = json.load(file)
        assert 5 == len(results)
        subprocess.check_output('rm output.json', shell=True)
    if 'output.csv' in command:
        df = pd.read_csv('output.csv')
        assert 5 == len(df)
        subprocess.check_output('rm output.csv', shell=True)
