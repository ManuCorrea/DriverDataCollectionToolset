import sensor
import json
import numpy as np
from utils import get_files_from_path
import os

"""
Use me as a template for your sensor!
"""
class Skeleton(sensor.Sensor):
    def __init__(self, sensor_name=None) -> None:
        super().__init__(sensor_name)

    def initialize(self):
        pass

    def get_data(self):
        pass

    def read_saved_data(self):
        pass

    def read_and_format_saved_data(self):
        pass


class TimeStatus(sensor.Sensor):
    def __init__(self, sensor_name=None) -> None:
        super().__init__(sensor_name)
        self.day_name = {0: 'Monday',
                         1: 'Tuesday',
                         2: 'Wednesday',
                         3: 'Thursday',
                         4: 'Friday',
                         5: 'Saturday',
                         6: 'Sunday'}

    def initialize(self):
        from datetime import datetime
        self.datetime = datetime

    def get_data(self):
        now = self.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        day = self.datetime.today().weekday()
        results = [current_time, day]
        # print(f"Results {results}")
        # self.data.append(results)
        return results

    def read_saved_data(self, path):
        data = {"time": [],
                "day": []
                }
        for recording in get_files_from_path(path):
            print(f"Taking recording {recording}")
            # as data:
            read_data = np.load(os.path.join(
                path, recording), allow_pickle=True)
            print(read_data)
            for time, day in read_data:
                print(time)
                print(day)
                print(type(time))
                print(type(day))
                data['time'].append(time)
                data['day'].append(day)

        return json.dumps(data)

    def read_and_format_saved_data(self, path):
        pass