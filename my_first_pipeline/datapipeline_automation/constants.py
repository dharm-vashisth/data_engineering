from pathlib import Path
import os

root = Path(__file__).resolve().parents[2]

# log file variables
log_directory_name = 'logs/datapipeline'
log_directory_path = os.path.join(root,log_directory_name)
logger_name="datapipeline_logger"

# data source variables
data_directory_name = "data_inputs"
data_directory_path = os.path.join(root,data_directory_name)
