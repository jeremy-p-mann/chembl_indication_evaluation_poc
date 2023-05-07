import pandas as pd
from sqlalchemy import create_engine, text

from chind_eval.config import get_chembl_db_uri

'''
CREATE TABLE drug_indication (
        drugind_id BIGINT NOT NULL,
        record_id BIGINT NOT NULL,
        molregno BIGINT,
        max_phase_for_ind NUMERIC(2, 1),
        mesh_id VARCHAR(20) NOT NULL,
        mesh_heading VARCHAR(200) NOT NULL,
        efo_id VARCHAR(20),
        efo_term VARCHAR(200),
        CONSTRAINT drugind_pk PRIMARY KEY (drugind_id),
        CONSTRAINT drugind_molregno_fk FOREIGN KEY(molregno) REFERENCES molecule_dictionary (molregno) ON DELETE CASCADE,
        CONSTRAINT drugind_rec_fk FOREIGN KEY(record_id) REFERENCES compound_records (record_id) ON DELETE CASCADE,
        CONSTRAINT drugind_uk UNIQUE (record_id, mesh_id, efo_id)
);
CREATE UNIQUE INDEX drug_indication_pk ON drug_indication (drugind_id);
'''


def get_chembl_treatments_df(N: int) -> pd.DataFrame:
    engine = create_engine(get_chembl_db_uri())
    query = text('''
    select
        COMPOUND_NAME as intervention_name
        , mesh_heading as condition_name
        , max_phase_for_ind
        , drugind_id
    from drug_indication
    inner join compound_records
        on compound_records.record_id = drug_indication.record_id
    where drugind_id IN (
        select drugind_id
        from drug_indication
        order by RANDOM()
        limit :N
    )
    ;
    '''
                 )
    return pd.read_sql(query, engine, params={"N": N})
