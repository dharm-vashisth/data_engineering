import duckdb
from logger import get_logging_loader
from constants import root
import os

log_file_path = os.path.join(root,"logs","warehouse.log")
db_file_path = os.path.join(root,"database","warehouse.db")

table_command = """
create table if not exists silver_employee(
ID INTEGER PRIMARY KEY,
Name varchar(30),
Age INTEGER,
Salary DECIMAL(4),
Code varchar,
department varchar
)
"""


logger = get_logging_loader(logger_name="vault_logger", file_name=log_file_path)
db_file_path = os.path.join(root,"database","warehouse.db")

if __name__ == "__main__":
    # connection establishment.
    db = duckdb.connect(db_file_path)
    logger.info("Duckdb connection has been established")

    db.execute(table_command)
    tables = db.execute("SHOW tables").fetchall()
    print(tables)

    db.close()
