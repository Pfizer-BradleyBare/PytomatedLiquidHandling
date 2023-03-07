from ...Tools import BlockParameter
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class Dilute(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.Source = BlockParameter.List[str](self, 1)
        self.Dilent = BlockParameter.List[str](self, 2)
        self.StartingConc = BlockParameter.List[int | float](self, 3)
        self.TargetConc = BlockParameter.List[int | float](self, 4)
        self.TargetVolume = BlockParameter.List[int | float](self, 5)
        self.SourceVolumeLimit = BlockParameter.List[int | float](self, 6)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:
        ...

    # This is created by Avi and Diane 2/9/23 for ABNLogger
    # ABNloggerLogBlock(ABNLoggerDict, ExcelInstance.ExcelFilePath, 'Dilute', Row, Col,
    ##                 [self.Source, self.Dilent, self.StartingConc, self.TargetConc, self.TargetVolume, self.SourceVolumeLimit])
