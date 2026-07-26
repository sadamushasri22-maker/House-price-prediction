import sys
from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.exception import CustomException
from src.logger import logging


class TrainPipeline:

    def __init__(self):
        self.config_manager = ConfigurationManager()

    def run_pipeline(self):
        try:
            logging.info("Starting Training Pipeline...")

            # 1. Data Ingestion
            data_ingestion_config = self.config_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            train_path, test_path = data_ingestion.initiate_data_ingestion()
            print("[OK] Data Ingestion Completed")

            # 2. Data Validation
            validation_config = self.config_manager.get_data_validation_config()
            data_validation = DataValidation(validation_config)
            validation_status = data_validation.initiate_data_validation()
            print("[OK] Validation Status:", validation_status)

            if not validation_status:
                raise Exception("Data validation failed. Check schema compatibility.")

            # 3. Data Transformation
            transformation_config = self.config_manager.get_data_transformation_config()
            data_transformation = DataTransformation(transformation_config)
            train_arr, test_arr, train_target, test_target = (
                data_transformation.initiate_data_transformation(
                    train_path, test_path
                )
            )
            print("[OK] Data Transformation Completed")

            # 4. Model Training
            trainer_config = self.config_manager.get_model_trainer_config()
            model_trainer = ModelTrainer(trainer_config)
            best_score = model_trainer.initiate_model_trainer(
                train_arr, test_arr, train_target, test_target
            )
            print(f"[OK] Model Training Completed (R2: {best_score:.4f})")

            # 5. Model Evaluation
            evaluation_config = self.config_manager.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(evaluation_config)
            metrics = model_evaluation.initiate_model_evaluation(
                trainer_config.trained_model_file_path, test_arr, test_target
            )
            print("[OK] Model Evaluation Completed")
            return metrics

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
