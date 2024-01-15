from pydantic import dataclasses, field_validator

from plh.hal import Tip

from .LiquidClass import LiquidClass


@dataclasses.dataclass(kw_only=True)
class PipetteTip:
    Tip: Tip.Base.TipABC
    TipSupportDropoffLabwareID: str
    TipSupportPickupLabwareID: str
    TipWasteLabwareID: str
    SupportedLiquidClassCategories: dict[str, list[LiquidClass]]

    @field_validator("Tip", mode="before")
    def __TipValidate(cls, v):
        Objects = Tip.Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + Tip.Base.TipABC.__name__
                + " objects.",
            )

        return Objects[Identifier]

    @field_validator("SupportedLiquidClassCategories", mode="after")
    def __SupportedLiquidClassCategoriesValdate(cls, v):
        for Category in v:
            v[Category] = sorted(v[Category], key=lambda x: x.MaxVolume)

        return v

    def IsLiquidClassCategorySupported(self, Category: str) -> bool:
        return Category in self.SupportedLiquidClassCategories
