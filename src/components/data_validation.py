import os
import sys
import pandas as pd

from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import DataValidationConfig
from src.utils.common import read_yaml


class DataValidation:

    def __init__(self, config: DataValidationConfig):
        self.config = config

    def initiate_data_validation(self) -> bool:
        """
        Validates whether all dataset columns match the schema.
        """

        try:
            validation_status = True

            # Read dataset
            data = pd.read_csv(self.config.unzip_data_dir)

            # Read schema
            schema = read_yaml(self.config.all_schema)

            all_cols = list(schema["COLUMNS"].keys())

            logging.info("Schema loaded successfully.")

            print("Columns in Schema:")
            print(all_cols)

            print("\nColumns in Dataset:")
            print(list(data.columns))

            # Check every column
            for col in data.columns:
                if col not in all_cols:
                    print(f"Column not found in schema: {col}")
                    validation_status = False

            # Also check if any schema column is missing
            for col in all_cols:
                if col not in data.columns:
                    print(f"Column missing in dataset: {col}")
                    validation_status = False

            # Create validation folder
            os.makedirs(self.config.root_dir, exist_ok=True)

            # Save validation status
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}")

            logging.info(f"Validation Status: {validation_status}")

            return validation_status

        except Exception as e:
            raise CustomException(e, sys)