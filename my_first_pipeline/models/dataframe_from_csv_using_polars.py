import polars as pl
from constants import root
import os
from logger import get_logging_loader

bad_data_logger = get_logging_loader(logger_name="bad_data_logger",file_name="bad_data_logger.log")

if __name__=="__main__":
    file_path = os.path.join(root,"data_inputs","raw_data.csv")
    df = pl.read_csv(file_path, has_header=True)
    print("Original Dataframe:")
    df.show()
    # type casting
    df = df.with_columns(
        pl.col("Salary").cast(pl.Int64)
    )
    
    # total records.
    total_records_salaries = df.select(pl.col("Salary").len()).item()
    # null salary records.
    null_salaries_df = df.select(pl.col("Salary").null_count()).item()
    null_salary_percent = (null_salaries_df/total_records_salaries)*100

    if null_salary_percent > 10:
        bad_data_logger.info(f"Null Salary records are greater than 10% {null_salary_percent}")
    
    filtered_df = df.filter(pl.col("Salary").is_not_null())
    print("Filtered Dataframe with non-null salaries:")
    filtered_df.show()
    
