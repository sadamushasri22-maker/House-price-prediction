from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


if __name__ == "__main__":

    # =========================
    # Data Ingestion
    # =========================
    config = ConfigurationManager()

    data_ingestion_config = config.get_data_ingestion_config()

    data_ingestion = DataIngestion(data_ingestion_config)

    train_path, test_path = data_ingestion.initiate_data_ingestion()

    print("Data Ingestion Completed")


    # =========================
    # Data Validation
    # =========================
    validation_config = config.get_data_validation_config()

    data_validation = DataValidation(validation_config)

    validation_status = data_validation.initiate_data_validation()

    print("Validation Status :", validation_status)


    if validation_status:

        # =========================
        # Data Transformation
        # =========================
        transformation_config = config.get_data_transformation_config()

        data_transformation = DataTransformation(transformation_config)

        train_arr, test_arr, train_target, test_target = (
            data_transformation.initiate_data_transformation(
                train_path,
                test_path
            )
        )

        print("Data Transformation Completed")


        # =========================
        # Model Training
        # =========================
        trainer_config = config.get_model_trainer_config()

        model_trainer = ModelTrainer(trainer_config)

        model_trainer.initiate_model_trainer(
            train_arr,
            test_arr,
            train_target,
            test_target
        )

        print("Model Training Completed")