
# -*- coding: utf-8 -*-
## @package inversetoon.data.contour
#
#  Contour data definition.
#  @author      tody
#  @date        2015/07/30


## Contour data definition.
class Contour:
    ## Constructor
    #  @param  segments  [segment1, ..., segmentn]. segment = [(p1x, p1y), ..., (pnx, pny)].
    #  @param  closing   closing, [p1, ..., pn] -> [p1, ..., pn, p1].
    def __init__(self, segments=[], closing=False):
        self._segments_cvIDs = segments
        self._closing = closing

    def setSegments(self, segments):
        self._segments_cvIDs = segments

    def segments(self):
        return self._segments_cvIDs

    def setClosing(self, closing):
        self._closing = closing

    def closing(self):
        return self._closing

