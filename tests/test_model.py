import pytest
from datetime import datetime

from jsonschema import validate

from chind_eval.model import (ModelPrompt, format_openai_response, get_model,
                              get_model_response_schema)


@pytest.mark.skip(reason="It's expensive")
def test_model_can_echo_hello_world():
    input = 'Hello world.'
    model = get_model('gpt-3.5-turbo')
    system_prompt = 'Repeat exactly what the user says'
    ans = model(ModelPrompt(system_prompt, input))
    assert ans['response'] == input


def test_can_format_openai_model():
    resp = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "\n\nHello there, how may I assist you today?",
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }
    formatted = {
        **format_openai_response(resp),
        'execution_duration_ms': 1023.3,
        'execution_start_datetime': datetime.now().isoformat(),
    }
    validate(formatted, get_model_response_schema())


def test_mock_fits_schema():
    input = 'Hello world.'
    system_prompt = 'Repeat exactly what the user says'
    model = get_model('mock')
    ans = model(ModelPrompt(system_prompt, input))
    validate(ans, get_model_response_schema())
