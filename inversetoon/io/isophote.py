# -*- coding: utf-8 -*-
## @package inversetoon.io.isophote
#
#  Isophote scene IO utility package.
#  @author      tody
#  @date        2015/07/18

from inversetoon.data.scene import Scene


def loadSceneData(file_path):
    with open(file_path, 'r') as f:
        jsonData = f.read()
        scene = Scene()
        scene.loadJson(jsonData)
        return scene

    return None


def saveSceneData(file_path, scene):
    with open(file_path, 'w') as f:
        f.write(scene.writeJson())
