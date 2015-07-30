
# -*- coding: utf-8 -*-
## @package inversetoon.data.curve
#
#  Curve data definitions.
#  @author      tody
#  @date        2015/07/17

import json
import numpy as np

from inversetoon.data.contour import Contour
from inversetoon.data.data import Data
from inversetoon.data.segment import IsophoteSegment


## Curve data definition.
class Curve(Data):
    ## Constructor
    #  @param  cvs  control vertices. [(p1x, p1y), ..., (pnx, pny)].
    #  @param  segments [segment1, ..., segmentn]. segment = [(cvID1), ..., (cvIDn)].
    def __init__(self, cvs=[], segments_cvIDs=[]):
        self._cvs = np.array(cvs)
        self._segments_cvIDs = segments_cvIDs

    def numCVs(self):
        return len(self._cvs)

    def CVs(self):
        return self._cvs

    def setCVs(self, cvs):
        self._cvs = cvs

    def segments(self):
        return self._segments_cvIDs

    def setSegments(self, segments):
        self._segments_cvIDs = segments

    def setCurve(self, curve):
        self._cvs = curve._cvs
        self._segments_cvIDs = curve._segments_cvIDs

    def curvePoints(self):
        curves = []

        for segment in self._segments_cvIDs:
            curve = []
            for cvID in segment:
                curve.append(self._cvs[cvID])

            curve = np.array(curve)
            curves.append(curve)
        return curves

    def resampleCurve(self, span=10):
        segments_resampled = []

        for segment in self._segments_cvIDs:
            segment_resampled = segment[::span]
            segment_resampled.append(segment[-1])

            segments_resampled.append(segment_resampled)

        self.resampleSegments(segments_resampled)

    def resampleSegments(self, segments):
        cvIDs_resampled = set()
        for segment in segments:
            for cvID in segment:
                cvIDs_resampled.add(cvID)

        cvIDs_resampled = list(cvIDs_resampled)
        cvIDs_resampled.sort()
        cvIDs_map = {}
        for i, cvID in enumerate(cvIDs_resampled):
            cvIDs_map[cvID] = i

        self._cvs = self._cvs[cvIDs_resampled]

        for segment in segments:
            for i in range(len(segment)):
                segment[i] = cvIDs_map[segment[i]]
        self._segments_cvIDs = segments

    def setContour(self, contour):
        cvs = []
        self._segments_cvIDs = []

        si = 0
        for p_segment in contour.segments():
            segment = []
            for p in p_segment:
                cvs.append(p)
                segment.append(si)
                si += 1
            self._segments_cvIDs.append(segment)

        self._cvs = np.array(cvs)
        self.setClosing(contour.closing())

    def contour(self):
        cvs = self._cvs
        segments_cvIDs = self._segments_cvIDs

        contour_segments = []

        for segment_cvIDs in segments_cvIDs:
            coutour_segment = []
            for cvID in segment_cvIDs:
                p = cvs[cvID]
                coutour_segment.append(p)
            contour_segments.append(np.array(coutour_segment))

        return Contour(contour_segments, self.isClosing())

    def setClosing(self, closing=True):
        if closing:
            if self._segments_cvIDs[0][0] != self._segments_cvIDs[-1][-1]:
                self._segments_cvIDs[-1].append(self._segments_cvIDs[0][0])
        else:
            if self._segments_cvIDs[0][0] == self._segments_cvIDs[-1][-1]:
                self._segments_cvIDs[-1] = self._segments_cvIDs[-1][:-1]

    def isClosing(self):
        return self._segments_cvIDs[0][0] == self._segments_cvIDs[-1][-1]

    #################
    # Data IO
    #################

    ## dictionary data for writeJson method.
    def _dataDict(self):
        data = {"cvs": self._cvs.tolist(), "segmentsCVIDs": self._segments_cvIDs}
        return data

    ## set dictionary data for loadJson method.
    def _setDataDict(self, data):
        self._cvs = np.array(data["cvs"])
        self._segments_cvIDs = data["segmentsCVIDs"]


## Curve data with normals.
class NormalCurve(Curve):
    ## Constructor
    #  @param  normals  Additional normal data with the same size of cvs.
    def __init__(self, cvs=[], segments=[], normals=[]):
        super(NormalCurve, self).__init__(cvs, segments)
        self._normals = np.array(normals)

    def normals(self):
        return self._normals

    def setNormals(self, normals):
        self._normals = normals

    def setNormalImage(self, N_32F):
        normals = []

        for cv in self._cvs:
            normals.append(N_32F[int(cv[1])][int(cv[0])])

        self._normals = np.array(normals)

    def toCurveSegments(self):
        segments = []

        cvs = self._cvs
        normals = self._normals
        for cv_ids in self._segments_cvIDs:
            segment = IsophoteSegment(cvs[cv_ids], cv_ids)
            segment.setNormals(normals[cv_ids])
            segments.append(segment)

        return segments

    #################
    # Data IO
    #################

    def _dataDict(self):
        data = super(NormalCurve, self)._dataDict()
        data["normals"] = self._normals.tolist()
        return data

    def _setDataDict(self, data):
        super(NormalCurve, self)._setDataDict(data)
        self._normals = np.array(data["normals"])


## Isophote curve data.
class IsophoteCurve(NormalCurve):
    ## Constructor
    #  @param  L  Lgiht direction for the isophote.
    #  @param  iso_value  Illumination value for the isophote.
    #  @param  silhouette_cvIDs  Control vertex IDs of sihoutte vertices.
    def __init__(self, cvs=[], segments=[], normals=[], L=np.array([0, 0, 1]),
                 iso_value=0, silhouette_cvIDs=[]):
        super(IsophoteCurve, self).__init__(cvs, segments, normals)
        self._L = L
        self._iso_value = iso_value
        self._silhouette_cvIDs = silhouette_cvIDs

    def LightDir(self):
        return self._L

    def setLightDir(self, L):
        self._L = L

    def isoValue(self):
        return self._iso_value

    def setIsoValue(self, iso_value):
        self._iso_value = iso_value

    def silhouetteCVIDs(self):
        return self._silhouette_cvIDs

    def setSilhouetteCVIDs(self, silhouetteCVIDs):
        self._silhouette_cvIDs = sorted(list(set(silhouetteCVIDs)))

    def setSilhouetteMask(self, S_8U):
        cvs = self.CVs()
        segments = self.segments()

        silhouetteCVIDs = []

        for segment in segments:
            for cvID in segment:
                p = cvs[cvID]

                if S_8U[p[1], p[0]] == 255:
                    silhouetteCVIDs.append(cvID)

        self.setSilhouetteCVIDs(silhouetteCVIDs)

    def toCurveSegments(self):
        segments = []

        cvs = self._cvs
        normals = self._normals
        for cv_ids in self._segments_cvIDs:
            segment = IsophoteSegment(cvs[cv_ids], cv_ids)
            segment.setLightDir(self._L)
            segment.setNormals(normals[cv_ids])
            segments.append(segment)

        return segments

    #################
    # Data IO
    #################

    def _dataDict(self):
        data = super(IsophoteCurve, self)._dataDict()
        data["L"] = self._L.tolist()
        data["isoValue"] = self._iso_value
        data["silhouetteCVIDs"] = list(self._silhouette_cvIDs)
        return data

    def _setDataDict(self, data):
        super(IsophoteCurve, self)._setDataDict(data)

        self._L = np.array(data["L"])
        self._iso_value = data["isoValue"]
        self._silhouette_cvIDs = data["silhouetteCVIDs"]