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
from utils import model_feature,RMSE,get_disaggregated_metrics,split_data,train_model,lolo_valid

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
        print()
        print(f'the baseline rmse for the test data : {RMSE(test_data.pm_airnow,test_data.pm_cs)}')
        print()
        
        # printing the baseline disaggregated rmse for each location in the training data and test data
        print(f'the disaggregated metrics for each location in the training data {get_disaggregated_metrics(train_data)}')
        print()
        print(f'the disaggregated metrics for each location in the test data {get_disaggregated_metrics(test_data)}')
        print()
        
        # dropping some  features in both the test and training data
        logging.info('creating model features')
        new_train_data = model_feature(train_data)
        new_test_data = model_feature(test_data)
        
        # model features for training
        
        model_features = {
            "model_1": ["pm_cs"],
            "model_2": ["pm_cs", "temp", "humidity"],
            "model_3": ["pm_cs", "temp", "humidity", "a_road_500"],
            "model_4": [
                "pm_cs",
                "temp",
                "humidity",
                "a_road_500",
                "sin_time",
                "cos_time",
                "sin_month",
                "cos_month",
                ],
            "model_5": [
                "pm_cs",
                "temp",
                "humidity",
                "a_road_500",
                "sin_time",
                "cos_time",
                "sin_month",
                "cos_month",
                "weekend",
                ],
            }   
        
        logging.info('Test model performance with different features')
        # obtaining model with best performing features
        #linear regression
        train_model(LinearRegression(), new_train_data, new_test_data, model_features)
        #randomforestregressor
        print()
        train_model(RandomForestRegressor(), new_train_data, new_test_data, model_features)
        
        # training model with model_4 features since it has the better performance
        #splitting data
        logging.info('splitting data into test and train split')
        x_train,x_test,y_train,y_test = split_data(model_features['model_4'], new_train_data, new_test_data)
        
        # instantiateing model
        logging.info('instantiating model anf fitting')
        model = RandomForestRegressor()
        model.fit(x_train,y_train)
        
        #making predictions
        train_preds = model.predict(x_train)
        test_preds = model.predict(x_test)
        
        # disaggregrated errors in each location
        model_disagg_train_metrics = get_disaggregated_metrics(train_data,preds=train_preds,y_preds = True)
        model_disagg_test_metrics = get_disaggregated_metrics(test_data,test_preds,y_preds = True)
        
        # printing and comparing baseline and model disaggregated metrics for each location
        logging.info('comparing baseline and model disaggregated metrics')
        print("best model train")
        print(model_disagg_train_metrics)
        print("baseline train")
        print(get_disaggregated_metrics(train_data))
        
        print("best model test")
        print(model_disagg_test_metrics)
        print("baseline test")
        print(get_disaggregated_metrics(test_data))
        
        # performing lolo cross validation on train data
        lolo_metrics = lolo_valid(train_data, model_features, model)
        
        print("cross validation model train")
        print(lolo_metrics)
        print("baseline train")
        print(get_disaggregated_metrics(train_data))
        
        
        
        
        
        
        
        
        
        
        
        
        