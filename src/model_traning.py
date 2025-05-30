import os
import pandas as pd
import joblib
import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error,accuracy_score, precision_score,recall_score,f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.model_params import *
from config.path_config import *
from utils.common_function import read_yaml, load_data
from scipy.stats import randint, uniform

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)


class ModelTraining:
    def __init__(self,train_path, test_path , modlel_output_path ):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = modlel_output_path

        self.params_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f'Loading training data from {self.train_path}')
            train_df = load_data(self.train_path)
            logger.info(f'Loading test data from {self.test_path}')
            test_df = load_data(self.test_path) 
            logger.info('Data loaded successfully')

            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']

            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']
            logger.info('Data split into features and target variable')
            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f'Error in loading and splitting data: {e}')
            raise CustomException(f'Error in loading and splitting data: {e}')
    
    def train_lgbm(self, X_train,y_train):
        try:
            logger.info('Initializing LightGBM model')
            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params['random_state'])
            
            logger.info('Starting Randomized Search for hyperparameter tuning')
            random_search = RandomizedSearchCV(
                estimator= lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],

                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
            )

            logger.info('Start our hyperparameter tuning')
            random_search.fit(X_train, y_train)
            logger.info('Hyperparameters completed')

            best_params = random_search.best_params_
            logger.info(f'Best hyperparameters found: {best_params}')
            best_lgbm_model = random_search.best_estimator_
            logger.info('Training LightGBM model with best hyperparameters')
            return best_lgbm_model
        except Exception as e:
            logger.error(f'Error in training LightGBM model: {e}')
            raise CustomException(f'Error in training LightGBM model: {e}')
    
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info('Evaluating the model')
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            logger.info(f'Model evaluation completed with accuracy: {accuracy}, precision: {precision}, recall: {recall}, f1-score: {f1}')
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1
            }
        except Exception as e: 
            logger.error(f'Error in evaluating model: {e}')
            raise CustomException(f'Error in evaluating model: {e}')
    
    def save_model(self, model):
        try:
            logger.info(f'Saving the model to {self.model_output_path}')
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            joblib.dump(model, self.model_output_path)
            logger.info('Model saved successfully')
        except Exception as e:  
            logger.error(f'Error in saving model: {e}')
            raise CustomException(f'Error in saving model: {e}')    
    def run(self):
        try:
            with mlflow.start_run():
                logger.info('Starting model training pipeline')
                logger.info('starting our MLFLOW experiment')
                
                logger.info('Logginf the training and testing parameter to MLFLOW')
                mlflow.log_artifact(self.train_path, artifact_path='datasets')
                mlflow.log_artifact(self.test_path, artifact_path='datasets')
                
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                evaluation_metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)

                logger.info('Logging model to MLflow')
                mlflow.log_artifact(self.model_output_path)

                logger.info('Logging params and metrics to MLFLOW')
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(evaluation_metrics)

                logger.info(f'Model training process completed with evaluation metrics: {evaluation_metrics}')
                
        except Exception as e:
            logger.error(f'Error in model training process: {e}')
            raise CustomException(f'Error in model training process: {e}') 



if __name__ == "__main__":
    trainer = ModelTraining(
        train_path=PROCESSD_TRAIN_FILE_PATH,
        test_path=PROCESSD_TEST_FILE_PATH,
        modlel_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()
    logger.info('Model training script executed successfully')


