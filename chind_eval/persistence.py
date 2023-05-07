from typing import Dict, List

import pandas as pd
from sqlalchemy.engine import Engine

from chind_eval.utils import explode_dict_into_record


def parse_results_into_result_df(results: List[Dict]) -> pd.DataFrame:
    answer_df = pd.DataFrame([explode_dict_into_record(x) for x in results])
    columns = ['tokens_prompt', 'tokens_completion', 'tokens_total',
               'model_response_answer', 'model_response_reason',
               'execution_duration_ms', 'execution_start_datetime', 'model',
               'treatment_drugind_id', 'treatment_condition_name',
               'treatment_intervention_name', 'treatment_max_phase_for_ind']
    answer_df = answer_df[columns]
    return answer_df


def persist_results_to_db(results: List[Dict], engine: Engine):
    df = parse_results_into_result_df(results)
    df.to_sql('evaluation_results', engine, if_exists='append', index=False)
