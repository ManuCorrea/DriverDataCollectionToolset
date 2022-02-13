# Intended to see the data captured by data_capture.py
import cv2
import os
from utils import numpy_file_reader, get_directories_from_path, get_files_from_path

import sensors

timeframe = 0
DATA_PATH = 'dataset/' + timeframe
time_status_sensor = sensors.TimeStatus()


cameras_path = os.path.join(DATA_PATH, 'cameras')
sensors_path = os.path.join(DATA_PATH, 'sensors')

# get the different names of the cameras
cameras = get_directories_from_path(cameras_path)
# get the different names of the sensors
sensors = get_directories_from_path(sensors_path)

print(f'Cameras found {cameras}')
print(f'Sensors found {sensors}')

for cam_name, sensor_name in zip(cameras, sensors):
    cam_path = os.path.join(
        cameras_path, cam_name)
    sensor_path = os.path.join(
        sensors_path, sensor_name)
    data_records_camera = get_files_from_path(cam_path)
    data_records_sensor = get_files_from_path(sensor_path)
    
    sensor_data = time_status_sensor.read_saved_data(sensor_path)

    idx = 0
    # print(sensor_data)
    # print('\n')
    # print(sensor_data)
    # print('\n')
    data_records_camera.sort()
    for cam_data_file in data_records_camera:
        print(f"reading {cam_data_file}")
        cam_data = numpy_file_reader(os.path.join(cam_path, cam_data_file))
        for img in cam_data:
            # print(sensor)
            # print(type(sensor))
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(
                sensor_data['time'][idx]), (10, 500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Visualization', img)
            if cv2.waitKey(20) == ord('q'):
                break
            idx += 1

# para mostrar todas imagenes a la vez se tendria que meter en un solo array cada captura de cada camara
