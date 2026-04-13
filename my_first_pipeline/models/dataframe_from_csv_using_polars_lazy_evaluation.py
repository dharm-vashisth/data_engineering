import polars as pl
import os
from constants import (
    root,
    silver_employee_table_command,
    db_directory_path,
)
from logger import get_logging_loader
import duckdb

file_path = os.path.join(root,"data_inputs","raw_data.csv")
log_file_path = os.path.join(root,"logs","lazy_evaluation.log")
db_file_path = os.path.join(db_directory_path,"polars_warehouse.db")
db_log_file_path = os.path.join(root,"logs","polars_warehouse.log")

lazy_logger = get_logging_loader(logger_name="lazy_logger",file_name=log_file_path)
db_logger = get_logging_loader(logger_name="vault_logger", file_name=db_log_file_path)

def load_to_polars_warehouse(db:pl.DataFrame):
    # we have the filered_df ready now open the vault and store it.
    con = duckdb.connect(db_file_path)
    db_logger.info(f"Connection is established with {con}")
    try:
        # creating table in database using schema.
        con.execute(silver_employee_table_command)

        # temporary table using polars dataframe in duckdb connecting using pyarrow.
        con.register("emp_df",filtered_df)
        
        # transaction begines
        con.execute("BEGIN TRANSACTION")
        db_logger.info("Transaction begins")

        # upset approach
        con.execute("""
            delete from silver_employee where id in (select id from emp_df)
        """)

        con.execute("""
            insert into silver_employee select * from emp_df
        """)
        con.execute("COMMIT")

        db_logger.info("Transaction commited. vault updated successfully!")
        records =con.execute("select count(1) from silver_employee").fetchone()[0]
        print(f"Total records: {records}")


    except Exception as e:
        con.execute("ROLLBACK")
        db_logger.error(f"Transactions failed. Hence rolling back.\n {e}")
    finally:
        con.close()


if __name__ == "__main__":
    # lazy evaluation
    data = pl.scan_csv(file_path)

    # plan
    df = (
        data.with_columns(
            pl.col("Salary").cast(pl.Int64,strict=False)
        ).filter(pl.col("Salary")>44)
    )

    # explain the plan
    lazy_logger.info("The lazy execution plan:")
    print(df.explain())

    # execute the plan
    lazy_logger.info("The plan is going to execute...")
    filtered_df = df.collect()
    lazy_logger.info(f"Initial dataframe from scan_csv is of type {type(df)} \n where as after executing the collect(), dataframe returned is of type {type(filtered_df)}.")
    lazy_logger.info("plan is executed successfully!")
    print(filtered_df)
    # update records in duckdb table
    load_to_polars_warehouse(filtered_df)
