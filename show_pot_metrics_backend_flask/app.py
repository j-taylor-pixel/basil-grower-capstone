from flask import Flask, jsonify, make_response
from flask_cors import CORS
from manage_database import Measurements, write_to_database, read_last_measurement_database, populate_with_dummy_data
import random


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def display_metrics():
    # read database and display as txt. This will be invoked by frontend
    sensor_readings = {} # dict for json
    for measurement in Measurements:
        sensor_readings[str(measurement.value)] = read_last_measurement_database(measurement=measurement.value)[0]
    resp = make_response(jsonify(sensor_readings))
    resp.headers['Cache-Control'] = 'no-cache'
    return resp

@app.route('/populate/')
def populate_random_values():
    data = [random.randint(0, 100) for _ in range(len(Measurements))]
    populate_with_dummy_data(data=data)
    return f"Randomly changed values to {data}"

@app.route('/demo/', methods=['GET'])
def demo_page():
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)