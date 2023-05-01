from .....Tools.AbstractClasses import NonUniqueObjectABC


class AdvancedOptions:
    def __init__(
        self,
        *,
        BarcodeFilePath: str | None = None,
        LabwareScanPositions: str | None = None,
    ):
        self.BarcodeFilePath: str | None = BarcodeFilePath
        self.LabwareScanPositions: str | None = LabwareScanPositions


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        Sequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.Sequence: str = Sequence

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(
            BarcodeFilePath="barcode_1.txt", LabwareScanPositions="?"
        )
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
