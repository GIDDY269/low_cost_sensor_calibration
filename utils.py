import pandas as pd
import numpy as np
import sys
sys.path.append('C:/Users/user/low_cost_sensor_calibration')
from src.exception import CustomException
from src.logger import logging
import math
from sklearn.metrics import mean_squared_error



# structure the training data anfd perform some feature engineering
def train_data_transform(data,road_length):
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
def organise_test_data(df1,df2,road_df):
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


# caculate the root mean sqaured error
def RMSE(y_true,y_preds) :
    return round(mean_squared_error(y_true,y_preds,squared = False),2)


# get the disagregate rsme for each for locations 
def get_disaggregated_metrics(df,preds = None,y_preds = False) :
    '''
     Disaggregate evaluation metrics into locations
     '''
    result = {}
    if y_preds == True :
        for sensor in df['cs_sensor'].unique() :
            sensor_data = df[df['cs_sensor'] == sensor ]
            sensor_pm_cs = preds[df[df['cs_sensor'] == sensor].index]
            sensor_pm_airnow = df[df['cs_sensor'] == sensor]['pm_airnow']
            rmse =RMSE(sensor_pm_airnow,sensor_pm_cs)
            result[sensor] = rmse
    else :
        for sensor in df['cs_sensor'].unique() :
            sensor_data = df[df['cs_sensor'] == sensor ]
            sensor_pm_cs = sensor_data['pm_cs']
            sensor_pm_airnow = sensor_data['pm_airnow']
            
            rmse = RMSE(sensor_pm_airnow,sensor_pm_cs)
            result[sensor] = rmse
                    
    return {'rsme' : result}


# drops unnecessary columns
def model_feature(df) :
    new_df = df.drop(['airnow_sensor','cs_sensor','longitude','latitude','Time','month'],axis = 1)
    new_df = new_df.set_index('Datetime')
    return new_df

# splitting data 
def split_data(feature,train_data,test_data) :
        x_train = train_data[feature]
        y_train  = train_data['pm_airnow']
        x_test = test_data[feature]
        y_test = test_data['pm_airnow']
        return x_train,x_test,y_train,y_test
    
# train model
def train_model(model,train_data,test_data,model_features):
    estimator = model
    for key,values in model_features.items() :
        x_train,x_test,y_train,y_test = split_data(values,train_data,test_data)
        print(f'Training {model} model')
        print(f'{key} features : {values}')
        estimator.fit(x_train,y_train)
        train_preds = model.predict(x_train)
        test_preds = model.predict(x_test)
        model_training_rmse = RMSE(y_train,train_preds)
        print(f'Model train rmse : {model_training_rmse}')
        model_test_rmse = RMSE(y_test,test_preds)
        print(f'Model test rmse : {model_test_rmse}')
        print('===========================================================================================')

def lolo_valid(training_df,model_features,model):
    lolo_validation_errors = {}
    locations = training_df["cs_sensor"].unique()

    for leave_sensor in locations:

        train = training_df[training_df["cs_sensor"] != leave_sensor]
        validation = training_df[training_df["cs_sensor"] == leave_sensor]
        from sklearn.ensemble import RandomForestRegressor
        rf = RandomForestRegressor()

        x_train, y_train = train[model_features['model_4']], train["pm_airnow"]
        x_val, y_val = validation[model_features['model_4']], validation["pm_airnow"]

        rf.fit(x_train, y_train)

        y_hat_val = model.predict(x_val)

        error = RMSE(y_val, y_hat_val)
        lolo_validation_errors[leave_sensor] = error
    return lolo_validation_errors