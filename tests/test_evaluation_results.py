import pytest
from jsonschema import validate

from chind_eval import get_evaluation_results, get_json_schema_for_output


@pytest.fixture(scope='module')
def N():
    return 3


@pytest.fixture(scope='module')
def results(N):
    return get_evaluation_results(N, 'mock')


def test_can_get_correct_number_of_results(results, N):
    assert len(results) == N


def test_result_first_result_fits_schema(results):
    first_result = results[0]
    schema = get_json_schema_for_output()
    validate(first_result, schema)
