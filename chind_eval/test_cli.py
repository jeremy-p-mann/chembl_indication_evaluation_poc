import subprocess

import pytest


@pytest.fixture(params=['python3 chind_eval evaluate -N 5 -o output.json', 'python3 chind_eval evaluate', 'python3 chind_eval analyze'])
def command(request):
    return request.param


def test_command_runs_without_error(command):
    try:
        subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command '{command}' failed with error: {e}")
