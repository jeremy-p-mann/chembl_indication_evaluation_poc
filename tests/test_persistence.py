import pandas as pd
import pytest

from chind_eval import get_evaluation_results
from chind_eval.persistence import (parse_results_into_result_df, parse_analysis_to_df,
                                    persist_evaluation_to_db, persist_analysis_to_db, get_uri_type)
from chind_eval.utils import get_engine
from chind_eval.prompts import get_answer_values


@pytest.fixture(scope='module')
def results():
    return get_evaluation_results(3, 'mock')


@pytest.fixture(scope='module')
def results_df(results):
    return parse_results_into_result_df(results)


@pytest.fixture(scope='module')
def analysis_df(analysis_results):
    return parse_analysis_to_df([analysis_results])



def test_evaluation_results_can_into_db(results_df):
    expected_columns = ['tokens_prompt', 'tokens_completion', 'tokens_total',
                        'model_response_answer', 'model_response_reason',
                        'execution_duration_ms', 'execution_start_datetime', 'model',
                        'treatment_drugind_id', 'treatment_condition_name',
                        'treatment_intervention_name', 'treatment_max_phase_for_ind']
    for col in expected_columns:
        assert col in results_df.columns
    assert len(results_df.columns) == len(expected_columns)


def test_analysis_results_can_into_db(analysis_df):
    expected_columns = [
        *[f'answer_distribution_{ans}' for ans in get_answer_values()],
        'total_tokens_average',
        'total_tokens_standard_devation', 'total_tokens_total',
        'execution_time_ms_average', 'execution_time_ms_standard_devation',
        'execution_time_ms_total', 'n_indications', 'n_samples', 'model']
    for col in expected_columns:
        assert col in analysis_df.columns
    assert len(analysis_df.columns) == len(expected_columns)


def test_can_persist_analysis_to_db(analysis_df):
    engine = get_engine('sqlite:///:memory:')
    persist_analysis_to_db(analysis_df, engine)
    df = pd.read_sql('select * from analysis_results;', engine)
    assert len(df) == len(analysis_df)


def test_can_persist_evaluation_to_db(results_df):
    engine = get_engine('sqlite:///:memory:')
    persist_evaluation_to_db(results_df, engine)
    df = pd.read_sql('select * from evaluation_results;', engine)
    assert len(df) == len(results_df)



@pytest.mark.parametrize("url,expected", [
    ('sqlite:///data.db', 'sql'),
    ('foo.json', 'json'),
    ('postgresql://user@localhost', 'sql'),
    ('postgresql://user:secret@localhost', 'sql'),
    ('postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp', 'sql'),
    ('postgresql://localhost/mydb?user=other&password=secret', 'sql'),
    ('fooc.csv', 'csv'),
    ('foo.parquet', 'parquet'),
    ('unknown.xyz', 'unknown')
])
def test_get_uri_type(url, expected):
    assert get_uri_type(url) == expected
