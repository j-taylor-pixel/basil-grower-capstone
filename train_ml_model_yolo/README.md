# Plant Health Detection
## About
Trained model to identify healthy and unhealthy basil plants.

This is built as a component of my [Fourth Year Capstone Project](https://smartplantpot0.wordpress.com/). 
My FYDP aims to combine machine learning, and sensor feedback to control water and artificial light supplied to a basil plant to provide perfect growing conditions completely autonomously. 
The ML model will identify the basil plant's healthy and determine how its water and artifical light inputs should be altered. 

## Built with

[YOLOv8 CLI](https://docs.ultralytics.com/quickstart/#conda-docker-image)

Roboflow for dataset creation

## Install Guide
Install requirements

`pip install -r requirements.txt`

Python 3.10.8 was used

## Use Guide
Create a tagged dataset on [roboflow](https://blog.roboflow.com/how-to-train-yolov8-on-a-custom-dataset/)

Download the dataset to the project folder
`python downloadData.py`

In `data.yaml`, replace `test`, `train`, and `val` fields with absolute file paths.
By default, the fields have relative paths, but these are problematic and cause errors.

Train the model using the YOLO CLI:

`yolo task=detect \
mode=train \
model=yolov8s.pt \
data=/workspaces/plant_health_detection/Yolo/datasets/Basil-Helath-2/data.yaml \
epochs=100 \
imgsz=640
`

Validate the model using the YOLO CLI:

`yolo task=detect \
mode=val \
model=/workspaces/plant_health_detection/runs/detect/train8/weights/best.pt \
data=/workspaces/plant_health_detection/Yolo/datasets/Basil-Helath-2/data.yaml \
`

Predict using the trained and validated model:
`
yolo task=detect \
mode=predict \
model=/workspaces/plant_health_detection/runs/detect/train8/weights/best.pt \
conf=0.25 \
source=/workspaces/plant_health_detection/Yolo/datasets/Basil-Helath-2/test/images
`

## Results
Below shows the trained model correctly identifying a healhty basil plant.

![Image](runs/detect/predict2/healthy_5_jpg.rf.5e23842b316cf77c2c56cc6dfd7bff0f.jpg)

## Future Work
The end goal is the model will be able to identify different conditions of basil, such as underwatering, overwatering, too much sunlight and too little sunlight. 
This requires a larger and more detailed dataset.
