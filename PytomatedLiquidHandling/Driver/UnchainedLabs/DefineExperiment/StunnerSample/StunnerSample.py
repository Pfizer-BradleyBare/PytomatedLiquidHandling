class StunnerSample:
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
        self.SampleName: str = SampleName
        self.PlateName: str = PlateName
        self.Well: str = Well
        self.BlankSampleName: str = BlankSampleName
        self.ExtinctionCoefficient: float = ExtinctionCoefficient
        self.SampleMetaData: str = SampleMetaData
        self.BufferMetaData: str = BufferMetaData
