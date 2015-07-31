
# -*- coding: utf-8 -*-
## @package inversetoon.batch.batch
#
#  Batch functions.
#  @author      tody
#  @date        2015/07/31

from inversetoon.datasets import normal, isophote

from inversetoon.util.timer import Timer
from inversetoon.util.logger import getLogger
logger = getLogger(__name__)


def normalDataSetBatch(func):
    logger.info("Normal Dataset Batch: %s" % func.__name__)
    for data_name in normal.dataNames():
        with Timer(data_name, logger) as t:
            func(data_name)
