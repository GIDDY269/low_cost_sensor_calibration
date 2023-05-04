
from src.exception import CustomException
from src.logger import logging
import sys
sys.path.append('C:/Users/user/low_cost_sensor_calibration')
import pandas as pd
import math
from utils import load_object
from datetime import datetime

model = load_object('C:/Users/user/low_cost_sensor_calibration/artifacts/MODEL.pkl')

class calibrator:
    def __init__(self):
        pass
    
    def calibrate (self,sensor_data):
        try :
            logging.info('creating features')
            pm_cs = sensor_data['pm_cs']
            temp = sensor_data['temp']
            humidity = sensor_data['humidity']
            a_road_500 = sensor_data['a_road_500']
            date = sensor_data['datetime']
            logging.info('created datetime')
            sensor_data['Time'] = sensor_data['datetime'].hour
            sensor_data['month'] = sensor_data['datetime'].month
            logging.info('created time and month features')
            sensor_data['sin_time'] = math.sin(sensor_data['Time'])*2*(math.pi/24)
            sin_time = sensor_data['sin_time']
            sensor_data['cos_time'] = math.cos(sensor_data['Time'])*2*(math.pi/24)
            cos_time = sensor_data['cos_time']
            
            sensor_data['sin_month'] = math.sin(sensor_data['month'])*2*(math.pi/12)
            sin_month = sensor_data['sin_month']
            sensor_data['cos_month'] = math.cos(sensor_data['month'])*2*(math.pi/12)
            cos_month = sensor_data['cos_month']
            
            logging.info('created seasonal features')
            
            del sensor_data['datetime'], sensor_data['Time'], sensor_data['month']
            
            logging.info(f'dictionary keys : {sensor_data.keys()}')
            
            
            logging.info(f"Loaded model {model}")
            prediction = model.predict([[pm_cs,temp,humidity,a_road_500,sin_time,cos_time,sin_month,cos_month]])
            logging.info(f"Prediction: {prediction}")
            
            return prediction 
        except Exception as e:
            raise CustomException(e,sys)