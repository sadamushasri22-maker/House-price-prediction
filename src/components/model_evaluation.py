import os
import sys
import json
import pickle
import numpy as np

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

            # Predictions (model outputs log scale)
            predictions_log = model.predict(test_array)
            predictions = np.expm1(predictions_log)

            r2 = r2_score(test_target, predictions)
            mae = mean_absolute_error(test_target, predictions)
            mse = mean_squared_error(test_target, predictions)
            rmse = float(mse ** 0.5)

            r2_log = r2_score(np.log1p(test_target), predictions_log)

            metrics = {
                "R2 Score": float(r2),
                "Log R2 Score": float(r2_log),
                "MAE": float(mae),
                "RMSE": float(rmse),
            }

            # Create directory
            os.makedirs(self.config.root_dir, exist_ok=True)

            # Save metrics
            with open(self.config.metric_file_name, "w") as file:
                json.dump(metrics, file, indent=4)

            print("\nModel Evaluation Completed")
            print(json.dumps(metrics, indent=4))

            logging.info("Model evaluation completed successfully.")
            return metrics

        except Exception as e:
            raise CustomException(e, sys)