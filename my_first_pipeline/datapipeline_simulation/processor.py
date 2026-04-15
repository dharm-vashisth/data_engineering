import os
import argparse
from utils import get_logging_loader, load_data_to_warehouse
from constants import (
    logger_name,
    log_directory_path,
    data_directory_path,
    db_directory_path,
)

# log setup
processor_log_file = os.path.join(log_directory_path,"pipeline.log")
processor_log = get_logging_loader(logger_name=logger_name, file_name=processor_log_file)

if __name__ == "__main__":
    # setting up the command line arguments
    arg_parser = argparse.ArgumentParser(description="Argument Parser v1")
    arg_parser.add_argument("--file", type=str, required=True, help="Path to the souce file.")
    args = arg_parser.parse_args()

    processor_log.info("Pipeline started...")
    print(args.file)
    file_name = args.file
    data_source_file_path = os.path.join(data_directory_path,file_name)
    load_data_to_warehouse(db_logger=processor_log, data_path=data_source_file_path, db_path=db_directory_path)
    processor_log.info("Pipeline completed.")
