from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from enum import Enum

TOKEN = "o8iQsdxsSf1l7lNRAFIfKRdBSvmpzdEHmNeZqy5yrB4StPTcFqhj0_WONmK-UyN-ksGmycGVefWvgjv3GabqjQ==" #todo hide later
URL = "https://us-east-1-1.aws.cloud2.influxdata.com/"
ORG = "f6056c661b1ca7c8" # from url
BUCKET = "production"

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
    # Image storage
    image_untagged = 'image_untagged'
    image_tagged = 'image_tagged'

def write_to_database(measurement=Measurements.light.value, value=0):
    # Ensure string is passed, not enum object since it messes with the database
    if type(measurement) != type(Measurements.light.value):
        print('Use a string by appending .value to the measurement enum')
        return
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(BUCKET, ORG, [f"{measurement} {measurement}={value}"])
    return

def read_last_measurement_database(measurement=Measurements.light.value, timeframe='start: -10d'):
    query = f"from(bucket:\"{BUCKET}\")\
        |> range({timeframe})\
        |> filter(fn: (r) => r._measurement == \"{measurement}\")\
        |> last()"
    return query_influx(query=query)

def query_influx(query):
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    result = client.query_api().query(org=ORG, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(record.get_value())
    return results
    
def populate_with_dummy_data(data = [50,40,10,90,55,30, 20, 55, 80, 90]):
    for i, measure in enumerate(Measurements):
        write_to_database(measurement=measure.value, value=data[i])
    return
#populate_with_dummy_data()