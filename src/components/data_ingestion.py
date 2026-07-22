import os
import sys
import pandas as pd
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    input_data_path: str = "data/raw/data.csv"
    train_data_path="artifacts/train.csv"
    test_data_path="artifacts/test.csv"
    raw_data_path="artifacts/data.csv"

from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the Data Ingestion method")

        try:
            
            df = pd.read_csv(self.ingestion_config.input_data_path)
            logging.info("Dataset loaded successfully")
 
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
 
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Raw data saved successfully")
 
            logging.info("Performing train-test split")

            train_set, test_set = train_test_split(
                df,
                test_size=0.2,
                random_state=42
            )

           
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)

            logging.info("Train-test split completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)