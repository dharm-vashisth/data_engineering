import duckdb
from utils import get_logging_loader
from constants import (root, silver_employee_table_command, db_directory_path)
import os


log_file_path = os.path.join(root,"logs","warehouse.log")
db_file_path = os.path.join(db_directory_path,"warehouse.db")
logger = get_logging_loader(logger_name="vault_logger", file_name=log_file_path)

if __name__ == "__main__":
    # connection establishment.
    db = duckdb.connect(db_file_path)
    logger.info("Duckdb connection has been established")

    db.execute(silver_employee_table_command)
    tables = db.execute("SHOW tables").fetchall()
    print(tables)

    db.close()
