import sys
sys.path.append('C:/Users/user/low_cost_sensor_calibration')
import os
import pandas as pd
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DATA_TRANSFORMATION
from src.components.model_training import MODEL_TRAINER



@dataclass
class DATA_INGESTION_CONFIG :
    artifact_filepath = 'C:/Users/user/low_cost_sensor_calibration/artifacts/'
    data_file_path = os.path.join(artifact_filepath,'ingested_data.csv')
    road_file_path = os.path.join(artifact_filepath,'road_length.csv')
    test_data_1_filepath = os.path.join(artifact_filepath,'test_data_1.csv')
    test_data_2_filepath = os.path.join(artifact_filepath,'test_data_2.csv')
    
class DATA_INGESTION :
    def __init__(self):
        self.ingestion_config = DATA_INGESTION_CONFIG()
        
    def initiate_data_ingestion(self):
        logging.info('initiating data ingestion')
        
        try:
            data = pd.read_csv('C:/Users/user/low_cost_sensor_calibration/notebook/data/raw_collocated_data.csv')
            road_length_df = pd.read_csv('C:/Users/user/low_cost_sensor_calibration/notebook/data/road_lengths.csv')
            test_1 = pd.read_csv('C:/Users/user/low_cost_sensor_calibration/notebook/data/test-set_Sept-Oct.csv')
            test_2 = pd.read_csv('C:/Users/user/low_cost_sensor_calibration/notebook/data/test-set_Nov-Dec.csv')
            logging.info('loaded the data')
            
            # makinng directory name
            os.makedirs(self.ingestion_config.artifact_filepath, exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.data_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.road_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_1_filepath),exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_2_filepath),exist_ok=True)
            
            data.to_csv(self.ingestion_config.data_file_path,header=True,index=False)
            road_length_df.to_csv(self.ingestion_config.road_file_path,header=True,index=False)
            test_1.to_csv(self.ingestion_config.test_data_1_filepath,header=True,index=False)
            test_2.to_csv(self.ingestion_config.test_data_2_filepath,header=True,index=False)
            
            logging.info('Ingestion complete')
            
            return(self.ingestion_config.data_file_path,self.ingestion_config.road_file_path,self.ingestion_config.test_data_1_filepath,
                   self.ingestion_config.test_data_2_filepath)
        
        except Exception as e:
            raise CustomException(e,sys)
            
            
if __name__=='__main__':
    obj = DATA_INGESTION()
    T,r,t1,t2 = obj.initiate_data_ingestion()  

    transform = DATA_TRANSFORMATION()
    train_data,test_data = transform.initiate_data_transformation(T,r,t1,t2)  
    
    trainer = MODEL_TRAINER()
    trainer.initiate_model_trainer(train_data, test_data)        
    
    