from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def explode_dict_into_record(dct, parent_key=""):
    items = []
    for k, v in dct.items():
        new_key = f"{parent_key}_{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(explode_dict_into_record(v, parent_key=new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_engine(db_uri: str) -> Engine:
    return create_engine(db_uri)
