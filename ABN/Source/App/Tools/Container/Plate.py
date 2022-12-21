from ....API.Tools.Container import Plate as APIPlate
from ...Workbook.Block import BlockTracker


class Plate(APIPlate):
    def __init__(self, Name: str, MethodName: str, Filter: str):
        APIPlate.__init__(self, Name, MethodName, Filter)

        self.BlockTrackerInstance: BlockTracker = BlockTracker()
