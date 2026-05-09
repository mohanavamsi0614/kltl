from typing import List
from sqlalchemy import create_engine, inspect
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def get_table_columns(schema: str, table: str) -> List[str]:
    """
    Fetches column names for a given table using SQLAlchemy inspection.
    """
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns(table, schema=schema)
        return [col['name'] for col in columns]
    except Exception as e:
        print(f"Error fetching columns for {schema}.{table}: {e}")
        return []
