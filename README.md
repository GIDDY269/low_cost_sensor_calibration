## Time series modeling for air pollution monitoring with a focus on the calibration of low-cost sensors.¶

We have PM2.5 readings from low cost sensors and we want to learn a model that maps them to "true" readings from reference FEM (AirNow) sensors.
The model is trained on a dataset of sensor data and can be used to improve the accuracy of the sensor and save cost od purchasing the expensive sensors.


**Installation**
To install the model , clone the repository into your local machine

`git clone git clone https://github.com/GIDDY269/low_cost_sensor_calibration.git`


******************

Then, build the docker image;
`docker build -t low_cost_sensor_calibration .`

************************************************************

Then finally , run the image ;
`docker run -d--name low_cost_sensor_calibration -p 80:80 low_cost_sensor_calibration`

The app will now be running on port 80. You can access it by opening a web browser and navigating to `http://localhost:80`

********************************************

**Usage**

After accessing the api on your browser, you show be able to see a `welcome` text on your browser.Go to the link at the top your browser and add `/docs` to be able to access the swagger ui

![first_image](https://raw.githubusercontent.com/GIDDY269/low_cost_sensor_calibration/main/images/Screenshot67.png)

* click on the the try it out button to test the api

****************************

![second image](https://raw.githubusercontent.com/GIDDY269/low_cost_sensor_calibration/main/images/Screenshot65.png)

* input all the values for each paremeter and click on `execute`

****************************

![third image](https://raw.githubusercontent.com/GIDDY269/low_cost_sensor_calibration/main/images/Screenshot66.png)

* U should get a result in the response body



