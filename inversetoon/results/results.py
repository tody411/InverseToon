
import os

_root_dir = os.path.dirname(__file__)


## Result directory.
def resultDir(dir_name=""):
    result_dir = os.path.join(_root_dir, dir_name)

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    return result_dir


## Result file.
def resultFile(result_dir, data_name, data_ext=".png"):
    result_file = os.path.join(result_dir, data_name + data_ext)
    return result_file
