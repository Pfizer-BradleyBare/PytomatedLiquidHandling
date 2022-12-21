from ....Tools.AbstractClasses import ObjectABC
from ...Tools.Container.BaseContainer import Container


class TransferOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        SourceContainerInstance: Container,
        SourceMixCycles: int,
        DestinationContainerInstance: Container,
        DesitnationMixCycles: int,
        TransferVolume: float,
    ):
        self.Name: str = Name

        self.SourceContainerInstance: Container = SourceContainerInstance
        self.DestinationContainerInstance: Container = DestinationContainerInstance

        self.SourceMixCycles: int = SourceMixCycles
        self.DesitnationMixCycles: int = DesitnationMixCycles

        self.TransferVolume: float = TransferVolume
