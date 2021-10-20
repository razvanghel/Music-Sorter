import os
import shutil
def is_dir(path):
    return os.path.isdir(path)

def create_file(path):
    file = open(path, "w")
    file.close()

def create_directory(path):
    os.mkdir(path)

def is_file(path):
    return os.path.isfile(path)

def remove_directory(path):
    os.remove(path)

def remove_directory_with_contents(path):
    shutil.rmtree(path)

def move_file(old_path, new_path):
    try:
        os.rename(old_path, new_path)
    except:
        npath = new_path.split("\\")[-1]
        npath = new_path.replace(f"\\{npath}", "")
        string = ""
        if not is_dir(old_path):
            string = f"{old_path} not found"
        elif not is_dir(npath):
            string = f"{npath} not found"
        raise FileNotFoundError(string)

def extract_from_path(path):
    path.replace("/", "\\")
    return path.split("\\")[-1]

def combine_paths(param, param2):
    try:
        return param +"\\" + param2
    except:
        return None


def exists(path):
    return is_dir(path) or is_file(path)