import sys
sys.path.append('C:/Users/user/low_cost_sensor_calibration')
import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from utils import model_feature,RMSE,get_disaggregated_metrics

@dataclass
class MODEL_TRAINER_CONFIG:
    artifact_filepath = 'C:/Users/user/low_cost_sensor_calibration/artifacts/'
    model_train_config = os.path.join(artifact_filepath,'MODEL.pkl')
    
class MODEL_TRAINER:
    def __init__(self):
        self.model_train_config = MODEL_TRAINER_CONFIG()
        
    def initiate_model_trainer(self,train_data,test_data):
        logging.info('initiating model trainer')
        
        # printing baseline rmse for both the training and test data
        print(f'the baseline rmse for the training data : {RMSE(train_data.pm_airnow,train_data.pm_cs)}')
        print(f'the baseline rmse for the test data : {RMSE(test_data.pm_airnow,test_data.pm_cs)}')
        
        # printing the baseline disaggregated rmse for each location in the training data and test data
        print(f'the disaggregated metrics for each location in the training data {get_disaggregated_metrics(train_data)}')
        print(f'the disaggregated metrics for each location in the test data {get_disaggregated_metrics(test_data)}')
        
        # dropping some  features in both the test and training data
        train_data = model_feature(train_data)
        test_data = model_feature(test_data)
        
        
        
        
        
        
        
        
        
        