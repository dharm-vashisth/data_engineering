import polars as pl
import os
from constants import root
from logger import get_logging_loader

file_path = os.path.join(root,"data_inputs","raw_data.csv")
log_file_path = os.path.join(root,"logs","lazy_evaluation.log")
lazy_logger = get_logging_loader(logger_name="lazy_logger",file_name=log_file_path)

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
    print("The lazy execution plan:")
    print(df.explain())

    # execute the plan
    print("The plan is going to execute...")
    filtered_df = df.collect()
    print(f"Initial dataframe from scan_csv is of type {type(df)} \n where as after executing the collect(), dataframe returned is of type {type(filtered_df)}.")

    print("plan is executed successfully!")
    print(filtered_df)
