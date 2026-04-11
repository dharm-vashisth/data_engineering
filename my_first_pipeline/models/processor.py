import polars as pl
import os
from constants import root
from pathlib import Path


class EmployeeProcessor():
    def __init__(self, data_file):
        self.file_path = os.path.join(root,"data_inputs", data_file)
        if not Path(self.file_path).exists():
            raise FileNotFoundError(f"❌ {data_file} doesn't exists at location {self.file_path}")
        
    # plan building
    def _scan_file(self)-> pl.LazyFrame:
        self.lazy_df = pl.scan_csv(self.file_path)

    # cleaning the data
    def _clean_and_filtering(self)-> pl.LazyFrame:
        self.df = (
            self.lazy_df.with_columns(
                [
                    pl.col("Salary").cast(pl.Int64, strict=False),
                    pl.col("department").fill_null("unknown"),
                ]
            ).filter(pl.col("Salary").is_not_null())
        )
    
    # plan explaination
    def explain_plan(self)-> pl.DataFrame:
        return self.df.explain()
    
    # plan execution
    def _execute_plan(self)-> pl.DataFrame:
        return self.df.collect()
    
    def run(self) -> pl.DataFrame:
        try:
            print(f"1. scanning the file {self.file_path}... ✅")
            self._scan_file()
            print("2. cleaning and filtering the data... ✅")
            self._clean_and_filtering()
            print("3. processing the data... ✅")
            return self._execute_plan()
        except Exception as e:
            raise Exception(f"❌ Pipeline broke {e.json()}")

if __name__ == "__main__":
    FILE_NAME = "raw_data.csv"
    emp = EmployeeProcessor(data_file=FILE_NAME)
    
    print("⚙️ Pipeline is going to start....")
    emp_df = emp.run()
    emp_df.show(tbl_hide_column_data_types=True)
    print("⚙️ Pipeline is successfully completed! ✅")
