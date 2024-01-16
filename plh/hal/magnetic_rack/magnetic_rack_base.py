from __future__ import annotations

from pydantic import ValidationInfo, dataclasses, field_validator

from plh.hal import labware, pipette
from plh.hal import layout_item as li
from plh.hal.tools import HALDevice


@dataclasses.dataclass(kw_only=True)
class MagneticRackBase(HALDevice):
    supported_plates: list[li.CoverablePlate | li.Plate]
    supported_pipettes: list[pipette.PipetteBase]

    @field_validator("SupportedPlates", mode="before")
    @classmethod
    def __supported_plates_validate(
        cls: type[MagneticRackBase],
        v: list[str | li.LayoutItemBase],
    ) -> list[li.CoverablePlate | li.Plate]:
        supported_objects = []

        objects = li.devices

        for item in v:
            if isinstance(item, li.LayoutItemBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + li.LayoutItemBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

    @field_validator("SupportedPipettes", mode="before")
    # TODO
    def __supported_pipettes_validate(cls, v, info: ValidationInfo):
        SupportedObjects = []

        Objects = Pipette.Devices

        for Item in v:
            Identifier = Item["Pipette"]
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + Pipette.Base.PipetteBase.__name__
                    + " objects.",
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
                            Tip.SupportedLiquidClassCategories[CategoryName] = []
                        Tip.SupportedLiquidClassCategories[CategoryName].append(
                            LiquidClass,
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
                            Tip.SupportedLiquidClassCategories[CategoryName] = []
                        Tip.SupportedLiquidClassCategories[CategoryName].append(
                            LiquidClass,
                        )
                        Tip.SupportedLiquidClassCategories[CategoryName] = sorted(
                            Tip.SupportedLiquidClassCategories[CategoryName],
                            key=lambda x: x.MaxVolume,
                        )
                        break

            SupportedObjects.append(Object)

        return SupportedObjects

    def get_layout_item(
        self: MagneticRackBase,
        layout_item: li.CoverablePlate | li.Plate,
    ) -> li.CoverablePlate | li.Plate:
        for supported_layout_item in self.supported_plates:
            if supported_layout_item.labware == layout_item.labware:
                if isinstance(supported_layout_item, li.CoverablePlate):
                    if isinstance(layout_item, li.CoverablePlate):
                        supported_layout_item.is_covered = layout_item.is_covered
                    else:
                        supported_layout_item.is_covered = False

                return supported_layout_item

        raise labware.LabwareNotSupportedError([layout_item.labware])

    def get_aspirate_storage_buffer_liquid_class_category(
        self: MagneticRackBase,
    ) -> str:
        return "MagneticRack: " + self.identifier + " Aspirate"

    def get_add_storage_buffer_liquid_class_category(self: MagneticRackBase) -> str:
        return "MagneticRack: " + self.identifier + " Dispense"
