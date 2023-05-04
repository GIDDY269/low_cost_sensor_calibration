
from src.exception import CustomException
from src.logger import logging
import sys
sys.path.append('C:/Users/user/low_cost_sensor_calibration')
import pandas as pd
import math
from utils import load_object
from datetime import datetime

class calibrator:
    def __init__(self):
        pass
    
    def calibrate (self,data):
        try :
            logging.info('calibrating sensor readings')
            pm_cs = data['pm_cs']
            temp = data['temp']
            a_road_500 = data['a_road_500']
            date = datetime.strptime(data['datetime'],format= "%Y-%m-%d %H:%M:%S" )
            data['Time'] = date.dt.hour
            data['month'] = date.dt.month
            
            data['sin_time'] = data['Time'].apply(lambda x : math.sin(x)*2*(math.pi/24))
            sin_time = data['sin_time']
            data['cos_time'] = data['Time'].apply(lambda x : math.cos(x)*2*(math.pi/24))
            cos_time = data['cos_time']
            
            data['sin_month'] = data['month'].apply(lambda x : math.sin(x)*2*(math.pi/12))
            sin_month = data['sin_month']
            data['cos_month'] = data['month'].apply(lambda x : math.cos(x)*2*(math.pi/12))
            cos_month = data['cos_month']
            
            del data['datetime','Time','month']
            #load model
            model = load_object('C:/Users/user/low_cost_sensor_calibration/artifacts/MODEL.pkl')
            prediction = model.predict([[pm_cs,temp,a_road_500,sin_time,cos_time,sin_month,cos_month]])
            logging.info('calibrated readings')
            return prediction 
        except Exception as e:
            raise CustomException(e,sys)