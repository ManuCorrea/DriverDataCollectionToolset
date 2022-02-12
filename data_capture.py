# import sensors
import os
from pathlib import Path
import time
import camera
import sensor
from typing import List
# Objecto generate al que le pasamos array de sensores
# array de camaras
# intervalo de captura
# duración
# usar threads para los sensores?

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
        for cam in self.cameras:
            if self.camera_save_mode == 'numpy':
                print(f'Saving camera in path  {self.path}')
                cam.save_buffer(self.path, time_entry)

        # save sensor data
        for sensor in self.sensors:
            print(f'Saving sensor in path  {self.path}')
            sensor.save(self.path, time_entry)
        

    def done(self):
        for cam in self.cameras:
            cam.finish()
    
    def create_folder(self):
        Path(self.path).mkdir(parents=True, exist_ok=True)
        self.path = os.path.join(self.path, str(int(time.time())))
        Path(self.path).mkdir(parents=True, exist_ok=True)
    
