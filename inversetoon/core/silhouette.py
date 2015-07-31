# -*- coding: utf-8 -*-
## @package inversetoon.core.silhouette
#
#  Silhoutte functions.
#  @author      tody
#  @date        2015/07/31

from inversetoon.cv.contour import findContours, contourMask
from inversetoon.data.curve import NormalCurve


def silhoutteCurve(A_8U):
    h, w = A_8U.shape
    contour = findContours(A_8U, 200.0)
    silhoutteCurve = NormalCurve()
    silhoutteCurve.setContour(contour)
    silhoutteCurve.resampleCurve(span=5)

    silhoutte_contour = findContours(A_8U, 127.0)

    S_8U = contourMask(silhoutte_contour, h, w)
    S_8U[A_8U < 127] = 255
    return silhoutteCurve, S_8U
