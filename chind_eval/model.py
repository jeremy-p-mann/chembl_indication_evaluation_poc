from __future__ import annotations

import time
from datetime import datetime
from enum import Enum
from typing import Callable, Dict
import numpy as np
import json

import openai

from chind_eval.prompts import ModelPrompt, get_example_response, get_answer_values


class AcceptedModelID(str, Enum):
    GPT4 = 'gpt-4'
    GPT35TURBO = "gpt-3.5-turbo"
    MOCK = "mock"

    @classmethod
    def from_str(cls, value: str) -> AcceptedModelID:
        return {word.lower(): word for word in cls}[value.lower()]


Model = Callable[[ModelPrompt], Dict]


def get_model_response_schema() -> Dict:
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "response": {
                "type": "string"
            },
            "tokens": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "integer"
                    },
                    "completion": {
                        "type": "integer"
                    },
                    "total": {
                        "type": "integer"
                    }
                },
                "required": ["prompt", "completion", "total"]
            },
            "execution_duration_ms": {
                "type": "number"
            },
            "execution_start_datetime": {
                "type": "string",
                "format": "date-time"
            }
        },
        "required": ["response", "tokens", "execution_duration_ms", "execution_start_datetime"]
    }



def log_normal_random(mode, std_dev) -> float:
    log_std_dev = np.sqrt(np.log(1 + (std_dev / mode)**2))
    log_mean = np.log(mode) - 0.5 * log_std_dev**2
    random_number = np.random.lognormal(log_mean, log_std_dev)
    return random_number


def mock_model(model_prompt: ModelPrompt) -> Dict:
    execution_duration = log_normal_random(2, 0.2) * 1000
    response = json.dumps({
        'answer': np.random.choice(get_answer_values()),
        'reason': np.random.choice([
            'because I am a robot',
            'because I am dumb',
            'idk man i just answer with random answers',
        ]),
    })
    completion_tokens = np.random.randint(30, 80)
    prompt_variation = np.random.randint(0, 8)
    prompt_tokens = 193 + prompt_variation
    ans = {
        'response': response,
        'tokens': {
            "prompt": prompt_tokens,
            "completion": completion_tokens,
            "total": completion_tokens + prompt_tokens,
        },
        'execution_duration_ms': execution_duration,
        'execution_start_datetime': datetime.now().isoformat(),
    }
    return ans


def format_openai_response(resp: Dict) -> Dict:
    return {
        'response': resp['choices'][0]['message']['content'],
        'tokens': {
            "prompt": resp['usage']["prompt_tokens"],
            "completion": resp['usage']["completion_tokens"],
            "total": resp['usage']["total_tokens"]
        }
    }


def get_model(model: str) -> Model:
    model_parsed = AcceptedModelID.from_str(model)
    if model_parsed == AcceptedModelID.MOCK:
        return mock_model

    def model_fn(model_prompt: ModelPrompt) -> Dict:
        execution_datetime = datetime.now().isoformat()
        was_successful = False
        while not was_successful:
            try:
                start_time = time.time()
                time.sleep(2)
                resp = openai.ChatCompletion.create(
                    model=model_parsed.value,
                    temperature=0.5,
                    messages=[
                        {"role": "system", "content": model_prompt.system},
                        {"role": "user", "content": model_prompt.user},
                    ]
                )
                execution_duration = (time.time() - start_time) * 1000
                was_successful = True
            except Exception as e:
                time.sleep(100)
        ans = {
            **format_openai_response(resp),
            'execution_duration_ms': execution_duration,
            'execution_start_datetime': execution_datetime,
        }
        return ans
    return model_fn
