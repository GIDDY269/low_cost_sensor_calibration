import pandas
import numpy
from fastapi import FastAPI
import uvicorn
from src.pipeline.predict_pipeline import calibrator
from sensor_parameter import sensor_parameters
from datetime import datetime
import math
from utils import load_object
from src.logger import logging




#create app object
app = FastAPI()


# index route ,opens up automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return{'WELCOME'}

@app.post('/calibrate')
def sensor_calibration_endpoint(sensor_data:sensor_parameters):
    logging.info(f"Received sensor data: {sensor_data}")
    sensor_data = sensor_data.dict()
    cal = calibrator()
    prediction = cal.calibrate(sensor_data)
    return {'Calibrated pm 2.5 reading': str(prediction)}
    

