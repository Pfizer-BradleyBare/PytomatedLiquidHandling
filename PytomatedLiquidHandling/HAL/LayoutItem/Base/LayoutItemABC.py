from PytomatedLiquidHandling.HAL import DeckLocation, Labware
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject
from pydantic import field_validator


class LayoutItemABC(HALObject):
    LabwareID: str
    DeckLocation: DeckLocation.Base.DeckLocationABC
    Labware: Labware.Base.LabwareABC

    @field_validator("DeckLocation", mode="before")
    def __DeckLocationValidate(cls, v):
        Objects = DeckLocation.GetObjects()
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
        Objects = Labware.GetObjects()
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + Labware.Base.LabwareABC.__name__
                + " objects."
            )

        return Objects[Identifier]
