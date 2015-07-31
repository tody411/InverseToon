# -*- coding: utf-8 -*-
## @package inversetoon.data.isophote_mesh
#
#  Isophote mesh class.
#  @author      tody
#  @date        2015/07/17

import json

from inversetoon.data.data import Data
from inversetoon.data.curve import NormalCurve, IsophoteCurve



## Isophote mesh class.
#
#  Attributes:
#  * silhouette_curve: NormalCurve data for silhouette.
#  * isophote_curves: list of IsophoteCurve data for isophotes.
class IsophoteMesh(Data):
    ## Constructor
    def __init__(self, silhouette_curve=NormalCurve(), isophote_curves=[]):
        self._silhouette_curve = silhouette_curve
        self._isophote_curves = isophote_curves

    def silhouetteCurve(self):
        return self._silhouette_curve

    def setSilhouetteCurve(self, silhouetteCurve):
        self._silhouette_curve = silhouetteCurve

    def isophoteCurves(self):
        return  self._isophote_curves

    def setIsophoteCurves(self, isophoteCurves):
        self._isophote_curves = isophoteCurves

    #################
    # Data IO
    #################
    def _dataDict(self):
        isophoteCurvesDicts = [isophoteCurve._dataDict()
                               for isophoteCurve in self._isophote_curves]
        return {"silhoutte": self._silhouette_curve._dataDict(),
                "isophotes": isophoteCurvesDicts}

    def _setDataDict(self, data):
        self._silhouette_curve._setDataDict(data["silhoutte"])

        self._isophote_curves = []
        for isophoteCurveDict in data["isophotes"]:
            isophoteCurve = IsophoteCurve()
            isophoteCurve._setDataDict(isophoteCurveDict)
            self._isophote_curves.append(isophoteCurve)
