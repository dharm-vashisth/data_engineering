import duckdb
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]

DB_PATH = os.path.join(root,"data","data.duckdb")

def get_connection():
    return duckdb.connect(DB_PATH)

def init_db():
    conn = get_connection()

    # Create sequence
    conn.execute("""
    CREATE SEQUENCE IF NOT EXISTS expense_id_seq START 1;
    """)

    # Create table using sequence
    conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER DEFAULT nextval('expense_id_seq') PRIMARY KEY,
        amount DOUBLE,
        category VARCHAR,
        note VARCHAR
    )
    """)

    conn.close()
