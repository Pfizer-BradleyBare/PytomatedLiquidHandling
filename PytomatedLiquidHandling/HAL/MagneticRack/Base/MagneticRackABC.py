from pydantic import PrivateAttr, ValidationInfo, field_validator

from PytomatedLiquidHandling.HAL import LayoutItem, Pipette
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice


class MagneticRackABC(HALDevice):
    SupportedLayoutItems: list[LayoutItem.CoverablePlate | LayoutItem.Plate]
    SupportedPipettes: list[Pipette.Base.PipetteABC]

    @field_validator("SupportedLayoutItems", mode="before")
    def __SupportedLayoutItemsValidate(cls, v):
        SupportedObjects = list()

        Objects = LayoutItem.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + LayoutItem.Base.LayoutItemABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

    @field_validator("SupportedPipettes", mode="before")
    def __SupportedPipettesValidate(cls, v, info: ValidationInfo):
        SupportedObjects = list()

        Objects = Pipette.Devices

        for Item in v:
            Identifier = Item["Pipette"]
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + Pipette.Base.PipetteABC.__name__
                    + " objects."
                )
            Object = Objects[Identifier]

            for PipetteConfig in Item["LiquidClasses"]["Aspirate"]:
                LiquidClass = Pipette.Base.LiquidClass(
                    LiquidClassName=PipetteConfig["LiquidClassName"],
                    MaxVolume=PipetteConfig["MaxVolume"],
                )
                for Tip in Object.SupportedTips:
                    if Tip.Tip.Volume >= LiquidClass.MaxVolume:
                        CategoryName = (
                            "MagneticRack: " + info.data["Identifier"] + " Aspirate"
                        )

                        if CategoryName not in Tip.SupportedLiquidClassCategories:
                            Tip.SupportedLiquidClassCategories[CategoryName] = list()
                        Tip.SupportedLiquidClassCategories[CategoryName].append(
                            LiquidClass
                        )
                        Tip.SupportedLiquidClassCategories[CategoryName] = sorted(
                            Tip.SupportedLiquidClassCategories[CategoryName],
                            key=lambda x: x.MaxVolume,
                        )

                        break

            for PipetteConfig in Item["LiquidClasses"]["Dispense"]:
                LiquidClass = Pipette.Base.LiquidClass(
                    LiquidClassName=PipetteConfig["LiquidClassName"],
                    MaxVolume=PipetteConfig["MaxVolume"],
                )
                for Tip in Object.SupportedTips:
                    if Tip.Tip.Volume >= LiquidClass.MaxVolume:
                        CategoryName = (
                            "MagneticRack: " + info.data["Identifier"] + " Dispense"
                        )

                        if CategoryName not in Tip.SupportedLiquidClassCategories:
                            Tip.SupportedLiquidClassCategories[CategoryName] = list()
                        Tip.SupportedLiquidClassCategories[CategoryName].append(
                            LiquidClass
                        )
                        Tip.SupportedLiquidClassCategories[CategoryName] = sorted(
                            Tip.SupportedLiquidClassCategories[CategoryName],
                            key=lambda x: x.MaxVolume,
                        )
                        break

            SupportedObjects.append(Object)

        return SupportedObjects

    def GetLayoutItem(
        self,
        LayoutItemInstance: LayoutItem.CoverablePlate | LayoutItem.Plate,
    ) -> LayoutItem.CoverablePlate:
        for SupportedLayoutItemInstance in self.SupportedLayoutItems:
            if SupportedLayoutItemInstance.Labware == LayoutItemInstance.Labware:
                if not isinstance(
                    SupportedLayoutItemInstance, LayoutItem.CoverablePlate
                ):
                    raise Exception("This should never happen")

                if isinstance(LayoutItemInstance, LayoutItem.CoverablePlate):
                    SupportedLayoutItemInstance.IsCovered = LayoutItemInstance.IsCovered
                else:
                    SupportedLayoutItemInstance.IsCovered = False

                return SupportedLayoutItemInstance

        raise Exception("This rack does not support your layout item")

    def GetAspirateStorageBufferLiquidClassCategory(self):
        return "MagneticRack: " + self.Identifier + " Aspirate"

    def GetAddStorageBufferLiquidClassCategory(self):
        return "MagneticRack: " + self.Identifier + " Dispense"
