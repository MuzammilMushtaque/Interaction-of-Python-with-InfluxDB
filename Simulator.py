#                      Develop Python Application to Calculate the Target Heart Rate of Human being
# Reference: https://www.heartonline.org.au/resources/calculators/target-heart-rate-calculator

import random

def Target_Heart_Rate(age, HR_rest):
    '''
    Target Heart Rate (THR) range values are often calculated to ensure exercise intensity is 
    maintained at a desired level. This calculator automatically calculates THR ranges.
    The Karvonen formula is often used for this purpose and calculates results as a function of 
    heart rate reserve (HRR) and maximum heart rate (HRmax).
    '''
    desired_training_intensity_ranges = {
        'Very Light': (1.0, 19.0),
        'Light': (20.0, 39.0),
        'Moderate': (40.0, 59.0),
        'Hard': (60.0, 84.0),
        'Very Hard': (85.0, 100.0)
    }

    desired_training_intensity = random.choice(list(desired_training_intensity_ranges.keys()))
    desired_training_intensity_min, desired_training_intensity_max = desired_training_intensity_ranges[desired_training_intensity]
    desired_training_intensity_current = random.uniform(desired_training_intensity_min, desired_training_intensity_max)

    HRmax = 220. - age
    HRR = HRmax - HR_rest
    
    '''
    Target HR range is calculated as follows:
    '''
    THRR_current = (HRR * desired_training_intensity_current/100) + HR_rest
    THRR_min = (HRR * desired_training_intensity_min/100) + HR_rest
    THRR_max = (HRR * desired_training_intensity_max/100) + HR_rest
    
    return [desired_training_intensity, THRR_current, THRR_min, THRR_max]

#                       Implement the Target Heart Rate application to InfluxDB

# First Users need to initialized the Organization, User, Bucket name  
# Organization Name: your_org_name
# User Name: your_user_name 
# Bucket Name: your_bucker_name

# Create 
# Measurement => Heart Rate
# tags => Desired Training Intensity
# fields => Current_THRR, Min_THRR, Max_THRR (THRR represents Target heart rate range)

from influxdb_client import InfluxDBClient
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import time

token= "aFFa8cFx********************************************RnrJQmPQ==" # Your token_number
org = "Fachhochschule Kiel"
url = "http://localhost:8086"
# Initialize the InfluxDB client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# Initialize the InfluxDB client

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

for i in range(1,1000,1): #generate 1000 measurements (1 measurement/0.25 seconds interval)
    # Create an InfluxDB Point with weather data
    weather = Target_Heart_Rate(32., 60.)
    point = (
        influxdb_client.Point("Heart Rate")
        .tag("Desired_Training_Intensity", weather[0])
        .field("Current_THRR", weather[1])
        .field("Min_THRR", weather[2])
        .field("Max_THRR", weather[3])
    )

    write_api.write(bucket="Health", org=org, record=point)
    time.sleep(0.25)