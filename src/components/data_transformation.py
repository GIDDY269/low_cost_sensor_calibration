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
    train_data_path = os.path.join(artifact_filepath,'Train_data.csv')
    test_data_path = os.path.join(artifact_filepath,'Test_data.csv')
    
class DATA_TRANSFORMATION:
    def __init__(self):
        self.transfrom_config = DATA_TRANSFORM_CONFIG()
        
    def train_data_transform(self,data,road_length):
        try:
            # convert to datetime
        
            data['DateTime'] = pd.to_datetime(data['DateTime'])
            
            # rearranging dataframe and removing locations without coresponding values for either airnow or cs
            i15_reference_reading = "PM2.5(I-25 Globeville/AirNow)"
            logging.info('stacking train data')
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
            
    # creating function to organise test data
    def organise_test_data(self,df1,df2,road_df):
        df1['DateTime'] = pd.to_datetime(df1['DateTime'])
        df2['DateTime'] = pd.to_datetime(df2['DateTime'])
            
        """
        Utility function to organise our test data
        
        """
        try:
            logging.info('stacking tests data')
            new_data = pd.DataFrame(
                np.vstack(
                    [
                        pd.concat(
                            [df1.iloc[:, 0], df1.iloc[:, 1], df1.iloc[:, 3:5], df1.iloc[:, 9]],
                            axis=1,
                            ),
                        pd.concat(
                            [df1.iloc[:, 0], df1.iloc[:, 5], df1.iloc[:, 7:9], df1.iloc[:, 10]],
                            axis=1,
                            ),
                        ]
                    ),
                columns=["Datetime", "pm_cs", "temp", "humidity", "pm_airnow"]
                )
            
            camp_sensor_column1 = ["CAMP"] * len(df1)
            denvor_sensor_column1 = ["i25_denver"] * len(df1)
            new_data["airnow_sensor"] = camp_sensor_column1 + denvor_sensor_column1
            
            # second test data
            new_data2 = pd.DataFrame(
                np.vstack(
                    [
                        pd.concat(
                            [df2.iloc[:, 0], df2.iloc[:, 1], df2.iloc[:, 3:5], df2.iloc[:, 9]],
                            axis=1,
                            ),
                        pd.concat(
                            [df2.iloc[:, 0], df2.iloc[:, 5], df2.iloc[:, 7:9], df2.iloc[:, 10]],
                            axis=1,
                            ),
                        ]
                    ),
                columns=["Datetime", "pm_cs", "temp", "humidity", "pm_airnow"]
                )
            
            camp_sensor_column2 = ["CAMP"] * len(df2)
            denvor_sensor_column2 = ["i25_denver"] * len(df2)
            new_data2["airnow_sensor"] = camp_sensor_column2 + denvor_sensor_column2
            
            # merging both dataframes
            full_test_data = pd.concat([new_data,new_data2], axis=0)
            full_test_data["cs_sensor"] = full_test_data["airnow_sensor"]
            
            #setting threshold for true valid valyes
            low = 0
            high =  1500

            full_test_data = full_test_data[
                (full_test_data["pm_airnow"] > low)
                & (full_test_data["pm_cs"] > low)
                & (full_test_data["temp"] > low)
                & (full_test_data["humidity"] > low)
                & (full_test_data["pm_cs"] < high)
                ]   

            full_test_data = full_test_data.dropna(
                subset=["pm_cs", "temp", "humidity", "pm_airnow"]
                )
            # adding day,month and weekend columns to dataframe

            full_test_data['Time'] = full_test_data['Datetime'].dt.hour
            full_test_data['month'] = full_test_data['Datetime'].dt.month
            
            full_test_data['weekend'] = (full_test_data['Datetime'].dt.dayofweek >= 4).astype(int)
            # Adding cyclical enconding to hour and month  labels
            full_test_data['sin_time'] = full_test_data['Time'].apply(lambda x : math.sin(x) * 2 / (math.pi/24))
            full_test_data['cos_time'] = full_test_data['Time'].apply(lambda x : math.cos(x) * 2 / (math.pi/24))
            
            full_test_data['sin_month'] = full_test_data['month'].apply(lambda x : math.cos(x) * 2 / (math.pi/12))
            full_test_data['cos_month'] = full_test_data['month'].apply(lambda x : math.cos(x) * 2 / (math.pi/12))
            # mergring road data
            full_test_data = road_df.merge(full_test_data,on = 'airnow_sensor')
            return full_test_data
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,ingested_df,road_length_df,test_1,test_2):
        try :
            logging.info('initiating data transformation')
            ingested_df = pd.read_csv(ingested_df)
            road_length_df = pd.read_csv(road_length_df)
            test_1 = pd.read_csv(test_1)
            test_2 = pd.read_csv(test_2)
            logging.info('reading the ingested dataframe and load length dataframe')
            
            train_df =self.train_data_transform(ingested_df,road_length_df)
            test_df = self.organise_test_data(test_1,test_2, road_length_df)
            
            logging.info('Data Transformation Complete')
            logging.info(f'new data columns {train_df.columns}')
            logging.info(f'test data columns {test_df.columns}')
            
            return(train_df,test_df)
        except Exception as e:
            raise CustomException(e,sys)
        
        
        
        
        