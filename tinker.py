import cv2 as cv
import numpy as np
import time
from camera import Camera
from utils import *
import sensors

# print(count_cameras())

# camera = Camera(0, capture=True, saving_mode='numpy', data_name='test')
# print(camera.width)
# print(camera.heigh)
# camera.set_resolution(1280, 720)

# print(check_frames_per_n_seconds_no_class(10))
# print(check_frames_per_n_seconds(camera, 10)) # 121/10

time_sensor = sensors.TimeStatus()

time_sensor.capture()
time_sensor.save('data', 1)

for _ in range(10):
    time_sensor.capture()
time_sensor.save('data', 2)

print(time_sensor.read_saved_data('data'))


# while True:
#     frame = camera.capture_save_in_buffer()
#     # print(f"############# {frame}")
#     cv.imshow('frame', frame)
#     if cv.waitKey(1) == ord('q'):
#         break
# camera.save_buffer()
# # When everything done, release the capture
# camera.finish()
# cv.destroyAllWindows()

# captured = numpy_cam_file_reader("test_1642803207.5125124.npy")
# for img in captured:
#     cv.imshow('frame', img)
#     if cv.waitKey(20) == ord('q'):
#         break
