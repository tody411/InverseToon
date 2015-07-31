
import os
from inversetoon.io.image import loadNormal

from inversetoon.util.logger import getLogger
logger = getLogger(__name__)

data_dir = os.path.abspath(__file__).replace(".py", "")


## Data names.
def dataNames():
    scenes = os.listdir(data_dir)
    data_names = []

    for scene in scenes:
        data_names.append(scene.replace(".png", ""))
    return data_names


## Data file name.
def dataFile(data_name):
    img_file = os.path.join(data_dir, "%s.png" % data_name)
    logger.debug(img_file)
    return img_file


## Load data for the data name.
def loadData(data_name):
    img_file = dataFile(data_name)
    N_32F, A_8U = loadNormal(img_file)
    return N_32F, A_8U