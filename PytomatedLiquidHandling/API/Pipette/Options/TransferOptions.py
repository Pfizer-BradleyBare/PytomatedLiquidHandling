from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectABC

from ...Tools.Container.BaseContainer import Container


class TransferOptions(NonUniqueObjectABC):
    def __init__(
        self,
        SourceContainerInstance: Container,
        SourceMixCycles: int,
        SourceWellPosition: int,
        DestinationContainerInstance: Container,
        DestinationMixCycles: int,
        DestinationWellPosition: int,
        TransferVolume: float,
    ):
        self.SourceContainerInstance: Container = SourceContainerInstance
        self.DestinationContainerInstance: Container = DestinationContainerInstance

        self.SourceMixCycles: int = SourceMixCycles
        self.DestinationMixCycles: int = DestinationMixCycles

        self.SourceWellPosition: int = SourceWellPosition
        self.DestinationWellPosition: int = DestinationWellPosition

        self.TransferVolume: float = TransferVolume
