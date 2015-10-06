# -*- coding: utf-8 -*-
## @package inversetoon.core.isophote
#
#  Isophote functions.
#  @author      tody
#  @date        2015/07/31

from inversetoon.cv.image import to8U
from inversetoon.cv.contour import findContours
from inversetoon.data.curve import IsophoteCurve
from inversetoon.core.smoothing import smoothing_contour


def isophoteCurves(I_32F, iso_values=[0.2, 0.4, 0.6, 0.8], M_8U=None):
    I_8U = to8U(I_32F)
    isophote_curves = []
    for iso_value in iso_values:
        isophote_curves.append(isophoteCurve(I_8U, iso_value, M_8U))
    return isophote_curves


def isophoteCurve(I_8U, iso_value, M_8U):
    contour = findContours(I_8U, 255 * iso_value)
    print contour.segments()

    contour.clipByMask(M_8U)
    contour.resample(span=5)
    contour = smoothing_contour(contour)

    isophoteCurve = IsophoteCurve()
    isophoteCurve.setContour(contour)
    isophoteCurve.setIsoValue(iso_value)
    isophoteCurve.setSilhouetteMask(M_8U)
    return isophoteCurve
