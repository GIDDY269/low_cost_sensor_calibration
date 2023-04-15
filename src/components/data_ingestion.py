import pandas 
import os
import sys
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException



@dataclass
class DATA_INGESTION_CONFIG :
    artifact_filepath = 'user/low_cost_sensor_calibration/artifacts'
    data_file_path = os.path.join(artifact_filepath,'ingested_data.csv')
    road_file_path = os.path.join(artifact_filepath,'road_length.csv')
    
class DATA_INGESTION :
    def __init__(self):
        self.ingestion_config = DATA_INGESTION_CONFIG()
        
    def initiate_data_ingestion(self):
        logging.info('initiating data ingestion')
        
        try:
            data = pd.read_csv('user/low_cost_sensor_calibration/notebook/data/raw_collocated_data.csv')
            road_length_df = pd.csv('user/low_cost_sensor_calibration/notebook/data/road_lengths.csv')
            
            logging.info('loaded the data')
