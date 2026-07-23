import sys

from sklearn.metrics import r2_score

from src.entity.config_entity import ModelTrainerConfig
from src.exception import CustomException
from src.logger import logging
from src.utils.common import save_object

from src.models.model_factory import (
    get_models,
    get_xgboost,
)
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

            # Get all baseline models
            models = get_models()

            best_model = None
            best_score = float("-inf")

            print("\n========== Baseline Model Comparison ==========\n")

            for model_name, model in models.items():

                logging.info(f"Training {model_name}")

                model.fit(train_array, train_target)

                predictions = model.predict(test_array)

                score = r2_score(test_target, predictions)

                print(f"{model_name} R2 Score : {score:.4f}")

                if score > best_score:
                    best_score = score
                    best_model = model

            print("\n==============================================")
            print(f"Best Baseline Score : {best_score:.4f}")
            print("==============================================")

            # -------------------------------
            # Hyperparameter Tuning (XGBoost)
            # -------------------------------

            print("\nStarting XGBoost Hyperparameter Tuning...\n")

            tuned_model = tune_model(
                model=get_xgboost(),
                params=xgb_params,
                X_train=train_array,
                y_train=train_target,
            )

            tuned_predictions = tuned_model.predict(test_array)

            tuned_score = r2_score(
                test_target,
                tuned_predictions,
            )

            print(f"\nTuned XGBoost R2 Score : {tuned_score:.4f}")

            if tuned_score > best_score:

                print("\n✅ Tuned XGBoost performed better.")

                best_model = tuned_model
                best_score = tuned_score

            else:

                print("\nℹ️ Baseline model is still better.")

            save_object(
                file_path=self.config.trained_model_file_path,
                obj=best_model,
            )

            print("\n==============================================")
            print("Best Model Saved Successfully")
            print(f"Final Best R2 Score : {best_score:.4f}")
            print("==============================================")

        except Exception as e:
            raise CustomException(e, sys)