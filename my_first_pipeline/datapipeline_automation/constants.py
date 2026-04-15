from pathlib import Path
import os

root = Path(__file__).resolve().parents[2]

# log file variables
log_directory_name = 'logs/datapipeline'
log_directory_path = os.path.join(root,log_directory_name)
logger_name="datapipeline_logger"

# duckdb database variables
db_directory_name = "database/datapipeline"
db_directory_path = os.path.join(root,db_directory_name)


# sql commmands
silver_employee_table_command = """
create table if not exists silver_employee(
ID INTEGER PRIMARY KEY,
Name varchar(30),
Age INTEGER,
Salary DECIMAL(4),
Code varchar,
department varchar
)
"""
