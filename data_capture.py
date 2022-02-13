# import sensors
import os
from pathlib import Path
import time
import camera
import sensor
from typing import List

class DataCapture:
    def __init__(self, cameras: List[camera.Camera], camera_save_mode, sensors: List[sensor.Sensor], path, batchs=None) -> None:
        self.cameras = cameras
        self.camera_save_mode = camera_save_mode
        self.sensors = sensors
        self.path = path
        self.batchs = batchs
        
        self.create_folder()

    def capture(self):
        time_entry = int(time.time())
        for _ in range(self.batchs):
            # capture cameras data
            # TODO take into account frames. In many case we do not need big refresh date of a sensor
            for cam in self.cameras:
                if self.camera_save_mode == 'numpy':
                    cam.capture_save_in_buffer()
                elif self.camera_save_mode == 'video':
                    # (not implemented yet)
                    cam.capture_save_in_video()
            
            for sensor in self.sensors:
                sensor.capture()
        # batches finished
        # save camera data
        for cam, cam_path in zip(self.cameras, self.cameras_paths):
            if self.camera_save_mode == 'numpy':
                print(f'Saving camera in path  {cam_path}')
                cam.save_buffer(cam_path, time_entry)

        # save sensor data
        for sensor, sensor_path in zip(self.sensors, self.sensors_paths):
            print(f'Saving sensor in path  {sensor_path}')
            sensor.save(sensor_path, time_entry)
        

    def done(self):
        for cam in self.cameras:
            cam.finish()
    
    def create_folder(self):
        Path(self.path).mkdir(parents=True, exist_ok=True)
        self.path = os.path.join(self.path, str(int(time.time())))
        Path(self.path).mkdir(parents=True, exist_ok=True)
        cameras_path = os.path.join(self.path, "cameras")
        sensors_path = os.path.join(self.path, "sensors")
        Path(cameras_path).mkdir(parents=True, exist_ok=True)
        Path(sensors_path).mkdir(parents=True, exist_ok=True)

        self.cameras_paths = [os.path.join(cameras_path, cam.data_name) for cam in self.cameras]
        self.sensors_paths = [os.path.join(sensors_path, sensor.name) for sensor in self.sensors]

        for cam_folder in self.cameras_paths:
            Path(cam_folder).mkdir(parents=True, exist_ok=True)
        for sensor_folder in self.sensors_paths:
            Path(sensor_folder).mkdir(parents=True, exist_ok=True)
    
