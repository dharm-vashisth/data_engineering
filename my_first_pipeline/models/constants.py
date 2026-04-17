from pathlib import Path
import os

root = Path(__file__).resolve().parents[2] # fake commit.
log_directory_name = 'logs'
db_directory_path = os.path.join(root,"database")
validation_logger="validation_logger"
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
