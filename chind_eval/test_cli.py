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
    'python3 chind_eval analyze -o',
]
OUTPUT_FILES = [
    '#tmpdir#_output.csv',
    # 'output.parquet', # TODO Add support for parquet
    '#tmpdir#/#prefix#_output.json',
    'sqlite:///#tmpdir#/#prefix#_data.db',
]


@pytest.fixture(params=OUTPUT_FILES)
def output_file(request, tmpdir):
    output_file = request.param
    file = output_file.replace('#tmpdir#', str(tmpdir))
    return file


@pytest.fixture(params=COMMANDS)
def command(request, output_file,):
    cmd = request.param
    prefix = 'evaluation' if 'evaluation' in cmd else 'analysis'
    file = output_file.replace('#prefix#', prefix)
    if '-o' in cmd:
        cmd = f'{cmd} {file}'
    yield cmd


def test_command_runs_without_error(command, tmpdir):
    try:
        subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command '{command}' failed with error: {e}")


def test_commands_compose(tmpdir, output_file):
    uri = output_file
    cmd = f'python3 chind_eval evaluate -N 5 -o {uri}; python3 chind_eval analyze -i {uri} -o {uri}'
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command '{cmd}' failed with error: {e}")
