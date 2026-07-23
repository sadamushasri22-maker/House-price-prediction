from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
    ElasticNet,
)

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
)

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


def get_models():

    models = {

        "Linear Regression": LinearRegression(),

        "Ridge": Ridge(random_state=42),

        "Lasso": Lasso(
            random_state=42,
            max_iter=10000,
        ),

        "ElasticNet": ElasticNet(
            random_state=42,
        ),

        "Decision Tree": DecisionTreeRegressor(
            random_state=42,
        ),

        "Random Forest": RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1,
        ),

        "Extra Trees": ExtraTreesRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1,
        ),

        "Gradient Boosting": GradientBoostingRegressor(
            random_state=42,
        ),

        "AdaBoost": AdaBoostRegressor(
            random_state=42,
        ),

        "XGBoost": XGBRegressor(
            objective="reg:squarederror",
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            random_state=42,
        ),

        "LightGBM": LGBMRegressor(
            n_estimators=300,
            random_state=42,
        ),

        "CatBoost": CatBoostRegressor(
            verbose=0,
            random_state=42,
        ),
    }

    return models

def get_xgboost():

     return XGBRegressor(
        objective="reg:squarederror",
        random_state=42,
    )