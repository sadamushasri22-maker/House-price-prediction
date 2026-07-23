from sklearn.metrics import r2_score


def evaluate_models(models, X_train, X_test, y_train, y_test):

    model_report = {}

    trained_models = {}

    for model_name, model in models.items():

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        score = r2_score(y_test, predictions)

        model_report[model_name] = score

        trained_models[model_name] = model

    return model_report, trained_models