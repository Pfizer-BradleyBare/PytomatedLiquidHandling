from pydantic import field_validator

from PytomatedLiquidHandling.HAL import DeckLocation, Labware
from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
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
