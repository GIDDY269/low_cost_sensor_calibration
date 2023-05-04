from pydantic import BaseModel,validator
from datetime import datetime

# class with describes the sensor parameters
class sensor_parameters(BaseModel):
    pm_cs: float
    temp: float
    humidity: float
    a_road_500 : float
    datetime : datetime

    