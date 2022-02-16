# import sensors
import os
from pathlib import Path
import time
import camera
import sensor
from typing import List


class DataCapture:
    def __init__(self, cameras: List[camera.Camera], camera_save_mode, sensors: List[sensor.Sensor], path, batchs=1, frames_per_sensor_capture=1, sensors_refresh_rate=None) -> None:
        """This class will provide easy capture of the given camera/s and sensor/s.

        Args:
            cameras (List[camera.Camera]): list of the desired camera objects to capture
            camera_save_mode (str): numpy or video
            sensors (List[sensor.Sensor]): list of the desired sensor objects to capture
            path (str): path where the data will be saved
            batchs (int, optional): Defines the number of camera captures per numpy file. Defaults to 1.
            frames_per_sensor_capture (int, optional): Defines the number of captured frames per sensor capture. Defaults to 1.
            sensors_refresh_rate (List[int], optional): It will give the refresh rate of each sensor given in sensors arg,
                                                        must be same size and the time will be defined in the same order. Defaults to None.
        """
        self.cameras = cameras
        self.camera_save_mode = camera_save_mode
        self.sensors = sensors
        self.path = path
        self.batchs = batchs

        self.frames_per_sensor_capture = frames_per_sensor_capture

        if sensors_refresh_rate is not None:
            self.capture = self.capture_with_refresh_rate
            self.sensors_refresh_rate = sensors_refresh_rate
            self.elapsed = [time.time()] * len(sensors)
        else:
            self.capture = self.capture_with_frame_rate

        self.create_folder()

    def capture_with_frame_rate(self):
        """
        This method will capture the data when no refresh rate is provided.
        It will capture n (frames_per_sensor_capture) frames per sensor capture
        """
        time_entry = int(time.time())
        for _ in range(self.batchs):
            # capture cameras data
            for _ in range(self.frames_per_sensor_capture):
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

    def capture_with_refresh_rate(self):
        """
        This method will capture the sensors according the refresh rate provided to each sensor
        """
        time_entry = int(time.time())

        for _ in range(self.batchs):
            # capture cameras data
            for cam in self.cameras:
                if self.camera_save_mode == 'numpy':
                    cam.capture_save_in_buffer()
                elif self.camera_save_mode == 'video':
                    # (not implemented yet)
                    cam.capture_save_in_video()

            for idx, sensor in enumerate(self.sensors):
                captured = 'Sensors captured: '
                # print(f'{time.time()} - {self.elapsed[idx]}')
                sensor_elapsed_time = time.time() - self.elapsed[idx]
                print(f'elapsed: {sensor_elapsed_time}')
                if sensor_elapsed_time > self.sensors_refresh_rate[idx]:
                    captured += str(idx) + ' '
                    self.elapsed[idx] = time.time()
                    sensor.capture()
            print(captured)

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
        """
        call when finished
        """
        for cam in self.cameras:
            cam.finish()

    def create_folder(self):
        """
        Creates the necesaries directories for saving the different data and its numpy files.
        """
        Path(self.path).mkdir(parents=True, exist_ok=True)
        self.path = os.path.join(self.path, str(int(time.time())))
        Path(self.path).mkdir(parents=True, exist_ok=True)
        cameras_path = os.path.join(self.path, "cameras")
        sensors_path = os.path.join(self.path, "sensors")
        Path(cameras_path).mkdir(parents=True, exist_ok=True)
        Path(sensors_path).mkdir(parents=True, exist_ok=True)

        self.cameras_paths = [os.path.join(
            cameras_path, cam.data_name) for cam in self.cameras]
        self.sensors_paths = [os.path.join(
            sensors_path, sensor.name) for sensor in self.sensors]

        for cam_folder in self.cameras_paths:
            Path(cam_folder).mkdir(parents=True, exist_ok=True)
        for sensor_folder in self.sensors_paths:
            Path(sensor_folder).mkdir(parents=True, exist_ok=True)
