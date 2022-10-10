from typing import Any, Dict, Optional
from viam.components.motor import Motor
# from viam.operations import run_with_operation
from mindstorms import Hub

import time

class NotSupportedError(Exception):
    pass

class MindstormsMotor(Motor):
    # Subclass the Viam Arm component and implement the required functions

    def __init__(self, name: str, portname: str):
        # Starting position
        self.hub = Hub("/dev/rfcomm0")
        self.properties = Motor.Properties(position_reporting=False)
        self.portname = portname

        time.sleep(3) # wait for hub to initialize
        getattr(self.hub.port, portname).motor.mode(2) # preset 0 position to absolute zero position
        self.preset = getattr(self.hub.port, portname).motor.get()[0]
        getattr(self.hub.port, portname).motor.preset(self.preset) # preset 0 position to absolute zero position
        super().__init__(name)

    async def set_power(self, power: float, extra: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Sets the "percentage" of power the motor should employ between -1 and 1.
        When `power` is negative, the rotation will be in the backward direction.

        Args:
            power (float): Power between -1 and 1
                (negative implies backwards).
        """
        getattr(self.hub.port, self.portname).motor.pwm(power*100)

    # @run_with_operation
    async def go_for(self, rpm: float, revolutions: float, extra: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Spin the motor the specified number of `revolutions` at specified `rpm`.
        When `rpm` or `revolutions` is a negative value, the rotation will be in the backward direction.
        Note: if both `rpm` and `revolutions` are negative, the motor will spin in the forward direction.

        Args:
            rpm (float): Speed at which the motor should move in rotations per minute
                (negative implies backwards).
                Max: 160 rpm - converts to 100%
            revolutions (float): Number of revolutions the motor should run for
                (negative implies backwards).
        """
        speed_percent = rpm/160
        getattr(self.hub.port, self.portname).motor.run_for_degrees(360*revolutions,speed=speed_percent*100)

    # @run_with_operation
    async def go_to(self, rpm: float, position_revolutions: float, extra: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Spin the motor to the specified position (provided in revolutions from home/zero),
        at the specified speed, in revolutions per minute.
        Regardless of the directionality of the `rpm` this function will move
        the motor towards the specified position.

        Args:
            rpm (float): Speed at which the motor should rotate (absolute value).
                Max: 160 rpm - converts to 100%
            position_revolutions (float): Target position relative to home/zero, in revolutions.
        """
        speed_percent = rpm/160
        getattr(self.hub.port, self.portname).motor.run_to_position(position_revolutions*360, speed_percent*100)

    async def reset_zero_position(self, offset: float, extra: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Set the current position (modified by `offset`) to be the new zero (home) position.

        Args:
            offset (float): The offset from the current position to new home/zero position.
        """
        self.preset = getattr(self.hub.port, self.portname).motor.get()[0] + int(offset)
        getattr(self.hub.port, self.portname).motor.preset(self.preset)


    async def get_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> float:
        """
        Report the position of the motor based on its encoder.
        The value returned is the number of revolutions relative to its zero position.
        This method will raise an exception if position reporting is not supported by the motor.

        Returns:
            float: Number of revolutions the motor is away from zero/home.
        """
        return getattr(self.hub.port, self.portname).motor.get()[0]


    async def get_properties(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Motor.Properties:
        """
        Report a dictionary mapping optional properties to
        whether it is supported by this motor.

        Returns:
            Properties: Map of feature names to supported status.
        """
        return self.position_reporting


    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Stop the motor immediately, without any gradual step down.
        """
        getattr(self.hub.port, self.portname).motor.brake()


    async def is_powered(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> bool:
        """
        Returns whether or not the motor is currently running.

        Returns:
            bool: Indicates whether the motor is currently powered.
        """
        raise NotSupportedError(f"Motor named {self.name} does not support returning whether it is powered")


    async def is_moving(self) -> bool:
        """
        Get if the motor is currently moving.

        Returns:
            bool: Whether the motor is moving.
        """
        raise NotSupportedError(f"Motor named {self.name} does not support returning whether it is moving")

