
# -*- coding: utf-8 -*-
## @package inversetoon.data.scene
#
#  Scene data definition.
#  @author      tody
#  @date        2015/07/30

from inversetoon.data.data import Data
from inversetoon.data.isophote_mesh import IsophoteMesh

from inversetoon.io.image import loadNormal

from inversetoon.util.logger import getLogger
logger = getLogger(__name__)


## Scene data definition.
#
#  Attribute:
#   isophoteMesh
#   normalImage
class Scene(Data):
    ## Constructor
    #  @param  isophote_mesh  IsophoteMesh data.
    #  @param  normal_image_file  Normal image file path.
    def __init__(self, isophote_mesh=IsophoteMesh(), normal_image_file=None):
        self._isophote_mesh = isophote_mesh
        self._normal_image_file = normal_image_file
        self._normal_image = None
        self._alpha_image = None

    def setIsophoteMesh(self, isophote_mesh):
        self._isophote_mesh = isophote_mesh

    def isophoteMesh(self):
        return self._isophote_mesh

    def setNormalImageFile(self, normal_image_file):
        self._normal_image_file = normal_image_file

    def normalImageFile(self):
        return self._normal_image_file

    def normalImage(self):
        if self._normal_image is None:
            self._normal_image, self._alpha_image = loadNormal(self._normal_image_file)

        return self._normal_image

    def alphaImage(self):
        if self._alpha_image is None:
            self._normal_image, self._alpha_image = loadNormal(self._normal_image_file)

        return self._alpha_image

    #################
    # Data IO
    #################

    def _dataDict(self):
        isophote_mesh_dicts = self._isophote_mesh._dataDict()
        isophote_mesh_dicts["normalImageFile"] = self._normal_image_file
        return isophote_mesh_dicts

    def _setDataDict(self, data):
        self._isophote_mesh._setDataDict(data)
        self._normal_image_file = data["normalImageFile"]

