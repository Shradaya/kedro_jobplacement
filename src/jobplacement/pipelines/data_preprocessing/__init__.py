"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.2
"""

from .pipeline import create_pipeline
from .nodes import exclude_feature
__all__ = ["create_pipeline"]

__version__ = "0.1"
