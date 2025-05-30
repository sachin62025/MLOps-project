import os

########## DATA PATHS INGESTION ##########
RAW_DIR = 'artifacts/raw'
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = 'config/config.yaml' 


########### DATA PROCESSING ##########
PROCESSD_DIR = 'artifacts/processed'
PROCESSD_TRAIN_FILE_PATH = os.path.join(PROCESSD_DIR, "processed_train.csv")
PROCESSD_TEST_FILE_PATH = os.path.join(PROCESSD_DIR, "processed_test.csv")

###################### Model Training ######################
MODEL_OUTPUT_PATH = 'artifacts/model/lgbm_model.pkl'

