"""
This is a boilerplate test file for pipeline 'data_preprocessing'
generated using Kedro 0.18.2.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""
import pytest
import pandas as pd
from kedro.config import ConfigLoader
from constants import CONF_PATH
from kedro.io import DataCatalog
from kedro.extras.datasets.pandas import CSVDataSet
from jobplacement.pipelines.data_preprocessing import exclude_feature

class TestDataPreprocessing:
    input_data = [
        (pd.DataFrame({'col1':[1,2,3], 'col2':[2,3,4]}), 
        "col1", 
        pd.DataFrame({'col2':[2,3,4]}))
    ]
    @pytest.mark.parametrize('data, drop_features, expected', input_data)
    def test_get_start_and_end_of_week(self, data, drop_features, expected):
        function_output = exclude_feature(data, drop_features)
        assert expected.columns == function_output.columns