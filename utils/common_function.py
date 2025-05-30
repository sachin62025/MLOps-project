import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'YAML file not found at {file_path}')
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f'Successfully read YAML file from {file_path}')
            return config
    
    except Exception as e:
        logger.error("Error while reading the yaml file ")
        raise CustomException('Failed to read yaml file ', e)
    
def load_data(path):
    try:
        logger.info(f'Loading data from {path}')
        return pd.read_csv(path)
    except FileNotFoundError as e:
        logger.error(f'File not found at {path}')
        raise CustomException(f'File not found at {path}', e)


