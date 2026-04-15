from pathlib import Path
import os

root = Path(__file__).resolve().parents[2]
logger_name="datapipeline_logger"


# name variables
log_directory_name = 'logs/datapipeline'
db_directory_name = "database/datapipeline/pipeline.db"
data_directory_name = "data_inputs"

# path variables
log_directory_path = os.path.join(root,log_directory_name)
data_directory_path = os.path.join(root,data_directory_name)
db_directory_path = os.path.join(root,db_directory_name)
