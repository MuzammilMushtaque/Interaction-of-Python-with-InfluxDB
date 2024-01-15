# Extract and Display the Filtered Dataset 

import time
import random
from datetime import datetime
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient
import influxdb_client

token= "aFFa8cFxUE************qJdJBPRnrJQmPQ==" # Your Token_number
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

def influxdb_to_python(fields, tags):
    bucket_name = "Health"
    print (fields)
    query = f'''
        from(bucket: "{bucket_name}")
            |> range(start: -1h)
            |> filter(fn: (r) =>
                r._measurement == "Heart Rate" and
                r._field == "{fields}" and
                r.Desired_Training_Intensity == "{tags}" 
            )
            |> keep(columns: ["_time", "_value"])  
            |> yield(name: "time_and_field_values")
    '''
    # Execute the query and fetch the data
    query_api = client.query_api()
    tables = query_api.query(query)


    # Extract time and field values
    time_values = []
    field_values = []
    for table in tables:
        for record in table.records:
            time_values.append(record.values.get("_time"))
            field_values.append(record.values.get("_value"))

    # Plotting time versus field values
    plt.figure(figsize=(10, 6))
    plt.plot(time_values, field_values, marker='o')
    plt.title("Time versus Estimated Target Heart Rate in the "+ tags + " Desired training Intensity")
    plt.xlabel("Time")
    plt.ylabel("Estimated Target Heart Rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('Python_display.png')
    plt.show()
    
# Randomly select the tags and fields to generate timeseries plot
influxdb_to_python(random.choice(["Current_THRR"]),
                   random.choice(['Very Light', 'Light', 'Moderate', 'Hard', 'Very Hard'])
                  )
