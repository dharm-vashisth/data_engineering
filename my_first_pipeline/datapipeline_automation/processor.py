import os
from utils import get_logging_loader
from constants import (
    logger_name,
    log_directory_path

)

# log setup
processor_log_file = os.path.join(log_directory_path,"pipeline.log")
processor_log = get_logging_loader(logger_name=logger_name, file_name=processor_log_file)

if __name__ == "__main__":
    processor_log.log("Pipeline started...")
    