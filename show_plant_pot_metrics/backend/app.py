from flask import Flask
from manage_database import DatabaseInterface, Measurements

app = Flask(__name__)

@app.route('/')
def display_metrics():
    # read database and display as txt for now
    db_interface = DatabaseInterface()
    measurements = []
    measure_dict = {}
    for measurement in Measurements:
        measurements.append(db_interface.read_data(measurement=measurement, additional_args="|> last()"))
        # dict for json
        measure_dict[str(measurement)] = db_interface.read_data(measurement=measurement, additional_args="|> last()")[0][0]
    print(measure_dict)
    return measure_dict


if __name__ == "__main__":
    app.run(debug=True)