from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import dataclasses

from .labware_base import LabwareBase

if TYPE_CHECKING:
    from .well import Well


@dataclasses.dataclass(kw_only=True)
class PipettableLabware(LabwareBase):
    well_definition: Well

    def get_height_from_volume(self: PipettableLabware, volume: float) -> float:
        calculated_height = 0.0

        segments = self.well_definition.segments

        while True:
            temp_height = calculated_height
            calculated_volume = 0
            # reset each round

            for segment in segments:
                segment_height = segment.height
                eval_height = temp_height

                if eval_height > segment_height:
                    eval_height = segment_height
                # Make sure we do not exceed the segment height during the calc

                calculated_volume += eval(  # noqa:PGH001 S307
                    segment.equation,
                    {},
                    {"h": eval_height},
                )
                temp_height -= segment_height

                if temp_height <= 0:
                    break

            if calculated_volume >= volume or temp_height > 0:
                break

            calculated_height += 0.1

        return calculated_height

    def get_volume_from_height(self: PipettableLabware, height: float) -> float:
        segments = self.well_definition.segments
        calculated_volume = 0

        for segment in segments:
            segment_height = segment.height

            eval_height = segment_height if height > segment_height else height

            height -= segment_height

            calculated_volume += eval(  # noqa:PGH001 S307
                segment.equation,
                {},
                {"h": eval_height},
            )

        return calculated_volume