import os


def get_chembl_db_uri() -> str:
    return os.environ.get('CHEMBL_DB_URI', 'sqlite:///chembl_32.db')
