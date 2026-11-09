import glob
import os


def clear_workdir(name: str, dir: str = ""):

    basename = os.path.join(dir, name)

    paths = []
    paths += glob.glob(basename+"*.png")
    paths += glob.glob(basename+"*.mp4")

    for path in paths:
        os.remove(path)
