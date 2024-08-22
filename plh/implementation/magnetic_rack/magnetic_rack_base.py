from __future__ import annotations

from typing import Annotated

from pydantic import ValidationInfo, dataclasses, field_validator
from pydantic.functional_validators import BeforeValidator

from plh.implementation import labware, pipette
from plh.implementation import layout_item as li
from plh.implementation.tools import Resource


@dataclasses.dataclass(kw_only=True, eq=False)
class MagneticRackBase(Resource):
    """A magnetic rack to be used for condensing magnetic beads."""

    plates: Annotated[
        list[li.CoverablePlateBase | li.PlateBase],
        BeforeValidator(li.validate_list),
    ]
    """Supported plates."""

    pipettes: list[pipette.PipetteBase]
    """Supported pipettes."""

    @field_validator("pipettes", mode="before")
    @classmethod
    def __pipettes_validate(
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
                    min_volume=pipette_config["MinVolume"],
                )
                for tip in pipette_object.supported_tips:
                    if tip.tip.volume >= liquid_class.max_volume:
                        category_name = (
                            "MagneticRack: " + info.data["Identifier"] + " Aspirate"
                        )

                        if (
                            category_name
                            not in tip.supported_aspirate_liquid_class_categories
                        ):
                            tip.supported_aspirate_liquid_class_categories[
                                category_name
                            ] = []

                        tip.supported_aspirate_liquid_class_categories[
                            category_name
                        ].append(
                            liquid_class,
                        )
                        tip.supported_aspirate_liquid_class_categories[
                            category_name
                        ] = sorted(
                            tip.supported_aspirate_liquid_class_categories[
                                category_name
                            ],
                            key=lambda x: x.max_volume,
                        )

                        break

            for pipette_config in item["liquid_classes"]["Dispense"]:
                liquid_class = pipette.LiquidClass(
                    liquid_class_name=pipette_config["LiquidClassName"],
                    max_volume=pipette_config["MaxVolume"],
                    min_volume=pipette_config["MinVolume"],
                )
                for tip in pipette_object.supported_tips:
                    if tip.tip.volume >= liquid_class.max_volume:
                        category_name = (
                            "MagneticRack: " + info.data["Identifier"] + " Dispense"
                        )

                        if (
                            category_name
                            not in tip.supported_dispense_liquid_class_categories
                        ):
                            tip.supported_dispense_liquid_class_categories[
                                category_name
                            ] = []

                        tip.supported_dispense_liquid_class_categories[
                            category_name
                        ].append(
                            liquid_class,
                        )
                        tip.supported_dispense_liquid_class_categories[
                            category_name
                        ] = sorted(
                            tip.supported_dispense_liquid_class_categories[
                                category_name
                            ],
                            key=lambda x: x.max_volume,
                        )
                        break

            supported_objects.append(pipette_object)

        return supported_objects

    def assert_supported_labware(
        self: MagneticRackBase,
        *args: labware.LabwareBase,
    ) -> None:
        supported_labware = [item.labware for item in self.plates]

        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in supported_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def get_layout_item(
        self: MagneticRackBase,
        labware: labware.LabwareBase,
    ) -> li.CoverablePlateBase | li.PlateBase:
        self.assert_supported_labware(labware)

        for supported_layout_item in self.plates:
            if supported_layout_item.labware == labware:
                return supported_layout_item

        msg = "Should never reach this point."
        raise RuntimeError(msg)

    def get_aspirate_storage_buffer_liquid_class_category(
        self: MagneticRackBase,
    ) -> str:
        return "MagneticRack: " + self.identifier + " Aspirate"

    def get_add_storage_buffer_liquid_class_category(self: MagneticRackBase) -> str:
        return "MagneticRack: " + self.identifier + " Dispense"
