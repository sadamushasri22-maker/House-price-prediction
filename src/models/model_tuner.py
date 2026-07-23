from sklearn.model_selection import RandomizedSearchCV


def tune_model(model, params, X_train, y_train):

    random_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=params,
        n_iter=20,
        scoring="r2",
        cv=5,
        verbose=2,
        random_state=42,
        n_jobs=-1,
    )

    random_search.fit(X_train, y_train)

    print("\nBest Parameters:")
    print(random_search.best_params_)

    print(f"Best CV Score: {random_search.best_score_:.4f}")

    return random_search.best_estimator_