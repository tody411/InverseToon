
# -*- coding: utf-8 -*-
## @package inversetoon.data.contour
#
#  Contour data class.
#  @author      tody
#  @date        2015/07/30

import numpy as np


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

    ## Clip contours by clipping Mask.
    def clipByMask(self, M_8U, endpoints=True):
        if M_8U is None:
            return

        segments_clipped = []

        for segment in self._segments:
            segment_clipped = []

            p_start = None

            for p in segment:
                if M_8U[p[1], p[0]] == 255:
                    p_start = p

                    if len(segment_clipped) > 0:
                        if endpoints:
                            segment_clipped.append(p)

                        segments_clipped.append(np.array(segment_clipped))
                        segment_clipped = []
                        p_start = None
                        continue

                if endpoints:
                    if p_start is not None:
                        segment_clipped.append(p_start)

                segment_clipped.append(p)

        if len(segment_clipped) > 0:
            segments_clipped.append(np.array(segment_clipped))

        self._segments = segments_clipped
