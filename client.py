import asyncio
import time
from viam import logging
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.motor import Motor
from viam.components.sensor import Sensor

from secrets import ADDRESS_SECRET, PAYLOAD_SECRET

async def connect():

    creds = Credentials(
        type='robot-location-secret',
        payload=PAYLOAD_SECRET)
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address(ADDRESS_SECRET, opts)

async def move_forward_slowly (rotations, rwheel, lwheel):
    await rwheel.go_for(-30, rotations)
    await lwheel.go_for(30, rotations)

async def stop_all(rwheel, lwheel):
    await rwheel.stop()
    await lwheel.stop()

async def hello(arm):
    await arm.go_to(80, 1/6)
    time.sleep(0.25)
    await arm.go_to(80, 0)
    time.sleep(0.25)
    await arm.go_to(80, 1/6)
    time.sleep(0.25)
    await arm.go_to(80, 0)
    time.sleep(0.25)


async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    rwheel = Motor.from_robot(robot, 'charlie:motor-a')
    larm = Motor.from_robot(robot, 'charlie:motor-b')
    # dsensor = Sensor.from_robot(robot, 'charlie:distance-sensor')
    rarm = Motor.from_robot(robot, 'charlie:motor-f')
    lwheel = Motor.from_robot(robot, 'charlie:motor-e')

    await move_forward_slowly(2, rwheel, lwheel)
    time.sleep(2)
    await hello(larm)

    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())