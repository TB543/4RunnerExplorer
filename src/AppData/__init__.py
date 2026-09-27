from json import load, dump


MOUNTPOINTS = []
try:
    with open("AppData/mountpoints.json", "r") as f:
        MOUNTPOINTS = load(f)
except:
    with open("AppData/mountpoints.json", "w") as f:
        dump(MOUNTPOINTS, f, indent=4)
