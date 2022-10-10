import cv2 as cv
import numpy as np
import time


class Camera:
    def __init__(self, cam_id, capture=False, saving_mode=None, data_name=None) -> None:
        """Camera class intented to initialize a camera

        Args:
            cam_id (int): ID of camera for OpenCV
            capture (bool, optional): Variable to tell if we are capturing with the object or not. Defaults to False.
            saving_mode (str, optional):
                * numpy -> save stream as numpy data
                * video -> save video of the recording
            data_name (str, optional): Name of the file that will be saved. Defaults to None.
        """

        self.cap = cv.VideoCapture(cam_id)
        self.saving_mode = saving_mode
        self.data_name = data_name

        self.width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.heigh = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        if capture:
            if saving_mode is None:
                print("Need to specify saving mode!")
            if data_name is None:
                print("Need to specify numpy file/video name!")
            if saving_mode == 'numpy':
                self.buffer = []
            elif saving_mode == 'video':
                pass

        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()

    def capture(self):
        """Reads from camera a frame

        Returns:
            numpy.ndarray: frame either grayscale or BGR
        """
        ret, frame = self.cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?).")
            exit()
        return frame

    def capture_save_in_buffer(self):
        """
        Takes a capture from the camera and save it into object's buffer
        """
        frame = self.capture()
        print(type(frame))
        self.buffer.append(frame)
        return frame

    def capture_save_in_video(self):
        # TODO implement
        pass

    def save_buffer(self, path, time_entry):
        """Saves and deletes object buffer

        Args:
            path (str): Desired parent path for saving the data
            time_entry (int): It will identify the numpy file
        """
        # start = time.time()
        np.save(f"{path}/{self.data_name}_{time_entry}.npy", np.array(self.buffer))
        # print(f'Save: {time.time() - start} seconds')
        # start = time.time()
        # np.savez_compressed(f"{path}/cameras/{self.data_name}_{time_entry}.npy",
        #         np.array(self.buffer))
        # print(f'Compressed: {time.time() - start} seconds')
        self.buffer = []

    def finish(self):
        """
        Free up camera resources
        """
        self.cap.release()

    def set_video(self):
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter(f'{self.data_name}.avi', fourcc, 20.0, (640, 480))

    def set_resolution(self, width, height):
        """Sets camera resolution

        Args:
            width (int)
            height (int)
        """
        self.width = self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.heigh = self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
