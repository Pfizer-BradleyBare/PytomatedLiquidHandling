from ....Tools.AbstractClasses import ObjectABC
from ...Tools.Labware.BaseLabware import Labware as APILabware


class TransferOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        SourceAPILabware: APILabware,
        SourceMixCycles: int,
        DestinationAPILabware: APILabware,
        DesitnationMixCycles: int,
        TransferVolume: float,
    ):
        self.Name: str = Name

        self.SourceAPILabware: APILabware = SourceAPILabware
        self.DestinationAPILabware: APILabware = DestinationAPILabware

        self.SourceMixCycles: int = SourceMixCycles
        self.DesitnationMixCycles: int = DesitnationMixCycles

        self.TransferVolume: float = TransferVolume
