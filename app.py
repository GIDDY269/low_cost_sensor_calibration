import pandas
import numpy
from fastapi import FastAPI
import uvicorn
from src.pipeline.predict_pipeline import calibrator
from sensor_parameter import sensor_parameters
from datetime import datetime
import math
from utils import load_object
import json


#create app object
app = FastAPI()

# index route ,opens up automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return{'WELCOME'}

@app.post('/calibrate')
def sensor_calibration_endpoint(sensor_data : sensor_parameters):
    sensor_data = sensor_data.json()
    sensor_data = json.load(sensor_data)
    cal = calibrator()
    prediction = cal.calibrate(sensor_data)
    return {'calibrated pm2.5 readings':prediction}
    
if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)
