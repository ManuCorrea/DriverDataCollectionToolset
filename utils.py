import cv2 as cv
import numpy as np
import time
import os


def get_files_from_path(path):
    """Returns all files in a path

    Args:
        path (str): desired  path

    Returns:
        list: list of files
    """
    (_, _, filenames) = next(os.walk(path))
    return filenames


def get_directories_from_path(path):
    """Returns all directories in a path

    Args:
        path (str): desired path

    Returns:
        list: list of directories
    """
    (_, directories, _) = next(os.walk(path))
    return directories


print(get_files_from_path('.'))

# https://stackoverflow.com/questions/49567637/the-output-of-cv2-videowriter-is-incorrect-its-faster
def check_frames_per_n_seconds(camera, capture_duration):
    start_time = time.time()
    frameCount = 0
    while(int(time.time() - start_time) < capture_duration):
        # wait for camera to grab next frame
        frame = camera.capture()
        # count number of frames
        frameCount += 1

    print('Total frames: ', frameCount)


def check_frames_per_n_seconds_no_class(capture_duration):
    cap = cv.VideoCapture(0)
    start_time = time.time()
    frameCount = 0
    while(int(time.time() - start_time) < capture_duration):
        # wait for camera to grab next frame
        ret, frame = cap.read()
        # count number of frames
        frameCount += 1

    print('Total frames: ', frameCount)


def count_cameras(max_to_test=4):
    for i in range(max_to_test):
        temp_camera = cv.VideoCapture(i)
        if temp_camera.isOpened():
            temp_camera.release()
            continue
        return i


def numpy_cam_file_reader(file):
    file = np.load(file)
    return file
