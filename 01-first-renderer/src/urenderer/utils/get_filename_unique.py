import os


def get_filename_unique(filename: str, path: str = "", extension=".png") -> str:

    i = 0
    new_path = os.path.join(path, filename+f"{i:03d}"+extension)
    while os.path.exists(new_path):
        i += 1
        new_path = os.path.join(path, filename+f"{i:03d}"+extension)
    return new_path
