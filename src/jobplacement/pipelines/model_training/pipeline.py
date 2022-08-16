"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import tune_hyperparameters, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                tune_hyperparameters,
                ["params:trial_count", "X_train", "y_train", "X_valid", "y_valid"],
                "best_param",
                name="tune",
            ),
            node(
                train_model,
                ["best_param", "X_train", "y_train", "X_valid", "y_valid"],
                "lightgbm_model",
                name="train",
            ),
        ]
    )
