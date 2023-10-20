from PytomatedLiquidHandling.HAL import DeckLocation, Labware
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject


class LayoutItemABC(HALObject):
    LabwareID: str
    DeckLocation: DeckLocation.Base.DeckLocationABC
    Labware: Labware.Base.LabwareABC
