# -*- coding: utf-8 -*-
## @package inversetoon.datasets.normal
#
#  Normal map dataset loader functions.
#  @author      tody
#  @date        2015/07/31


import os
from inversetoon.io.image import loadNormal, saveNormal

from inversetoon.util.logger import getLogger
logger = getLogger(__name__)

data_dir = os.path.join(os.path.dirname(__file__), "normal")
original_data_dir = os.path.join(os.path.dirname(__file__), "normal_original")


## Data directory.
def dataDir(target="normal"):
    if target == "normal":
        return data_dir
    else:
        return original_data_dir


## Data names.
def dataNames(target="normal"):
    logger.debug(dataDir(target))
    images = os.listdir(data_dir)
    data_names = []

    for image in images:
        data_names.append(image.replace(".png", ""))
    return data_names


## Data file name.
def dataFile(data_name, target="normal"):
    img_file = os.path.join(dataDir(target), "%s.png" % data_name)
    logger.debug(img_file)
    return img_file


## Load data for the data name.
def loadData(data_name, target="normal"):
    img_file = dataFile(data_name, target)
    N_32F, A_8U = loadNormal(img_file)
    return N_32F, A_8U


## Save data for the data name.
def saveData(data_name, N_32F, A_8U, target="normal"):
    img_file = dataFile(data_name, target)
    saveNormal(img_file, N_32F, A_8U)
