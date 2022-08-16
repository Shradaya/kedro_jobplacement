from sklearn.metrics import roc_curve, auc
from lightgbm import LGBMClassifier
import mlflow
import mlflow.lightgbm

# Hyperparameter tunning library
import optuna
import warnings
from functools import partial

warnings.filterwarnings("ignore")


def tune_hyperparameters(trial_count, X_train, X_valid, y_test, y_valid):
    print(mlflow.active_run().info)
    study = optuna.create_study(direction="maximize")
    fun_objective = partial(objective, X_train, X_valid, y_test, y_valid)
    study.optimize(fun_objective, n_trials=trial_count)

    trial = study.best_trial
    print("AUC: {}".format(trial.value))
    print("Best hyperparameters: {}".format(trial.params))
    return trial.params


def objective(X_train, y_train, X_valid, y_valid, trial):
    param = {
        "objective": "binary",
        "metric": "auc",
        "learning_rate": trial.suggest_float("learning_rate", 1e-2, 1e-1),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.4, 1.0),
        "subsample": trial.suggest_float("subsample", 0.4, 1.0),
        "random_state": 42,
    }
    trial_dict = {}
    trial_count = str(trial.__dict__["_trial_id"])
    trial_dict[f"trial_{trial_count}_learning_rate"] = param["learning_rate"]
    trial_dict[f"trial_{trial_count}_colsample_bytree"] = param["colsample_bytree"]
    trial_dict[f"trial_{trial_count}_subsample"] = param["subsample"]

    mlflow.log_params(trial_dict)

    auc = model_training_tracking(param, X_train, y_train, X_valid, y_valid)
    return auc


def model_training_tracking(params, X_train, y_train, X_valid, y_valid):
    lgb_clf = train_model(params, X_train, y_train, X_valid, y_valid)
    mlflow.log_metrics({"Score": lgb_clf.score(X_valid, y_valid)})

    lgb_valid_prediction = lgb_clf.predict_proba(X_valid)[:, 1]
    fpr, tpr, _ = roc_curve(y_valid, lgb_valid_prediction)
    roc_auc = auc(fpr, tpr)
    print("=====================================")
    print("Validation AUC:{}".format(roc_auc))
    auc_metric = {"Validation_AUC": roc_auc}
    mlflow.log_metrics(auc_metric)
    print(f"Logged metrics {auc_metric}")
    print("=====================================")

    return roc_auc


def train_model(params, X_train, y_train, X_valid, y_valid):
    model = LGBMClassifier(**params)
    model.fit(
        X_train,
        y_train,
        eval_set=[(X_train, y_train), (X_valid, y_valid)],
        early_stopping_rounds=50,
        verbose=20,
    )
    mlflow.sklearn.log_model(model, "model")
    return model


# def deploy_model(model_path):
#     model = mlflow.pyfunc.load_model(model_path)
#     return model_path
