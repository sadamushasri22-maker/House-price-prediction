import os
import sys
import json
import pickle

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
)

from src.entity.config_entity import ModelEvaluationConfig
from src.exception import CustomException
from src.logger import logging


class ModelEvaluation:

    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def initiate_model_evaluation(
        self,
        model_path,
        test_array,
        test_target,
    ):

        try:

            # Load trained model
            with open(model_path, "rb") as file:
             model = pickle.load(file)

            # Make predictions
            predictions = model.predict(test_array)

            r2 = r2_score(test_target, predictions)

            mae = mean_absolute_error(
              test_target,
              predictions,
            )

            mse = mean_squared_error(
            test_target,
            predictions,
              )

            rmse = mse ** 0.5

            metrics = {
                "R2 Score": float(r2),
                "MAE": float(mae),
                "RMSE": float(rmse),
            }

            # Create directory
            os.makedirs(self.config.root_dir, exist_ok=True)

            # Save metrics
            with open(self.config.metric_file_name, "w") as file:
                json.dump(metrics, file, indent=4)

            print("\nModel Evaluation Completed")
            print(metrics)

            logging.info("Model evaluation completed successfully.")

        except Exception as e:
            raise CustomException(e, sys)