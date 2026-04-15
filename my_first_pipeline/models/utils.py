import logging, os, duckdb
import polars as pl
from constants import (
    root,
    log_directory_name,
    silver_employee_table_command
)


def load_data_using_dataframe_to_warehouse(
        db:pl.DataFrame,
        db_logger, 
        db_file_path, 
        table_name="emp_df",
        create_table_command = silver_employee_table_command
    ):
    # we have the filered_df ready now open the vault and store it.
    con = duckdb.connect(db_file_path)
    db_logger.info(f"Connection is established with {con}")
    try:
        # creating table in database using schema.
        con.execute(create_table_command)

        # temporary table using polars dataframe in duckdb connecting using pyarrow.
        con.register(table_name,db)
        
        # transaction begines
        con.execute("BEGIN TRANSACTION")
        db_logger.info("Transaction begins")

        # upset approach
        con.execute(f"delete from silver_employee where id in (select id from {table_name})")

        con.execute(f"insert into silver_employee select * from {table_name}")
        con.execute("COMMIT")

        db_logger.info("Transaction commited. vault updated successfully!")
        records =con.execute("select count(1) from silver_employee").fetchone()[0]
        print(f"Total records: {records}")


    except Exception as e:
        con.execute("ROLLBACK")
        db_logger.error(f"Transactions failed. Hence rolling back.\n {e}")
    finally:
        con.close()


def get_logging_loader(logger_name:str, file_name:str="unknown_handler.log", level:int=logging.INFO, console:bool=False):
    # set up formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

    # attach handlers to formatter
    # file handler
    file_path = os.path.join(root,log_directory_name,file_name)
    file_handler= logging.FileHandler(filename= file_path, mode='a')
    file_handler.setFormatter(formatter)

    # get logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(file_handler)
        # console handler
        if (console == True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger
