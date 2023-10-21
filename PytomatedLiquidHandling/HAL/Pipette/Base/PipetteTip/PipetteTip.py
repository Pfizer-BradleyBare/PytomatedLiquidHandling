from pydantic import BaseModel, field_validator

from PytomatedLiquidHandling.HAL import Tip


class PipetteTip(BaseModel):
    Tip: Tip.Base.TipABC
    TipSupportDropoffLabwareID: str
    TipSupportPickupLabwareID: str
    TipWasteLabwareID: str
    TipWastePositionIDs: list[str]
    SupportedLiquidClassCategories: dict[str, str]

    @field_validator("Tip", mode="before")
    def __TipValidate(cls, v):
        Objects = Tip.GetObjects()
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + Tip.Base.TipABC.__name__
                + " objects."
            )

        return Objects[Identifier]

    @field_validator("TipWastePositionIDs", mode="before")
    def __TipWastePositionIDsValidate(cls, v):
        print("HERE")
        if isinstance(v, list):
            return [str(v) for v in v]
        else:
            v = v.lower()
            if "range" in v:
                return [
                    str(v)
                    for v in list(
                        range(
                            *[
                                int(v)
                                for v in v.replace("range(", "")
                                .replace(")", "")
                                .split(",")
                            ]
                        )
                    )
                ]
            # This allows us to trick pydantic into understanding a range object. However, the desired object is a list of strings.
            else:
                ValueError("The only acceptable inputs are either range or list.")

    def IsLiquidClassCategorySupported(self, Category: str) -> bool:
        return Category in self.SupportedLiquidClassCategories

    def IsVolumeSupported(self, Volume: float) -> bool:
        return Volume <= self.Tip.Volume
