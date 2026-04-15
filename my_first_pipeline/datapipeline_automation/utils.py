import logging, os
from constants import (
    root,
    log_directory_name
)

def get_logging_loader(logger_name:str, file_name:str="unknown_handler.log", level:int=logging.INFO, console:bool=False):
    # set up formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

    # attach handlers to formatter
    # file handler
    file_path = os.path.join(root,log_directory_name,file_name)
    file_handler= logging.FileHandler(filename= file_path, mode= 'a')
    file_handler.setFormatter(formatter)

    # get logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(file_handler)
        # console handler
        if (console == True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger
