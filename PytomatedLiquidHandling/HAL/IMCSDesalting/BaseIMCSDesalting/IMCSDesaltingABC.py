from ....Tools.AbstractClasses import UniqueObjectABC
from ...Tools.AbstractClasses import InterfaceABC
from ...DeckLocation import DeckLocationTracker
from ...Tip.BaseTip import Tip
from ...Labware import LabwareTracker
from dataclasses import dataclass, field
from .IMCSTip import DesaltingTipTracker
from .Interface import IMCSDesaltingOptions
from abc import abstractmethod


@dataclass
class IMCSDesaltingABC(InterfaceABC, UniqueObjectABC):
    TipInstance: Tip
    PipetteTipSupportDropOffSequence: str
    PipetteTipSupportPickupSequence: str
    IMCSTipSupportDropOffSequence: str
    IMCSTipSupportPickupSequence: str
    LoadLiquidClass: str
    EluteLiquidClass: str
    SupportedSourceLabwareTrackerInstance: LabwareTracker
    SupportedDestinationLabwareTrackerInstance: LabwareTracker
    SupportedDeckLocationTrackerInstance: DeckLocationTracker
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
