
# -*- coding: utf-8 -*-
## @package inversetoon.core.angle
#
#  inversetoon.core.angle utility package.
#  @author      tody
#  @date        2015/09/28

import numpy as np


def angleErros(Ns1, Ns2):
    cos_errors = [np.dot(N1, N2) for N1, N2 in zip(Ns1, Ns2)]
    cos_errors = np.clip(cos_errors, -1.0, 1.0)
    angle_errors = np.arccos(cos_errors)
    return np.degrees(angle_errors)