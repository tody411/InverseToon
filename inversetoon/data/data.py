
# -*- coding: utf-8 -*-
## @package inversetoon.data.data
#
#  Base data definition.
#  @author      tody
#  @date        2015/07/30

import json

from inversetoon.util.logger import getLogger
logger = getLogger(__name__)


## Base data definition.
#
#  Provide Json IO (writeJson, loadJson) by implementing _dataDict and _setDataDict.
class Data(object):
    ## Constructor
    def __init__(self):
        pass

    #################
    # Data IO
    #################

    ## Write Json file (shared with derived classes).
    #  Note: implement _dataDict method in the derived class.
    def writeJson(self):
        data = self._dataDict()
        return json.dumps(data)

    ## Load Json file (shared with derived classes).
    #  Note: implement _setDataDict method in the derived class.
    def loadJson(self, json_data):
        data = json.loads(json_data)
        self._setDataDict(data)

    ## dictionary data for writeJson method.
    def _dataDict(self):
        logger.warning("Need to implement _dataDict function.")
        return None

    ## set dictionary data for loadJson method.
    def _setDataDict(self, data):
        logger.warning("Need to implement _setDataDict function.")
        pass
