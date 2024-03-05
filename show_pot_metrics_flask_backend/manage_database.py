from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from enum import Enum

TOKEN = "o8iQsdxsSf1l7lNRAFIfKRdBSvmpzdEHmNeZqy5yrB4StPTcFqhj0_WONmK-UyN-ksGmycGVefWvgjv3GabqjQ==" #todo hide later
URL = "https://us-east-1-1.aws.cloud2.influxdata.com/"
ORG = "f6056c661b1ca7c8" # from url
BUCKET = "second_bucket"

# different types of measurements
class Measurements(Enum): 
    light = 'light' # sufficient hour sof light
    moisture = 'moisture' # sufficient soil moisture
    npk = 'npk' # soil quality
    ml = 'ml' # ratio of healthy leaves detected
    nominal_light = 'nominal_light' # how much light we think is ideal 
    nominal_water = 'nominal_moisture' # how much water we think is ideal


class DatabaseInterface:
    def __init__(self, token=TOKEN, url=URL, org=ORG, bucket=BUCKET):
        self.token = token
        self.url = url 
        self.org = org
        self.bucket = bucket
        self.client = InfluxDBClient(url=url, token=token, org=org)
    
    def send_data(self, measurement=Measurements.light, value=0):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        write_api.write(self.bucket, "my-org", [f"{measurement} {measurement}={value}"])
        return
    
    def read_data(self, measurement=Measurements.light, timeframe="start: -30d", additional_args=""):
        query = f"from(bucket:\"{self.bucket}\")\
        |> range({timeframe})\
        |> filter(fn: (r) => r._measurement == \"{measurement}\")\
        {additional_args}"
        result = self.client.query_api().query(org=self.org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_value(), record.get_field()))
        # print(results)
        return results
    
    def populate_with_dummy_data(self):
        db_interface = DatabaseInterface()
        data = [50,40,10,90,55,30]
        for i, measure in enumerate(Measurements):
            db_interface.send_data(measurement=measure, value=data[i])
        return


def test(): # example code
    db_interface = DatabaseInterface()
    db_interface.send_data(measurement=Measurements.light)
    db_interface.read_data(measurement=Measurements.light)
    return

