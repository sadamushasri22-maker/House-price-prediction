import os
import sys
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import DataTransformationConfig
from src.utils.common import save_object


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
                "view",
                "condition",
                "sqft_above",
                "sqft_basement",
                "yr_built",
                "yr_renovated",
            ]

            categorical_columns = [
                "date",
                "waterfront",
                "street",
                "city",
                "statezip",
                "country",
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
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns),
                ]
            )

            logging.info("Preprocessor object created successfully")

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        """
        Reads train/test data, applies preprocessing,
        saves the preprocessor object, and returns transformed arrays.
        """
        try:

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Train and Test data loaded successfully")

            preprocessing_obj = self.get_data_transformer_object()

            target_column = "price"

            input_feature_train_df = train_df.drop(columns=[target_column])
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column])
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