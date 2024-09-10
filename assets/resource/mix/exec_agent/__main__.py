from typing import Tuple
from maa.context import SyncContext

# python -m pip install maafw
from maa.define import RectType
from maa.resource import Resource
from maa.controller import AdbController
from maa.instance import Instance
from maa.toolkit import Toolkit

from maa.custom_recognizer import CustomRecognizer
from maa.custom_action import CustomAction

import asyncio
import subprocess
import os

def send_adb_command(command):
    subprocess.run(f"adb shell su -c {command}", shell=True)

async def main():
    user_path = "./"
    Toolkit.init_option(user_path)

    resource = Resource()
    await resource.load("assets/resource/mix")

    device_list = await Toolkit.adb_devices()
    if not device_list:
        print("No ADB device found.")
        input("Press any key to continue...")
        exit()

    # for demo, we just use the first device
    device = device_list[0]
    print(device.address)
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
    )
    await controller.connect()

    maa_inst = Instance()
    maa_inst.bind(resource, controller)

    if not maa_inst.inited:
        print("Failed to init MAA.")
        input("Press any key to continue...")
        exit()

    print("Waiting task...")
    maa_inst.register_action("FightStart", fight_start)
    maa_inst.register_action("FightEnd", fight_end)
    while 1:
        await maa_inst.run_task("test")
        # await maa_inst.run_task("inFight")
        # await maa_inst.run_task("outFight")

class FightStart(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("run FightStart...")
        commands = [
            "su -c sendevent /dev/input/event5 3 47 0",
            "su -c sendevent /dev/input/event5 3 57 1",
            "su -c sendevent /dev/input/event5 1 330 1",
            "su -c sendevent /dev/input/event5 1 325 1",
            "su -c sendevent /dev/input/event5 3 53 240",
            "su -c sendevent /dev/input/event5 3 54 825",
            "su -c sendevent /dev/input/event5 0 0 0",
            "su -c sendevent /dev/input/event5 3 47 1",
            "su -c sendevent /dev/input/event5 3 57 2",
            "su -c sendevent /dev/input/event5 3 53 112",
            "su -c sendevent /dev/input/event5 3 54 1728",
            "su -c sendevent /dev/input/event5 0 0 0",
        ]

        for command in commands:
            send_adb_command(command)

        return True
    
    def stop(self) -> None:
        pass

class FightEnd(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("run FightSEnding...")
        commands = [
            "su -c sendevent /dev/input/event5 3 47 0",
            "su -c sendevent /dev/input/event5 3 57 -1",
            "su -c sendevent /dev/input/event5 0 0 0",
            "su -c sendevent /dev/input/event5 3 47 1",
            "su -c sendevent /dev/input/event5 3 57 -1",
            "su -c sendevent /dev/input/event5 1 330 0",
            "su -c sendevent /dev/input/event5 1 325 0",
            "su -c sendevent /dev/input/event5 0 0 0"
        ]

        for command in commands:
            send_adb_command(command)

        return True
    
    def stop(self) -> None:
        pass

class MyAction(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        return True

    def stop(self) -> None:
        pass

fight_start = FightStart()
fight_end = FightEnd()
my_act = MyAction()

if __name__ == "__main__":
    asyncio.run(main())
