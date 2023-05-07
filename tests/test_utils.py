import pytest

from chind_eval.utils import explode_dict_into_record


@pytest.fixture(params=[
    ({'foo': 'bar', 'baz': {'bag': 0, 'bob': 'yes'}},
     {'foo': 'bar', 'baz_bag': 0, 'baz_bob': 'yes'}),
    ({'a': {'b': {'c': 1}}, 'd': 2}, {'a_b_c': 1, 'd': 2}),
    ({'foo': {'bar': {'baz': 'qux'}}}, {'foo_bar_baz': 'qux'}),
    ({}, {}),
])
def input_and_expected_output(request):
    return request.param


def test_explode_dict_into_record(input_and_expected_output):
    input, expected_output = input_and_expected_output
    output = explode_dict_into_record(input)
    assert output == expected_output
