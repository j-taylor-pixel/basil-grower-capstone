# This script should be used on a raspberry pi,
# with a picamera module3 attached. 
# the script  takes a photo when called, and saves a test_full
# the photo is 16 x 9, 4k resolution
# which will be downscaled by the ml model@

import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_preview_configuration()
#capture_config = picam2.create_still_configuration(main={"size": (640, 640)},)
capture_config = picam2.create_still_configuration()
picam2.configure(preview_config)

picam2.start()
time.sleep(2)

picam2.switch_mode_and_capture_file(capture_config, "test_full.jpg")


