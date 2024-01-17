from __future__ import annotations

from pydantic import ValidationInfo, dataclasses, field_validator

from plh.hal import labware, pipette
from plh.hal import layout_item as li
from plh.hal.tools import HALDevice


@dataclasses.dataclass(kw_only=True)
class MagneticRackBase(HALDevice):
    supported_plates: list[li.CoverablePlate | li.Plate]
    supported_pipettes: list[pipette.PipetteBase]

    @field_validator("supported_plates", mode="before")
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

    @field_validator("supported_pipettes", mode="before")
    @classmethod
    def __supported_pipettes_validate(
        cls: type[MagneticRackBase],
        v: list[dict],
        info: ValidationInfo,
    ) -> list[pipette.PipetteBase]:
        supported_objects = []

        objects = pipette.devices

        for item in v:
            if item["Pipette"] not in objects:
                raise ValueError(
                    item["Pipette"]
                    + " is not found in "
                    + pipette.PipetteBase.__name__
                    + " objects.",
                )

            pipette_object = objects[item["Pipette"]]

            for pipette_config in item["liquid_classes"]["Aspirate"]:
                liquid_class = pipette.LiquidClass(
                    liquid_class_name=pipette_config["LiquidClassName"],
                    max_volume=pipette_config["MaxVolume"],
                )
                for tip in pipette_object.supported_tips:
                    if tip.tip.volume >= liquid_class.max_volume:
                        category_name = (
                            "MagneticRack: " + info.data["Identifier"] + " Aspirate"
                        )

                        if category_name not in tip.supported_liquid_class_categories:
                            tip.supported_liquid_class_categories[category_name] = []

                        tip.supported_liquid_class_categories[category_name].append(
                            liquid_class,
                        )
                        tip.supported_liquid_class_categories[category_name] = sorted(
                            tip.supported_liquid_class_categories[category_name],
                            key=lambda x: x.max_volume,
                        )

                        break

            for pipette_config in item["liquid_classes"]["Dispense"]:
                liquid_class = pipette.LiquidClass(
                    liquid_class_name=pipette_config["LiquidClassName"],
                    max_volume=pipette_config["MaxVolume"],
                )
                for tip in pipette_object.supported_tips:
                    if tip.tip.volume >= liquid_class.max_volume:
                        category_name = (
                            "MagneticRack: " + info.data["Identifier"] + " Dispense"
                        )

                        if category_name not in tip.supported_liquid_class_categories:
                            tip.supported_liquid_class_categories[category_name] = []

                        tip.supported_liquid_class_categories[category_name].append(
                            liquid_class,
                        )
                        tip.supported_liquid_class_categories[category_name] = sorted(
                            tip.supported_liquid_class_categories[category_name],
                            key=lambda x: x.max_volume,
                        )
                        break

            supported_objects.append(pipette_object)

        return supported_objects

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
