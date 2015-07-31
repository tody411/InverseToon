
# -*- coding: utf-8 -*-
## @package inversetoon.data.contour
#
#  Contour data class.
#  @author      tody
#  @date        2015/07/30


## Contour data class.
#  Attributes:
#  * segments: list of segment data.
#      - segment: list of points (n x 2 numpy.array).
#  * closing: if True, [p1, ..., pn] -> [p1, ..., pn, p1].
class Contour:
    ## Constructor
    def __init__(self, segments=[], closing=False):
        self._segments = segments
        self._closing = closing

    def setSegments(self, segments):
        self._segments = segments

    def segments(self):
        return self._segments

    def setClosing(self, closing):
        self._closing = closing

    def closing(self):
        return self._closing

