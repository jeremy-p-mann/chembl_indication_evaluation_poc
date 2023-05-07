import pytest

from chind_eval import get_analysis, get_evaluation_results


@pytest.fixture(scope='module')
def analysis_results():
    return get_analysis(get_evaluation_results(100, 'mock'), 'mock')
