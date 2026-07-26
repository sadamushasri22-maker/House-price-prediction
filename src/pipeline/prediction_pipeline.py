import sys
import os
import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils.common import load_object
from src.components.data_transformation import add_engineered_features


class PredictPipeline:

    def __init__(self):
        self.preprocessor_path = os.path.join(
            "artifacts", "data_transformation", "preprocessor.pkl"
        )
        self.model_path = os.path.join(
            "artifacts", "model_trainer", "model.pkl"
        )

    def predict(self, features: pd.DataFrame) -> float:
        """
        Preprocesses input features and returns predicted house price in USD.
        """
        try:
            logging.info("Loading preprocessor and trained model...")
            preprocessor = load_object(file_path=self.preprocessor_path)
            model = load_object(file_path=self.model_path)

            logging.info("Applying feature engineering to input features...")
            features_engineered = add_engineered_features(features)

            logging.info("Transforming input features with preprocessor...")
            data_scaled = preprocessor.transform(features_engineered)

            logging.info("Predicting price...")
            preds_log = model.predict(data_scaled)
            pred_price = np.expm1(preds_log)[0]

            return float(max(10000.0, pred_price))

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:

    def __init__(
        self,
        bedrooms: int,
        bathrooms: float,
        sqft_living: int,
        sqft_lot: int,
        floors: float,
        waterfront: int,
        view: int,
        condition: int,
        sqft_above: int,
        sqft_basement: int,
        yr_built: int,
        yr_renovated: int,
        city: str,
        zipcode: str,
    ):
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.sqft_living = sqft_living
        self.sqft_lot = sqft_lot
        self.floors = floors
        self.waterfront = waterfront
        self.view = view
        self.condition = condition
        self.sqft_above = sqft_above
        self.sqft_basement = sqft_basement
        self.yr_built = yr_built
        self.yr_renovated = yr_renovated
        self.city = city
        self.zipcode = str(zipcode)

    def get_data_as_data_frame(self) -> pd.DataFrame:
        try:
            custom_data_dict = {
                "bedrooms": [self.bedrooms],
                "bathrooms": [self.bathrooms],
                "sqft_living": [self.sqft_living],
                "sqft_lot": [self.sqft_lot],
                "floors": [self.floors],
                "waterfront": [self.waterfront],
                "view": [self.view],
                "condition": [self.condition],
                "sqft_above": [self.sqft_above],
                "sqft_basement": [self.sqft_basement],
                "yr_built": [self.yr_built],
                "yr_renovated": [self.yr_renovated],
                "city": [self.city],
                "statezip": [f"WA {self.zipcode}"],
                "zipcode": [self.zipcode],
            }

            return pd.DataFrame(custom_data_dict)

        except Exception as e:
            raise CustomException(e, sys)
