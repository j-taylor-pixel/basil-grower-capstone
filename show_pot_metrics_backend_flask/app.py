from flask import Flask, jsonify, make_response
from flask_cors import CORS
from manage_database import Measurements, write_to_database, read_last_measurement_database, populate_with_dummy_data
import random
from datetime import datetime


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def display_metrics():
    # read database and display as txt. This will be invoked by frontend
    sensor_readings = {} # dict for json
    leaf_health = read_last_measurement_database(measurement=Measurements.leaf_health.value)[0] * 100
    temp = read_last_measurement_database(measurement=Measurements.temperature.value)[0] # send in celcius
    light = read_last_measurement_database(measurement=Measurements.light.value)[0] / read_last_measurement_database(Measurements.light_threshold.value)[0] * 100
    light = min(light, 120) # cap 
    moisture_thresh = read_last_measurement_database(Measurements.moisture_threshhold.value)[0]
    moist_cur = read_last_measurement_database(measurement=Measurements.moisture.value)[0] 
    moisture = moisture_thresh / moist_cur * 100
    moisture = min(moisture, 120) # cap

    sensor_readings[str(Measurements.leaf_health.value)] = leaf_health
    sensor_readings[str(Measurements.temperature.value)] = temp
    sensor_readings[str(Measurements.light.value)] = light
    sensor_readings[str(Measurements.moisture.value)] =  moisture
    sensor_readings['max_temp'] = 26 # 26-32 is ideal # configure max temp on backend
    sensor_readings_int = {key: int(value) for key, value in sensor_readings.items()} # round to int

    resp = make_response(jsonify(sensor_readings_int))
    resp.headers['Cache-Control'] = 'no-cache'
    resp.headers['Connection'] = 'close'
    return resp


@app.route('/temp/', methods=['GET'])
def temp_metrics():
    # read database and display as txt. This will be invoked by frontend
    sensor_readings = {} # dict for json
    sensor_readings[str(Measurements.leaf_health.value)] = 82
    sensor_readings[str(Measurements.temperature.value)] = read_last_measurement_database(measurement=Measurements.temperature.value)[0] / 0.30 # ideal temp for basil is 30c
    light_measurement = read_last_measurement_database(measurement=Measurements.light.value)[0] / read_last_measurement_database(Measurements.light_threshold.value)[0] * 100
    sensor_readings[str(Measurements.light.value)] = 96 # cap at 150

    moist_threshold = read_last_measurement_database(Measurements.moisture_threshhold.value)[0]
    moist_value = read_last_measurement_database(measurement=Measurements.moisture.value)[0]
    sensor_readings[str(Measurements.moisture.value)] = 104
    sensor_readings_int = {key: int(value) for key, value in sensor_readings.items()} # round to int

    resp = make_response(jsonify(sensor_readings_int))
    resp.headers['Cache-Control'] = 'no-cache'
    resp.headers['Connection'] = 'close'
    return resp

#@app.route('/populate/')
#def populate_random_values():
#    data = [random.randint(0, 100) for _ in range(len(Measurements))]
#    populate_with_dummy_data(data=data)
#    return f"Randomly changed values to {data}"

@app.route('/demo/')
@app.route('/demo/<int:number_of_days>')
def demo_page(number_of_days=2):
    print(f'Demo Page for {number_of_days} days')
    data = {}
    for day in range(number_of_days): # day 0 can be today, day 1 can be 1 day ago
        print(day) # 0, 1
        todays_data = {}
        now = datetime.now()
        # Calculate the number of seconds passed today
        seconds_passed_today = int((now - datetime(now.year, now.month, now.day)).total_seconds())


        data[day] = todays_data # append to data
    print(data)
    return "ok" # data 

if __name__ == "__main__":
    app.run(debug=True)