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
        ret, frame = self.cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?).")
            exit()
        return frame

    def capture_save_in_buffer(self):
        frame = self.capture()
        self.buffer.append(frame)
        return frame

    def capture_save_in_video(self):
        pass

    def save_buffer(self):
        np.save(f"{self.data_name}_{time.time()}.npy", np.array(self.buffer))
        self.buffer = []

    def finish(self):
        self.cap.release()

    def set_video(self):
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter(f'{self.data_name}.avi', fourcc, 20.0, (640, 480))

    def set_resolution(self, width, height):
        self.width = self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.heigh = self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
