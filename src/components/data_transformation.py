import os
import sys
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import DataTransformationConfig
from src.utils.common import save_object


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies consistent advanced feature engineering to input DataFrames.
    """
    df = df.copy()
    
    # Extract clean zipcode if statezip column present
    if "statezip" in df.columns:
        df["zipcode"] = df["statezip"].apply(
            lambda x: str(x).split()[-1] if " " in str(x) else str(x)
        )
    elif "zipcode" not in df.columns:
        df["zipcode"] = "98001"
        
    # House age
    if "yr_built" in df.columns:
        df["house_age"] = 2014 - df["yr_built"]
    else:
        df["house_age"] = 0

    # Renovation metrics
    if "yr_renovated" in df.columns:
        df["is_renovated"] = (df["yr_renovated"] > 0).astype(int)
        df["renovated_age"] = df.apply(
            lambda r: (2014 - r["yr_renovated"]) if r["yr_renovated"] > 0 else r["house_age"],
            axis=1
        )
    else:
        df["is_renovated"] = 0
        df["renovated_age"] = df["house_age"]

    # Total square footage & ratios
    if "sqft_living" in df.columns and "sqft_lot" in df.columns:
        df["total_sqft"] = df["sqft_living"] + df["sqft_lot"]
        df["sqft_living_ratio"] = df["sqft_living"] / (df["sqft_lot"] + 1.0)
    else:
        df["total_sqft"] = 0
        df["sqft_living_ratio"] = 0.0

    if "sqft_above" in df.columns and "sqft_living" in df.columns:
        df["sqft_above_ratio"] = df["sqft_above"] / (df["sqft_living"] + 1.0)
    else:
        df["sqft_above_ratio"] = 1.0

    if "sqft_basement" in df.columns:
        df["has_basement"] = (df["sqft_basement"] > 0).astype(int)
    else:
        df["has_basement"] = 0

    if "bedrooms" in df.columns and "bathrooms" in df.columns:
        df["total_rooms"] = df["bedrooms"] + df["bathrooms"]
        if "sqft_living" in df.columns:
            df["sqft_per_room"] = df["sqft_living"] / (df["total_rooms"] + 0.5)
        else:
            df["sqft_per_room"] = 0.0
    else:
        df["total_rooms"] = 0
        df["sqft_per_room"] = 0.0

    return df


class DataTransformation:

    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_data_transformer_object(self):
        """
        Creates the preprocessing pipeline.
        """
        try:
            numerical_columns = [
                "bedrooms",
                "bathrooms",
                "sqft_living",
                "sqft_lot",
                "floors",
                "waterfront",
                "view",
                "condition",
                "sqft_above",
                "sqft_basement",
                "yr_built",
                "yr_renovated",
                "house_age",
                "is_renovated",
                "renovated_age",
                "total_sqft",
                "has_basement",
                "sqft_living_ratio",
                "sqft_above_ratio",
                "total_rooms",
                "sqft_per_room",
            ]

            categorical_columns = [
                "city",
                "zipcode",
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns),
                ],
                remainder="drop"
            )

            logging.info("Preprocessor object created successfully")
            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path):
        """
        Reads train/test data, applies feature engineering & preprocessing,
        saves preprocessor object, and returns transformed arrays & targets.
        """
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Train and Test data loaded successfully")

            # Apply feature engineering
            train_df = add_engineered_features(train_df)
            test_df = add_engineered_features(test_df)

            preprocessing_obj = self.get_data_transformer_object()

            target_column = "price"

            input_feature_train_df = train_df.drop(columns=[target_column], errors="ignore")
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column], errors="ignore")
            target_feature_test_df = test_df[target_column]

            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_feature_train_df
            )

            input_feature_test_arr = preprocessing_obj.transform(
                input_feature_test_df
            )

            save_object(
                file_path=self.config.preprocessor_obj_file_path,
                obj=preprocessing_obj,
            )

            logging.info("Preprocessor object saved successfully")

            return (
                input_feature_train_arr,
                input_feature_test_arr,
                target_feature_train_df,
                target_feature_test_df,
            )

        except Exception as e:
            raise CustomException(e, sys)