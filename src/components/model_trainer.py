import sys
import numpy as np
from sklearn.metrics import r2_score

from src.entity.config_entity import ModelTrainerConfig
from src.exception import CustomException
from src.logger import logging
from src.utils.common import save_object

from src.models.model_factory import get_models, get_xgboost
from src.models.hyperparameters import xgb_params
from src.models.model_tuner import tune_model


class ModelTrainer:

    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def initiate_model_trainer(
        self,
        train_array,
        test_array,
        train_target,
        test_target,
    ):
        try:
            # Transform target variable to log scale
            train_target_log = np.log1p(train_target)
            test_target_log = np.log1p(test_target)

            # Get baseline models
            models = get_models()

            best_model = None
            best_model_name = ""
            best_score = float("-inf")

            print("\n========== Baseline Model Comparison ==========\n")

            for model_name, model in models.items():
                logging.info(f"Training {model_name}")

                model.fit(train_array, train_target_log)

                predictions_log = model.predict(test_array)
                predictions = np.expm1(predictions_log)

                score = r2_score(test_target, predictions)
                score_log = r2_score(test_target_log, predictions_log)

                print(f"{model_name:<20} R2 Score (Dollar): {score:.4f} | R2 Score (Log): {score_log:.4f}")

                if score > best_score:
                    best_score = score
                    best_model = model
                    best_model_name = model_name

            print("\n==============================================")
            print(f"Best Baseline Model : {best_model_name} (R2 Score: {best_score:.4f})")
            print("==============================================")

            # Hyperparameter Tuning (XGBoost)
            print("\nStarting XGBoost Hyperparameter Tuning...\n")

            tuned_model = tune_model(
                model=get_xgboost(),
                params=xgb_params,
                X_train=train_array,
                y_train=train_target_log,
            )

            tuned_predictions_log = tuned_model.predict(test_array)
            tuned_predictions = np.expm1(tuned_predictions_log)

            tuned_score = r2_score(test_target, tuned_predictions)
            print(f"\nTuned XGBoost R2 Score : {tuned_score:.4f}")

            if tuned_score > best_score:
                print("\n[SUCCESS] Tuned XGBoost performed better.")
                best_model = tuned_model
                best_score = tuned_score
                best_model_name = "Tuned XGBoost"
            else:
                print(f"\n[INFO] Baseline {best_model_name} is still better.")

            save_object(
                file_path=self.config.trained_model_file_path,
                obj=best_model,
            )

            print("\n==============================================")
            print(f"Best Model ({best_model_name}) Saved Successfully")
            print(f"Final Best R2 Score : {best_score:.4f}")
            print("==============================================")

            return best_score

        except Exception as e:
            raise CustomException(e, sys)