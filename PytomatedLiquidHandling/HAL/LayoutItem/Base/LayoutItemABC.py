from pydantic import field_validator

from PytomatedLiquidHandling.HAL import DeckLocation, Labware
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice


class LayoutItemABC(HALDevice):
    LabwareID: str
    DeckLocation: DeckLocation.Base.DeckLocationABC
    Labware: Labware.Base.LabwareABC

    @field_validator("DeckLocation", mode="before")
    def __DeckLocationValidate(cls, v):
        Objects = DeckLocation.Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + DeckLocation.Base.DeckLocationABC.__name__
                + " objects."
            )

        return Objects[Identifier]

    @field_validator("Labware", mode="before")
    def __LabwareValidate(cls, v):
        Objects = Labware.Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + Labware.Base.LabwareABC.__name__
                + " objects."
            )

        return Objects[Identifier]
