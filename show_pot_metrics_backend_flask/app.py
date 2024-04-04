from flask import Flask, jsonify, make_response, send_from_directory, url_for
from flask_cors import CORS
from manage_database import Measurements, write_to_database, read_last_measurement_database, populate_with_dummy_data
from datetime import datetime
import os

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
        # get decision
        # get water, light percentage values?? optional for now

        #todays_data["image_url"] = get_image_url(day=day)
        image_name = get_image_name(day=day)
        todays_data["image_url"] = url_for('get_image', image_name=image_name, _external=True)
        todays_data["decision"] = get_decision(day=day)
        # increment seconds passed?
        data[day] = todays_data # dict of dicts
    print(data)
    return "ok" # data \

@app.route('/images/<image_name>') 
def get_image(image_name): # thefrontend will use this url for each pic
    return send_from_directory('images', image_name)


def get_decision(day):
    # idk how to 

    # first check my expected 


    return 0

def match_int_to_decision(decision_int):

    return

def get_image_name(day):
    match day:
        case 0: 
            return 'basil_23_03_2024_21 (1).jpg'
        case 1:
            return 'basil_22_03_2024_23.jpg'
        case 2: 
            return 'basil_14_03_2024_08.jpg'
    return ''

if __name__ == "__main__":
    app.run(debug=True)