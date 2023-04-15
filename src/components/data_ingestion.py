import sys
sys.path.append('C:/Users/user/low_cost_sensor_calibration')
import os
import pandas as pd
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException



@dataclass
class DATA_INGESTION_CONFIG :
    artifact_filepath = 'C:/Users/user/low_cost_sensor_calibration/artifacts/'
    data_file_path = os.path.join(artifact_filepath,'ingested_data.csv')
    road_file_path = os.path.join(artifact_filepath,'road_length.csv')
    
class DATA_INGESTION :
    def __init__(self):
        self.ingestion_config = DATA_INGESTION_CONFIG()
        
    def initiate_data_ingestion(self):
        logging.info('initiating data ingestion')
        
        try:
            data = pd.read_csv('C:/Users/user/low_cost_sensor_calibration/notebook/data/raw_collocated_data.csv')
            road_length_df = pd.read_csv('C:/Users/user/low_cost_sensor_calibration/notebook/data/road_lengths.csv')
            
            logging.info('loaded the data')
            
            os.makedirs(self.ingestion_config.artifact_filepath, exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.data_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.road_file_path), exist_ok=True)
            
            data.to_csv(self.ingestion_config.data_file_path,header=True,index=False)
            road_length_df.to_csv(self.ingestion_config.road_file_path,header=True,index=False)
            
            logging.info('Ingestion complete')
            
            return(self.ingestion_config.data_file_path,self.ingestion_config.road_file_path)
        
        except Exception as e:
            raise CustomException(e,sys)
            
            
if __name__=='__main__':
    obj = DATA_INGESTION()
    d,r = obj.initiate_data_ingestion()            
