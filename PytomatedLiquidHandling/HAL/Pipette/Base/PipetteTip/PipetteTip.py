from pydantic import field_validator, BaseModel

from PytomatedLiquidHandling.HAL import Tip


class PipetteTip(BaseModel):
    Tip: Tip.Base.TipABC
    TipSupportDropoffLabwareID: str
    TipSupportPickupLabwareID: str
    TipWasteLabwareID: str
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

    def IsLiquidClassCategorySupported(self, Category: str) -> bool:
        return Category in self.SupportedLiquidClassCategories

    def IsVolumeSupported(self, Volume: float) -> bool:
        return Volume <= self.Tip.Volume
