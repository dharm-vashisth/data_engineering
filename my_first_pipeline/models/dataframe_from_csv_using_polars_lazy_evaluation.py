import polars as pl
import os
from constants import (
    root,
    db_directory_path,
)
from utils import (get_logging_loader, load_data_using_dataframe_to_warehouse)
import duckdb

file_path = os.path.join(root,"data_inputs","raw_data.csv")
log_file_path = os.path.join(root,"logs","lazy_evaluation.log")
db_file_path = os.path.join(db_directory_path,"polars_warehouse.db")
db_log_file_path = os.path.join(root,"logs","polars_warehouse.log")

lazy_logger = get_logging_loader(logger_name="lazy_logger",file_name=log_file_path)
db_logger = get_logging_loader(logger_name="vault_logger", file_name=db_log_file_path)


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
    load_data_using_dataframe_to_warehouse(filtered_df, db_logger, db_file_path)
