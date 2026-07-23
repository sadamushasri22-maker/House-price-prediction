import os
from pathlib import Path

from src.utils.common import read_yaml
from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
)

from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig
)

class ConfigurationManager:

    def __init__(
        self,
        config_filepath=Path("config/config.yaml"),
    ):
        self.config = read_yaml(config_filepath)

    def get_data_ingestion_config(self):

        config = self.config["data_ingestion"]

        return DataIngestionConfig(
            root_dir=config["root_dir"],
            input_data_path=config["input_data_path"],
            raw_data_path=config["raw_data_path"],
            train_data_path=config["train_data_path"],
            test_data_path=config["test_data_path"],
        )

    def get_data_validation_config(self):

        config = self.config["data_validation"]

        return DataValidationConfig(
            root_dir=config["root_dir"],
            STATUS_FILE=config["STATUS_FILE"],
            unzip_data_dir=config["unzip_data_dir"],
            all_schema=config["all_schema"],
        )

    def get_data_transformation_config(self):

        config = self.config["data_transformation"]

        return DataTransformationConfig(
            root_dir=config["root_dir"],
            preprocessor_obj_file_path=config["preprocessor_obj_file_path"],
        )

    def get_model_trainer_config(self):

        config = self.config["model_trainer"]

        os.makedirs(config["root_dir"], exist_ok=True)

        model_trainer_config = ModelTrainerConfig(
        root_dir=config["root_dir"],
        trained_model_file_path=config["trained_model_file_path"]
    )

        return model_trainer_config
    
    def get_model_evaluation_config(self):

     config = self.config["model_evaluation"]

     os.makedirs(config["root_dir"], exist_ok=True)

     model_evaluation_config = ModelEvaluationConfig(
        root_dir=config["root_dir"],
        metric_file_name=config["metric_file_name"]
    )

     return model_evaluation_config