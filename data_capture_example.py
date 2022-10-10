import sensors
from camera import Camera

from data_capture import DataCapture

camera = Camera(0, capture=True, saving_mode='numpy', data_name='cam1')
cameras_list = [camera]
sensors_list = [sensors.TimeStatus(sensor_name='time')]#,
                # sensors.ArduinoSense()]
capture = DataCapture(cameras=cameras_list, camera_save_mode="numpy",
                      sensors=sensors_list, path='dataset', batchs=50) #,
                    #   sensors_refresh_rate=[2, 2])

for _ in range(10):
    capture.capture()

capture.done()
