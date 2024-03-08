# This script is useful for uploading sensor data
# and printing out the result

import requests

url = 'https://show-frontend-ro735h6uvq-pd.a.run.app/'
# if testing on locally deployed image, use url = 'http://127.0.0.1:5000/'
data = {"Measurement": "light", "value": 30}
# value can be between 0 - 100
# Measurement can be one of the enums in ../show_pot_metrics_backend_flask/manage_database.py
r = requests.post(url, json=data)

print(r.text)
