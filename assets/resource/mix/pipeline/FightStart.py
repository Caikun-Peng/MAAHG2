import subprocess

def send_adb_command(command):
    subprocess.run(f"adb shell {command}", shell=True)

commands = [
    "su -c sendevent /dev/input/event5 3 57 1",
    "su -c sendevent /dev/input/event5 1 330 1",
    "su -c sendevent /dev/input/event5 1 325 1",
    "su -c sendevent /dev/input/event5 3 53 240",
    "su -c sendevent /dev/input/event5 3 54 825",
    "su -c sendevent /dev/input/event5 0 0 0",
    "su -c sendevent /dev/input/event5 3 47 1",
    "su -c sendevent /dev/input/event5 3 57 2",
    "su -c sendevent /dev/input/event5 1 330 1",
    "su -c sendevent /dev/input/event5 1 325 1",
    "su -c sendevent /dev/input/event5 3 53 112",
    "su -c sendevent /dev/input/event5 3 54 1728",
    "su -c sendevent /dev/input/event5 0 0 0",
]

for command in commands:
    send_adb_command(command)
