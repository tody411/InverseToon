
# -*- coding: utf-8 -*-
## @package inversetoon.data.isophote_mesh
#
#  Isophote mesh definition.
#  @author      tody
#  @date        2015/07/17

import json

from curve import NormalCurve, IsophoteCurve


## Isophote mesh data.
#  Constructed by 1 silhoutte curve and n isophote curves.
class IsophoteMesh:
    ## Constructor
    #  @param  silhouette_curve  NormalCurve data for silhoutte.
    #  @param  isophote_curves  List of IsophoteCurve data for isophotes.
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

    def writeJson(self):
        data = self._dataDict()
        return json.dumps(data, sort_keys=True, indent=4)

    def loadJson(self, json_data):
        data = json.loads(json_data)
        self._setDataDict(data)

    def _dataDict(self):
        isophoteCurvesDicts = [isophoteCurve._dataDict()
                               for isophoteCurve in self._isophote_curves]
        return {"silhoutte": self._silhouette_curve._dataDict(),
                "isophoteCurves": isophoteCurvesDicts}

    def _setDataDict(self, data):
        self._silhouette_curve._setDataDict(data["silhoutte"])

        self._isophote_curves = []
        for isophoteCurveDict in data["isophoteCurves"]:
            isophoteCurve = IsophoteCurve()
            isophoteCurve._setDataDict(isophoteCurveDict)
            self._isophote_curves.append(isophoteCurve)