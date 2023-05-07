from chind_eval.chembl_treatments import get_chembl_treatments_df


def test_get_chembl_treatments_returns_dataframe_with_correct_columns():
    expected_columns = ['intervention_name', 'condition_name', 'drugind_id', 'max_phase_for_ind',]
    treatment_df = get_chembl_treatments_df(3)
    for column in expected_columns:
        assert column in treatment_df.columns
