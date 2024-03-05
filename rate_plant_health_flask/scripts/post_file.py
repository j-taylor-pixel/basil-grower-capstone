# This script is useful for uploading a select photo of basil, 
# then waiting for its the flask app to run image recognition,
# and printing out the resulting leaf types identified.

import requests

url = 'https://rate-app-image-ro735h6uvq-pd.a.run.app/upload/'
# if testing on locally deployed image, use url = 'http://127.0.0.1:5000/upload/'

with open('test_full.jpg', 'rb') as f:
    r = requests.post(url, files={'file': f})

print(r.text)
