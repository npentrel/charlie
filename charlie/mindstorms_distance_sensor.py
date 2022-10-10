from typing import Any, Mapping, Optional
from viam.components.sensor import Sensor
from mindstorms import Hub

import io
import json
import serial

class MindstormsDistanceSensor(Sensor):
    # Subclass the Viam Arm component and implement the required functions
    """
    Sensor represents a physical sensing device that can provide measurement readings.

    This acts as an abstract base cdlass for any drivers representing specific
    sensor implementations. This cannot be used on its own. If the `__init__()` function is
    overridden, it must call the `super().__init__()` function.
    """
    def __init__(self, name: str, port: str):
        self.ser = serial.Serial("/dev/rfcomm0", timeout=1)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
        ports = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5 }
        self.portnum = ports[port]
        super().__init__(name)

    async def get_readings(self, **kwargs) -> Mapping[str, Any]:
        """
        Obtain the measurements/data specific to this sensor.

        Returns:
            Mapping[str, Any]: The measurements. Can be of any type.
        """
        result = 30
        try:
            self.sio.flush()
            readings = json.loads(self.sio.readline())
            print(readings["p"])
            result = readings["p"][self.portnum][1][0]
        except Exception as e:
            print(e)
        return { "distance": result }
