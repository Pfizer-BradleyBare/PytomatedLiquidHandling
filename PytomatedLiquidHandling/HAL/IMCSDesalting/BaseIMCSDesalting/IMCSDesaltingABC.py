from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import DeckLocation, Labware, Tip
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import InterfaceABC
from .IMCSTip import DesaltingTipTracker
from .Interface import IMCSDesaltingOptions


@dataclass
class IMCSDesaltingABC(InterfaceABC, UniqueObjectABC):
    TipInstance: Tip.BaseTip.Tip
    PipetteTipSupportDropOffSequence: str
    PipetteTipSupportPickupSequence: str
    IMCSTipSupportDropOffSequence: str
    IMCSTipSupportPickupSequence: str
    LoadLiquidClass: str
    EluteLiquidClass: str
    SupportedSourceLabwareTrackerInstance: Labware.LabwareTracker
    SupportedDestinationLabwareTrackerInstance: Labware.LabwareTracker
    SupportedDeckLocationTrackerInstance: DeckLocation.DeckLocationTracker
    DesaltingTipTrackerInstance: DesaltingTipTracker
    IMCSTipDropOffSequence: str
    IMCSTipPickupSequence: str
    IMCSTipPipetteSequence: str
    IsEquilibrated: bool = field(init=False, default=False)

    @abstractmethod
    def Equilibrate(self, OptionsTrackerInstance: IMCSDesaltingOptions.OptionsTracker):
        self.IsEquilibrated = True

    @abstractmethod
    def Desalt(self, OptionsTrackerInstance: IMCSDesaltingOptions.OptionsTracker):
        self.IsEquilibrated = False
