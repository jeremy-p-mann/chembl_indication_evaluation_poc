import json
import re
from typing import Dict, List

import pandas as pd
from sqlalchemy.engine import Engine

from chind_eval.utils import explode_dict_into_record, get_engine


def parse_results_into_result_df(results: List[Dict]) -> pd.DataFrame:
    answer_df = pd.DataFrame([explode_dict_into_record(x) for x in results])
    columns = ['tokens_prompt', 'tokens_completion', 'tokens_total',
               'model_response_answer', 'model_response_reason',
               'execution_duration_ms', 'execution_start_datetime', 'model',
               'treatment_drugind_id', 'treatment_condition_name',
               'treatment_intervention_name', 'treatment_max_phase_for_ind']
    answer_df = answer_df[columns]
    return answer_df


def persist_results_to_db(results_df: pd.DataFrame, engine: Engine):
    results_df.to_sql('evaluation_results', engine,
                      if_exists='append', index=False,)


def persist_results_to_json(results: List[Dict], output_file_name: str):
    with open(output_file_name, "w") as outfile:
        json.dump(results, outfile)


def get_uri_type(uri):
    if re.match(r'.*://', uri):
        return 'sql'
    elif uri.endswith('.json'):
        return 'json'
    elif uri.endswith('.parquet'):
        return 'parquet'
    elif uri.endswith('.csv'):
        return 'csv'
    else:
        return 'unknown'


def persist_results(results: List[Dict], output: str):
    uri_type = get_uri_type(output)
    if uri_type == 'json':
        persist_results_to_json(results, output)
        return
    df = parse_results_into_result_df(results)
    if uri_type == 'parquet':
        df.to_parquet(output, index=False)
    elif uri_type == 'csv':
        df.to_csv(output, index=False)
    elif uri_type == 'sql':
        engine = get_engine(output)
        persist_results_to_db(df, engine)
    else:
        raise ValueError('Invalid format')
