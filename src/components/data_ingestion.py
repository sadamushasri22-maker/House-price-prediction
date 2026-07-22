import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig


class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self):
        logging.info("Data ingestion started")

        try:
            df = pd.read_csv(self.config.input_data_path)

            os.makedirs(self.config.root_dir, exist_ok=True)

            df.to_csv(self.config.raw_data_path, index=False)

            train_set, test_set = train_test_split(
                df,
                test_size=0.2,
                random_state=42,
            )

            train_set.to_csv(self.config.train_data_path, index=False)
            test_set.to_csv(self.config.test_data_path, index=False)

            logging.info("Train and Test data saved successfully")

            return (
                self.config.train_data_path,
                self.config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)