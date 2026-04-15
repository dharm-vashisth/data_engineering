import logging, os
from constants import (
    root,
    log_directory_name,
)
import duckdb
import polars as pl

def get_logging_loader(logger_name:str, file_name:str="unknown_handler.log", level:int=logging.INFO, console:bool=False):
    # set up formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

    # attach handlers to formatter
    # file handler
    file_path = os.path.join(root,log_directory_name,file_name)
    file_handler= logging.FileHandler(filename= file_path, mode= 'a')
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


# not a data contract but may face the schema drift.
def load_data_to_warehouse(
        db_logger, 
        data_path,
        db_path, 
        silver_table_name="silver_employee",
    ):
    # sql commmand
    create_table_command = f"""
create table if not exists {silver_table_name} as select * from tmp
"""
    # we have the filered_df ready now open the vault and store it.
    df = pl.read_csv(data_path, has_header=True)

    con = duckdb.connect(db_path)
    db_logger.info(f"Connection is established with {con}")
    try:
        # creating table in database using schema.
        con.register("tmp", df)
        con.execute(create_table_command)
        
        # transaction begines
        con.execute("BEGIN TRANSACTION")
        db_logger.info("Transaction begins")

        # upset approach
        con.execute(f"delete from {silver_table_name} where id in (select id from tmp)")

        con.execute(f"insert into {silver_table_name} select * from tmp")
        con.execute("COMMIT")

        db_logger.info("Transaction commited. vault updated successfully!")
        records =con.execute(f"select count(1) from {silver_table_name}").fetchone()[0]
        print(f"Total records: {records}")


    except Exception as e:
        con.execute("ROLLBACK")
        db_logger.error(f"Transactions failed. Hence rolling back.\n {e}")
    finally:
        con.close()
