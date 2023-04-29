import sys
sys.path.append('C:/Users/user/low_cost_sensor_calibration')
import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
import os
from utils import train_data_transform,organise_test_data


@dataclass
class DATA_TRANSFORM_CONFIG:
    artifact_filepath = 'C:/Users/user/low_cost_sensor_calibration/artifacts/'
    train_data_path = os.path.join(artifact_filepath,'Train_data.csv')
    test_data_path = os.path.join(artifact_filepath,'Test_data.csv')
    
class DATA_TRANSFORMATION:
    def __init__(self):
        self.transfrom_config = DATA_TRANSFORM_CONFIG()
        
    def initiate_data_transformation(self,ingested_df,road_length_df,test_1,test_2):
        try :
            logging.info('initiating data transformation')
            ingested_df = pd.read_csv(ingested_df)
            road_length_df = pd.read_csv(road_length_df)
            test_1 = pd.read_csv(test_1)
            test_2 = pd.read_csv(test_2)
            logging.info('reading the ingested dataframe and load length dataframe')
            
            train_df =train_data_transform(ingested_df,road_length_df)
            test_df = organise_test_data(test_1,test_2, road_length_df)
            
            logging.info('Data Transformation Complete')
            logging.info(f'new data columns {train_df.columns}')
            logging.info(f'test data columns {test_df.columns}')
            
            return(train_df,test_df)
        except Exception as e:
            raise CustomException(e,sys)
        
        
        
        
        