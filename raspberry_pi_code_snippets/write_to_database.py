from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from enum import Enum
from datetime import datetime
import pytz

TOKEN = "o8iQsdxsSf1l7lNRAFIfKRdBSvmpzdEHmNeZqy5yrB4StPTcFqhj0_WONmK-UyN-ksGmycGVefWvgjv3GabqjQ==" #todo hide later
URL = "https://us-east-1-1.aws.cloud2.influxdata.com/"
ORG = "f6056c661b1ca7c8" # from url
BUCKET = "third_bucket" 

class Measurements(Enum): # should this be 3 seperate enums?
    # Sensor measurements (these have values between 0 - 100), these are shown on frontend
    light = 'light' # sufficient hours of light
    moisture = 'moisture' # sufficient soil moisture
    phosporous = "phosporous"
    nitrogen = "nitrogen"
    potassium = "potassium"
    leaf_health = 'leaf_health' # ratio of healthy leaves detected using ML
    temperature = "temperature"
    # Control measurements (threshold is a maximum, target is an ideal value)
    moisture_threshhold = 'moisture_threshhold'
    moisture_target= 'moisture_target'
    light_threshold = 'light_threshold'
    light_target ='light_target'
    pump_on = 'pump_on'
    led_on = 'led_on'
    # Decision measurements: , decision | last update is 0, decision is a string
    last_update = 'last_update' # timestamp of when an update was made. Update won't be made for 3 more days
    decision = 'decision' # decision is made but not acted on twice a day. e.g increase light_target

def write_to_database(measurement=Measurements.light.value, value=0):
    # Ensure string is passed, not enum object since it messes with the database
    if type(measurement) != type(Measurements.light.value):
        print('Use a string by appending .value to the measurement enum')
        return
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(BUCKET, ORG, [f"{measurement} {measurement}={value}"])
    return

def read_last_measurement_database(measurement=Measurements.light.value, timeframe='start: -5d'):
    query = f"from(bucket:\"{BUCKET}\")\
        |> range({timeframe})\
        |> filter(fn: (r) => r._measurement == \"{measurement}\")\
        |> last()"
    return query_influx(query=query)

def read_average_database(measurement=Measurements.light.value, timeframe='start: -1d'):
    # average can be modified by setting timeframe to different values
    query = f"from(bucket:\"{BUCKET}\")\
        |> range({timeframe})\
        |> filter(fn: (r) => r._measurement == \"{measurement}\")\
        |> mean()"
    return query_influx(query=query) 

def read_3_days(measurement=Measurements.decision.value, timeframe='start: -73h'): # last 3 days + 1 hour
    query = f"from(bucket:\"{BUCKET}\")\
        |> range({timeframe})\
        |> filter(fn: (r) => r._measurement == \"{measurement}\")"
    return query_influx(query=query)

def read_update_time(measurement=Measurements.last_update.value, timeframe='start: -3d'): # not sure if timeframe should be more than 3 days
    query = f"from(bucket:\"{BUCKET}\")\
        |> range({timeframe})\
        |> filter(fn: (r) => r._measurement == \"{measurement}\")\
        |> last()"
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    result = client.query_api().query(org=ORG, query=query)
    for table in result:
        for record in table.records:
            utc_time = record.get_time() # utc time

    # Convert the UTC time to Eastern Standard Time (EST)
    est_tz = pytz.timezone('America/New_York') # est doesnt account for daylight savings, but new york does
    est_time = utc_time.astimezone(est_tz)

    # Format the EST time as a string
    est_time_str = est_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return est_time_str

def query_influx(query):
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    result = client.query_api().query(org=ORG, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(record.get_value())
    return results


#write_to_database(measurement=Measurements.moisture.value, value=82) # write sensor data 
#print(read_last_measurement_database(measurement=Measurements.moisture.value)) # read sensor data

#write_to_database(measurement=Measurements.last_update.value, value=0) # create last_update event
#print(read_update_time()) # read time last update occurred

#print(read_24_hrs_average_database(measurement=Measurements.light.value)) # get average of a value over 24 hours

#write_to_database(measurement=Measurements.decision.value, value="\"decreased water threshold\"") # log a decision
#print(read_3_days()) # read all of last 3 day of decicions
