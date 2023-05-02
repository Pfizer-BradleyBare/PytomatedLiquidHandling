from .....Tools.AbstractClasses import NonUniqueObjectABC
from ....Tools.AbstractOptions import AdvancedSingleOptionsABC, AdvancedOptionsWrapper


class AdvancedOptions(AdvancedSingleOptionsABC):
    @AdvancedOptionsWrapper
    def __init__(
        self,
        *,
        CustomErrorHandling: bool = False,
        BarcodeFilePath: str = "barcode_1.txt",
        LabwareScanPositions: str = "?",
    ):
        AdvancedSingleOptionsABC.__init__(self, CustomErrorHandling)
        self.BarcodeFilePath: str = BarcodeFilePath
        self.LabwareScanPositions: str = LabwareScanPositions


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        Sequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.Sequence: str = Sequence

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
