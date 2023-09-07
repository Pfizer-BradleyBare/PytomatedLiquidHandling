from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import DeckLocation, Labware, Tip
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC
from .IMCSTip import DesaltingTipTracker
from .Interface import IMCSDesaltingOptions


@dataclass
class IMCSDesaltingABC(InterfaceABC, HALObject):
    TipInstance: Tip.Base.TipABC
    PipetteTipSupportDropOffSequence: str
    PipetteTipSupportPickupSequence: str
    IMCSTipSupportDropOffSequence: str
    IMCSTipSupportPickupSequence: str
    LoadLiquidClass: str
    EluteLiquidClass: str
    SupportedSourceLabwares: list[Labware.Base.LabwareABC]
    SupportedDestinationLabwares: list[Labware.Base.LabwareABC]
    SupportedDeckLocationTracker: list[DeckLocation.Base.DeckLocationABC]
    DesaltingTipTrackerInstance: DesaltingTipTracker
    IMCSTipDropOffSequence: str
    IMCSTipPickupSequence: str
    IMCSTipPipetteSequence: str
    IsEquilibrated: bool = field(init=False, default=False)

    @abstractmethod
    def Equilibrate(self, Options: IMCSDesaltingOptions.ListedOptions):
        self.IsEquilibrated = True

    @abstractmethod
    def Desalt(self, Options: IMCSDesaltingOptions.ListedOptions):
        self.IsEquilibrated = False
