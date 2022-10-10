# charlie/python_server.py

import sys
import asyncio
import logging
from viam.rpc.server import Server

import time
import subprocess
from mindstorms_motor import MindstormsMotor
from mindstorms_distance_sensor import MindstormsDistanceSensor

def hacks():
    ## HACKY STUFF
    ## Something with rshell isn't working as expected. If I try to open the hub connection without connecting to rshell from the terminal beforehand, charlie just shuts down.
    ## So we ensure we connect to charlie with rshell first, wait 10 seconds and then kill that process.
    print("starting rshell")
    rshell = subprocess.Popen(["rshell", "-p", "/dev/rfcomm0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    time.sleep(20)
    rshell.kill()
    print("killed rshell")


async def run(host: str, port: int, log_level: int):
    server = Server(
        components=[
            MindstormsMotor('motor-a', "A"),
            MindstormsMotor('motor-b', "B"),
            MindstormsDistanceSensor('distance-sensor', "C"),
            MindstormsMotor('motor-e', "E"),
            MindstormsMotor('motor-f', "F")]
    )
    await server.serve(host=host, port=port, log_level=log_level)

if __name__ == "__main__":
    print("hello!")
    hacks()
    host = "localhost"
    port = 9090
    log_level = logging.DEBUG
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        level = sys.argv[3]
        if level.lower() == "q" or level.lower() == "quiet":
            log_level = logging.FATAL
    except (IndexError, ValueError):
        pass
    asyncio.run(run(host, port, log_level))
