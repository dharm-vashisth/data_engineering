import logging
import os

# set up for logging.
log_file_name = os.path.join("..","logs","pipeline.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    filename=log_file_name,
    filemode='a'
)

# Data Loader object
class LocalDataLoader:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        logging.info(f"DataLoader initialized for folder: {self.folder_path} - {log_file_name}")
    
    def fetch_files(self, file_name: str):
        full_path = os.path.join("..",self.folder_path, file_name)
        logging.info(f"Attempting to fetch: {file_name} - {full_path}")

        if not os.path.exists(full_path):
            logging.error(f"File Not Found: {full_path}")
            return None
        try:
            with open(full_path,'r') as file:
                data = file.read()
                logging.info(f"Successfully loaded {len(data)} characters from the {full_path} file. ")

        except Exception as e:
            logging.error(f"System error while reading the file {full_path}: {e}")


        
# Execution block
if __name__ == "__main__":
    # creating the object
    loader = LocalDataLoader(folder_path="data_inputs")

    # fetching the file content
    loader.fetch_files("raw_data.csv")

        