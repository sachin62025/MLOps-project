from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_traning import ModelTraining
from config.path_config import *
from utils.common_function import read_yaml , load_data


if __name__ == "__main__":
    # 1. data ingestion
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    # 2 data processing
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSD_DIR,CONFIG_PATH)
    processor.process() 

    # 3. model training

    trainer = ModelTraining(
        train_path=PROCESSD_TRAIN_FILE_PATH,
        test_path=PROCESSD_TEST_FILE_PATH,
        modlel_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()

