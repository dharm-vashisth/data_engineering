from pathlib import Path

root = Path(__file__).resolve().parents[2]
log_directory_name = 'logs'
validation_logger="validation_logger"
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
