import pytest
import pandas as pd

from chind_eval import get_evaluation_results
from chind_eval.persistence import parse_results_into_result_df, persist_results_to_db
from chind_eval.utils import get_engine


@pytest.fixture(scope='module')
def results():
    return get_evaluation_results(3, 'mock')


@pytest.fixture(scope='module')
def results_df(results):
    return parse_results_into_result_df(results)


def test_evaluation_results_can_into_db(results_df):
    expected_columns = ['tokens_prompt', 'tokens_completion', 'tokens_total',
                        'model_response_answer', 'model_response_reason',
                        'execution_duration_ms', 'execution_start_datetime', 'model',
                        'treatment_drugind_id', 'treatment_condition_name',
                        'treatment_intervention_name', 'treatment_max_phase_for_ind']
    for col in expected_columns:
        assert col in results_df.columns
    assert len(results_df.columns) == len(expected_columns)


def test_can_persist_results_to_db(results):
    engine = get_engine('sqlite:///:memory:')
    persist_results_to_db(results, engine)
    df = pd.read_sql('select * from evaluation_results;', engine)
    assert len(df) == len(results)
