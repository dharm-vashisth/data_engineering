from utils import get_logging_loader
from polars.interchange.dataframe import PolarsDataFrame
import polars as pl

logger = get_logging_loader(logger_name="data_processing", file_name="data_processor.log")

class DataProcessing:
    ddf: PolarsDataFrame=None

    def __init__(self):
        self.ddf = pl.DataFrame(self._get_raw_data())

    def _get_raw_data(self):
        # hardcoded raw data for now.
        return {
            "id": [1,2,3,4],
            "name": ["ab","bc","cd","de"],
            "dept": ["AC","AC","RF","RF"],
            "age": [25,24,27,-32],
            "salary": [14000,9000,16000,27000]
        }

    def get_dataframe(self) -> PolarsDataFrame:
        return self.ddf
    

if __name__ == "__main__":
    logger.info("Data processing has started.")
    data = DataProcessing()
    df = data.get_dataframe()
    
    logger.info("Dataframe is created.")
    print("Original Dataframe")
    df.show()

    # aggregation dataframe
    agg_df = df.group_by(pl.col("dept"))\
                .agg(
                    pl.col("salary").mean().alias("Average Salary"),
                    pl.col("salary").max().alias("Max Salary")
                )
    logger.info("Aggregated Dataframe is successful.")
    print("Aggregated Dataframe")    
    agg_df.show()
    
