import sys

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

from src.entity.config_entity import ModelTrainerConfig
from src.exception import CustomException
from src.logger import logging
from src.utils.common import save_object


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

            models = {
                "Linear Regression": LinearRegression(),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Random Forest": RandomForestRegressor(random_state=42),
            }

            best_model = None
            best_score = -1

            for model_name, model in models.items():

                logging.info(f"Training {model_name}")

                model.fit(train_array, train_target)

                predictions = model.predict(test_array)

                score = r2_score(test_target, predictions)

                print(f"{model_name} R2 Score : {score:.4f}")

                if score > best_score:
                    best_score = score
                    best_model = model

            save_object(
                file_path=self.config.trained_model_file_path,
                obj=best_model,
            )

            print("\nBest Model Saved Successfully")
            print(f"Best R2 Score : {best_score:.4f}")

        except Exception as e:
            raise CustomException(e, sys)