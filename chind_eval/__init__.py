import json
from typing import Dict, List, Union

import pandas as pd

from chind_eval.chembl_treatments import get_chembl_treatments_df
from chind_eval.model import get_model
from chind_eval.prompts import get_answer_values, get_model_prompts_from_chembl
from chind_eval.utils import explode_dict_into_record


def format_results(model_output: Dict, model: str, treatment: Dict) -> Dict:
    parsed_response = json.loads(model_output['response'])
    return {
        'tokens': model_output['tokens'],
        'model_response': parsed_response,
        'execution_duration_ms': model_output['execution_duration_ms'],
        'execution_start_datetime': model_output['execution_start_datetime'],
        'model': model,
        'treatment': {
            'drugind_id': treatment['drugind_id'],
            'condition_name': treatment['condition_name'],
            'intervention_name': treatment['intervention_name'],
            'max_phase_for_ind': treatment['max_phase_for_ind'],
        }
    }


def get_json_schema_for_output() -> Dict:
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "tokens": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "integer"},
                    "completion": {"type": "integer"},
                    "total": {"type": "integer"}
                },
                "required": ["prompt", "completion", "total"]
            },
            "model": {"type": "string"},
            "model_response": {
                "type": "object",
                "properties": {
                    "answer": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["answer", "reason"]
            },
            "execution_duration_ms": {"type": "number"},
            "execution_start_datetime": {"type": "string", "format": "date-time"},
            "treatment": {
                "type": "object",
                "properties": {
                    "drugind_id": {"type": "integer"},
                    "condition_name": {"type": "string"},
                    "intervention_name": {"type": "string"},
                    "max_phase_for_ind": {"type": "integer"},
                },
                "required": ["drugind_id", "condition_name", "intervention_name", "max_phase_for_ind"]

            }
        },
        "required": [
            "tokens",
            "model_response",
            "model",
            "execution_duration_ms",
            "execution_start_datetime",
            "treatment"
        ]
    }


def get_evaluation_results(
    N: int,
    model_name: str,
) -> List[Dict]:
    print(f'getting model {model_name}')
    model = get_model(model_name)
    print(f'getting {N} treatments')
    treatments = get_chembl_treatments_df(N).to_dict('records')
    evaluations = []
    for treatment in treatments:
        prompt = get_model_prompts_from_chembl(
            treatment['intervention_name'], treatment['condition_name']
        )
        print(f'getting output for treatment: {treatment}')
        model_output = model(prompt)
        formatted_results = format_results(model_output, model_name, treatment)
        print(f'Obtained results {formatted_results}')
        evaluations.append(formatted_results)
    return evaluations


def get_json_schema_for_analysis() -> Dict:
    return {
        "type": "object",
        "properties": {
            "answer_distribution": {
                "type": "object",
                "properties": {
                    x: {"type": "number", "minimum": 0, "maximum": 1}
                    for x in get_answer_values()
                },
                "required": get_answer_values()
            },
            "total_tokens": {
                "type": "object",
                "properties": {
                    "average": {"type": "number"},
                    "standard_devation": {"type": "number"},
                    "total": {"type": "number"}
                },
                "required": ["average", "standard_devation", 'total']
            },
            "execution_time_ms": {
                "type": "object",
                "properties": {
                    "average": {"type": "number"},
                    "standard_devation": {"type": "number"},
                    "total": {"type": "number"}
                },
                "required": ["average", "standard_devation", 'total']
            },
            "n_indications": {"type": "integer"},
            "n_samples": {"type": "integer"},
            "model": {"type": "string"}
        },
        "required": [
            "answer_distribution",
            "total_tokens",
            "execution_time_ms",
            "n_indications",
            "model",
            "n_samples"
        ]
    }


def get_analysis(
    evaluation: Union[List[Dict], pd.DataFrame],
    model_name: str,
) -> Dict:
    if isinstance(evaluation, List):
        answer_df = pd.DataFrame([explode_dict_into_record(x) for x in evaluation])
    else:
        answer_df = evaluation
    avg_tokens, std_tokens, total_tokens = (
        answer_df['tokens_total'].mean(),
        answer_df['tokens_total'].std(),
        answer_df['tokens_total'].sum()
    )
    avg_execution, std_execution, total_execution = (
        answer_df['execution_duration_ms'].mean(),
        answer_df['execution_duration_ms'].std(),
        answer_df['execution_duration_ms'].sum()
    )
    answer_distribution = answer_df['model_response_answer'].value_counts(
        normalize=True).to_dict()
    n_indications = answer_df['treatment_drugind_id'].nunique()
    n_samples = len(answer_df)
    ans = {
        'answer_distribution': {
            ans: answer_distribution.get(ans, 0)
            for ans in get_answer_values()
        },
        'total_tokens': {'average': avg_tokens, 'standard_devation': std_tokens, 'total': int(total_tokens)},
        'execution_time_ms': {'average': avg_execution, 'standard_devation': std_execution, 'total': int(total_execution)},
        'n_indications': int(n_indications),
        'n_samples': int(n_samples),
        'model': str(model_name),
    }
    return ans


