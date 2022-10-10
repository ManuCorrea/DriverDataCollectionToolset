# DriverDataCollectionToolset
This project is intended to build a set of tools for making a capture device for drivers with the possibility of other uses.

## Use
The best way to start is with data_capture_example.py
In that basic example is defined a single camera and a dummy sensor TimeStatus(hour and day). For further information about function and arguments check modules and commented methods.
    python3 data_capture_example.py

The data will be saved in:
```
├── dataset
│   ├── timestamp
│   │   ├── cameras (each children dir is a camera object)
│   │   │   └── cam{id}
│   │   │       ├── cam_batch.npy
│   │   └── sensors (each children dir is a sensor object)
│   │       └── sensor_name
│   │           ├── sensor_batch.npy
```
Over that data the user can read it in structure way. Its intended to develop a class that handles and read this data for the rest of the pipeline.

## Arquitecture
We have different types of Classes:
### Camera
This object is intended to initialize a camera and have easy way of using it and capture its data

### Sensor
A sensor for the pipeline will be everything that adds information to the data capturing and is not image/camera information. A sensor does not need to be a hardware sensor itself.

To implement our own we will need to do it in sensors.py, the methods to implement are the following:
```
class Skeleton(sensor.Sensor):
    def __init__(self, sensor_name=None) -> None:
        super().__init__(sensor_name)

    def initialize(self):
        """
        This function will be used to initialize the sensor if required.
        E.g.: initialize sensor over serial, import required libraries, set up configuration...
        """
        pass

    def get_data(self):
        """
        This function will get the data of the sensor
        """
        pass

    def read_saved_data(self):
        """
        OVERRIDE
        Reads the data and returns it
        Returns:
            # TODO: decide whether or not it must be predefined
            # or choosen by the user
            # If predefined will be better for data visualization part.
        """
        pass

    def read_and_format_saved_data(self):
        """
        Reads and format saved data for use with TF/PyTorch frameworks
        """
        pass
```

These objects will be along the pipeline:
## Pipeline
```
                             Modifies
 Camera objects          ┌─────────────┐
       │                 │             │
       ▼                 │    ┌───Postprocesing
      Data   generates   ▼    │
    Capture ───────────►Data──┼───Visualization
       ▲                      │
       │                      └───Read and format for ML
  Sensor objects
```
The project stills on development but the end goal is to provide a framework that enables and easy data collection, easily reusable with tools that are useful during the development and research.

# TODO
* Data visualization abstraction
* Add other tipes of camera like Depth Cameras
* Data Post Processor:
    * Basic OpenCV postprocessing.
    * Face dots, skeleton, etc with Deep Learning models.
    * Data cleaning and visualization tools.
* Create a general hardware environment sensor for easy community use. Arduino BLE sense is good starting point, easy to add other sensor modules to the already existing onest.
