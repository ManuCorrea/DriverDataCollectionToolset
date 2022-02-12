import numpy as np


class Sensor:
    def __init__(self, sensor_name=None) -> None:
        self.data = []
        if sensor_name is None:
            self.name = type(self).__name__
        else:
            self.name = sensor_name

        print(f"Initializing sensor {self.name}")
        self.initialize()

    def initialize(self):
        """
        OVERRIDE
        This function will be used to initialize the sensor if required.
        E.g.: initialize sensor over serial, import required libraries, set up configuration...
        """
        pass

    def get_data(self):
        """
        OVERRIDE
        This function will get the data of the sensor
        """
        pass

    def capture(self):
        """
        Gets data from the sensor and saves it in the object list.
        """
        self.data.append(self.get_data())

    def save(self, path, time_entry):
        """Saves the data that has been capture into a numpy file.

        Args:
            path (str): Path where the data will be saved
            time_entry (int): time entry that will identify the file
        """
        # print(f"Saving the following data: {self.data}")
        np.save(f"{path}/{self.name}_{time_entry}.npy", np.array(self.data))

    def read_saved_data(self):
        """
        OVERRIDE
        Reads the data and returns it in JSON formated str
        Returns:
            JSON formatted str
        """
        pass

    def read_and_format_saved_data(self):
        """
        OVERRIDE
        Reads and format saved data for use with TF/PyTorch frameworks
        """
        pass
