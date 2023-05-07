import pytest
from jsonschema import validate
import json

from chind_eval import get_json_schema_for_analysis
from chind_eval.prompts import get_answer_values


def test_result_first_result_fits_schema(analysis_results):
    schema = get_json_schema_for_analysis()
    json.dumps(analysis_results)
    validate(analysis_results, schema)


def test_schema_validates_mock():
    schema = get_json_schema_for_analysis()
    input = {
        'answer_distribution': {ans: .1 for ans in get_answer_values()},
        'total_tokens': {'average': 10.3, 'standard_devation': 2.3, 'total': 2000},
        'execution_time_ms': {'average': 10.3, 'standard_devation': 2.3, 'total': 2000},
        'n_indications': 100,
        'n_samples': 102,
        'model': 'mock',
    }
    validate(input, schema)
