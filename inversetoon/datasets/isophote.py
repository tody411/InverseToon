# -*- coding: utf-8 -*-
## @package inversetoon.datasets.isophote
#
#  Isophote scene dataset IO functions..
#  @author      tody
#  @date        2015/07/31



import os

from inversetoon.io.isophote import loadSceneData, saveSceneData

from inversetoon.util.logger import getLogger
logger = getLogger(__name__)

data_dir = os.path.join(os.path.dirname(__file__), "isophote")


## Data names.
def dataNames():
    scenes = os.listdir(data_dir)
    data_names = []

    for scene in scenes:
        data_names.append(scene.replace(".json", ""))
    return data_names


## Data file name.
def dataFile(data_name):
    img_file = os.path.join(data_dir, "%s.json" % data_name)
    logger.debug(img_file)
    return img_file


## Load data for the data name.
def loadData(data_name):
    data_file = dataFile(data_name)
    return loadSceneData(data_file)


## Save data for the data name.
def saveData(data_name, data):
    data_file = dataFile(data_name)
    saveSceneData(data_file, data)
