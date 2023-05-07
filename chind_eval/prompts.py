import json
from dataclasses import dataclass
from typing import Dict, List

from chind_eval.chembl_treatments import get_chembl_treatments_df


@dataclass
class ModelPrompt:
    user: str
    system: str


def get_example_response() -> str:
    return '''{"answer": "don't know", "reason": "I'm dumb"}'''


def get_answer_values() -> List[str]:
    return ["strongly disagree", "disagree", "I do not know", "agree", "strongly agree"]


def get_schema_for_output() -> str:
    return '''
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "answer": {
            "type": "string",
            "enum": ["strongly disagree", "disagree", "don't know", "agree", "strongly agree"]
        },
        "reason": {
            "type": "string"
        }
    },
    "required": ["answer", "reason"]
}
'''


def get_persona_statement() -> str:
    return '''You are a medical expert who is conservative with what you consider to be a treatment. You are very clear when you aren't sure of something.'''


def get_output_requirements(schema: str) -> str:
    return f'''You only respond with json strings that fits the following schema:
    {schema}
that indicates the extent to which you agree with the statement given along with a reason for your answer.
    '''


def get_system_prompt() -> str:
    persona = get_persona_statement()
    output_requirements = get_output_requirements(get_schema_for_output())
    return f'''{persona} {output_requirements}'''


def get_user_prompt(intervention_name: str, condition_name: str) -> str:
    return f'''{intervention_name} can be a treament for {condition_name}.'''


def get_model_prompts_from_chembl(
    intervention_name: str,
    condition_name: str,
) -> ModelPrompt:
    return ModelPrompt(system=get_system_prompt(), user=get_user_prompt(intervention_name, condition_name))
