from chind_eval.prompts import get_model_prompts_from_chembl


def test_treatments_can_be_parsed_to_model_prompts():
    mp = get_model_prompts_from_chembl('foo', 'bar')
    assert 'foo' in mp.user
    assert 'bar' in mp.user
