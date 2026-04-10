import polars as pl
from constants import root
import os

if __name__=="__main__":
    file_path = os.path.join(root,"data_inputs","raw_data.csv")
    df = pl.read_csv(file_path, has_header=False)
    print("Original Dataframe:")
    df.show()
    null_df = df.filter(pl.col("column_3").is_not_null())
    filtered_df = df.filter(pl.col("column_3").is_not_null())
    print("Filtered Dataframe:")
    filtered_df.show()
    
