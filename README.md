# DriverDataCollectionToolset
The intended to build a set of tools for making a capture device for drivers with the possibility of other uses.

# Objective
Providing a framework in which there is a whole data worflow, with standarized components. Making easy its expansion, reuse of existing tools and help in the process of data recolection and after use.

User implemented sensors should include methods for transforming the data in 1/human readable way, 2/ready to be feeded into any ML framework. This should lead for an easier way to use the different sensors and tools by other people.

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
A sensor for the pipeline will be everything that adds information to the data capturing and is not image/camera information. A sensor does not need to be a hardware sensor itself, for example current time can be consider a sensor.

To implement our own we will need to do it in sensors.py (which already has some examples), the methods to implement are the following:
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

### Datacapture
Datacapture class gets all the provided camera and sensors information. Check data_capture_example.py for use.

It uses the common defined methos for camera and sensor type, in the standarization relies the automation.

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

# Examples
This program can run in a laptop with an Arduino attatched to it. The ideal way to run it would be on a small computer (like SBC as RaspberryPi) in a way that doesn't interfere with the driver.

# TODO and improvements
* Create a more abstract and general data visualization module in a way that fits the rests of the pipeline. With options to plot, compare, show videos, give insights, etc
* Add other tipes of camera like Depth Cameras (e.g: Intel RealSense)
* Data Post Processor, adding common tools that could be use by the rest of the community, e.g:
    * Basic OpenCV postprocessing.
    * Face dots, skeleton, etc with Deep Learning models.
    * Data cleaning and visualization tools.
* Create a general hardware environment sensor for easy community use. Arduino BLE sense is good starting point, easy to add other sensor modules to the already existing onest.
* Car information, CAN sensor integration whcih would provide accurate vehicle speed, signals, rpm, etc...
* Driver information, that can be implemented as a sensor in the pipeline. That could be achieve in a non invasive way with a fitness wrist band, being able to take pulse, temperature, etc
