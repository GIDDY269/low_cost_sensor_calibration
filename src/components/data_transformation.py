import sys
sys.path.append('C:/Users/user/low_cost_sensor_calibration')
import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
import os
import math


@dataclass
class DATA_TRANSFORM_CONFIG:
    artifact_filepath = 'C:/Users/user/low_cost_sensor_calibration/artifacts/'
    transform_data_path = os.path.join(artifact_filepath,'Transformed_data.csv')
    
class DATA_TRANSFORMATION:
    def __init__(self):
        self.transfrom_config = DATA_TRANSFORM_CONFIG()
        
    def data_transform(self,data,road_length):
        try:
            # convert to datetime
        
            data['DateTime'] = pd.to_datetime(data['DateTime'])
            
            # rearranging dataframe and removing locations without coresponding values for either airnow or cs
            i15_reference_reading = "PM2.5(I-25 Globeville/AirNow)"
            
            new_data_df = pd.DataFrame(
                np.vstack(
                    [
                        data.iloc[:, 1:5],
                        pd.concat(
                            [
                                data.iloc[:, 5:8],
                                data[i15_reference_reading],
                                ],
                            axis=1,
                            ),
                        pd.concat(
                            [
                                data.iloc[:, 8:11],
                                data[i15_reference_reading],
                                ],
                            axis=1,
                            ),
                        data.iloc[:, 11:15],
                        data.iloc[:, 15:19],
                        ]
                    ),
                columns=["pm_cs", "temp", "humidity", "pm_airnow"],
                )
            # creating datetime for new rows
            new_data_df['Datetime'] = pd.to_datetime(
                pd.concat([data.iloc[:, 0]] * 5, ignore_index=True)
                )
            cs_sensor = ["NJH", "i25_glo_1", "i25_glo_2", "i25_glo_3", "la_casa"]
            cs_sensor_label = np.repeat(cs_sensor,len(data))
            new_data_df['cs_sensor'] = cs_sensor_label
            
            # creating airnow sencor location tag
            new_data_df['airnow_sensor'] = new_data_df['cs_sensor'].apply(lambda x : 'i25_glo' if x in ["i25_glo_1", "i25_glo_2", "i25_glo_3"]
                                                                          else x)
            
            # extracting hour and month data and weekends
            
            new_data_df['Time'] = new_data_df['Datetime'].dt.hour
            new_data_df['month'] = new_data_df['Datetime'].dt.month
            new_data_df["weekend"] = (new_data_df["Datetime"].dt.dayofweek >= 4).astype("int")
            
            
            # extracting hour and month data and weekends
            
            new_data_df['Time'] = new_data_df['Datetime'].dt.hour
            new_data_df['month'] = new_data_df['Datetime'].dt.month
            new_data_df["weekend"] = (
                new_data_df["Datetime"].dt.dayofweek >= 4
                ).astype("int")
            
            # creating seasonal data point
            new_data_df['sin_time'] = new_data_df['Time'].apply(lambda x : math.sin(x)*2*(math.pi/24))
            new_data_df['cos_time'] = new_data_df['Time'].apply(lambda x : math.cos(x)*2*(math.pi/24))
            
            new_data_df['sin_month'] = new_data_df['month'].apply(lambda x : math.sin(x)*2*(math.pi/12))
            new_data_df['cos_month'] = new_data_df['month'].apply(lambda x : math.cos(x)*2*(math.pi/12))
            
            
            #setting threshold for true valid valyes
            low = 0
            high =  1500
            
            new_data_df = new_data_df[
                (new_data_df["pm_airnow"] > low)
                &( new_data_df["pm_cs"] > low)
                & (new_data_df["temp"] > low)
                & (new_data_df["humidity"] > low)
                & (new_data_df["pm_cs"] < high)
                ]
            
            
            new_data_df = new_data_df.dropna(
                subset=["pm_cs", "temp", "humidity", "pm_airnow"]
                )
            # adding road length data
            new_data_df = road_length.merge(new_data_df,on='airnow_sensor')
            
            return new_data_df
        except Exception as e :
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self):
        try :
            logging.info('initiating data transformation')
            ingested_df = pd.read_csv('C:/Users/user/low_cost_sensor_calibration/artifacts/ingested_data.csv')
            road_length_df = pd.read_csv('C:/Users/user/low_cost_sensor_calibration/artifacts/road_length.csv')
            logging.info('reading the ingested dataframe and load length dataframe')
            
            transform_df =self.data_transform(ingested_df,road_length_df)
            
            logging.info('Data Transformation Complete')
            
            return(transform_df,self.transfrom_config.transform_data_path)
        except Exception as e:
            raise CustomException(e,sys)
        
        
        
        
        