from flask import Flask, request
from flask_cors import CORS
from manage_database import DatabaseInterface, Measurements

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def display_metrics():
    if request.method == 'GET':
        # read database and display as txt for now
        db_interface = DatabaseInterface()
        measurements = []
        measure_dict = {}
        for measurement in Measurements:
            measurements.append(db_interface.read_data(measurement=measurement, additional_args="|> last()"))
            # dict for json
            measure_dict[str(measurement)] = db_interface.read_data(measurement=measurement, additional_args="|> last()")[0][0]
        return measure_dict
    # POST
    data = request.get_json()
    matched_measurement = matching_enum(data=data)
    db_interface = DatabaseInterface()
    db_interface.send_data(measurement=matched_measurement, value=data["value"])
    return "200 OK"

def matching_enum(data): # matches a string to its relevant enum
    measurement_value = data["Measurement"]
    matching_measurement = None
    for measurement in Measurements:
        if measurement.value == measurement_value:
            matching_measurement = measurement
            break

    return matching_measurement

@app.rout('/demo/', methods=['GET'])
def demo_page():
    

    return "ok"



if __name__ == "__main__":
    app.run(debug=True)