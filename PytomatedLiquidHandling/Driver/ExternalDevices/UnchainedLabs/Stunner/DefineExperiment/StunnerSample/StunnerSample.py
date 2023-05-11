from .......Tools.AbstractClasses import UniqueObjectABC


class StunnerSample(UniqueObjectABC):
    def __init__(
        self,
        *,
        SampleName: str,
        PlateName: str,
        Well: str,
        BlankSampleName: str,
        ExtinctionCoefficient: float,
        SampleMetaData: str = "NA",
        BufferMetaData: str = "NA",
    ):
        UniqueObjectABC.__init__(self, PlateName + ": " + str(Well))
        self.SampleName: str = SampleName
        self.PlateName: str = PlateName
        self.Well: str = Well
        self.BlankSampleName: str = BlankSampleName
        self.ExtinctionCoefficient: float = ExtinctionCoefficient
        self.SampleMetaData: str = SampleMetaData
        self.BufferMetaData: str = BufferMetaData
