from ....Tools.AbstractClasses import ObjectABC


class LoadCarrierOptions(ObjectABC):
    def __init__(self, Name: str, Sequence: str):

        self.Name: str = Name

        self.Sequence: str = Sequence
        self.BarcodeFilePath: str = "barcode_1.txt"
        self.LabwareScanPositions: str = "?"

    def GetName(self) -> str:
        return self.Name
