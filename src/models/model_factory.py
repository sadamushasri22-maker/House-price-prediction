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
    VotingRegressor,
)

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


def get_models():

    cat = CatBoostRegressor(
        iterations=600,
        learning_rate=0.03,
        depth=6,
        verbose=0,
        random_state=42,
    )

    lgb = LGBMRegressor(
        n_estimators=600,
        learning_rate=0.03,
        num_leaves=31,
        random_state=42,
        verbose=-1,
    )

    xgb = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=500,
        learning_rate=0.03,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )

    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    et = ExtraTreesRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    ensemble = VotingRegressor(
        estimators=[
            ("catboost", cat),
            ("lightgbm", lgb),
            ("xgboost", xgb),
            ("random_forest", rf),
        ],
        weights=[0.35, 0.35, 0.20, 0.10],
    )

    models = {
        "Random Forest": rf,
        "Extra Trees": et,
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
        "XGBoost": xgb,
        "LightGBM": lgb,
        "CatBoost": cat,
        "Ensemble Blend": ensemble,
    }

    return models


def get_xgboost():
    return XGBRegressor(
        objective="reg:squarederror",
        random_state=42,
    )