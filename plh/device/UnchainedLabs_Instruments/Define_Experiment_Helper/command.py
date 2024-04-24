from __future__ import annotations

import dataclasses
from typing import Any

from plh.device.tools import CommandOptionsListMixin
from plh.device.UnchainedLabs_Instruments.backend import UnchainedLabsCommandBase

from .options import OptionsList


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandBase, CommandOptionsListMixin[OptionsList]):
    def execute_command_helper(self: Command, stunner_dll_object) -> Any:
        column_source_plate = -1
        column_source_position = -1
        blank_plate_id = ""
        blank_plate_position = ""
        stored_blanks_sample_group_name = ""
        column_stored_blanks_sample_group_name = -1
        # Do not use so set as default

        plate_info: dict[str, tuple[str, str]] = {
            Opt.sample_name: (Opt.sample_plate_id, Opt.sample_plate_position)
            for Opt in self.options
        }

        blanks = [
            Opt.blank_sample_name
            for Opt in self.options
            if Opt.blank_sample_name is not None
        ]

        if all(Blank is None for Blank in blanks):
            blanking_information = 0
            blank_name_used = ""
            # If no blanks then we are going to autoblank
        elif not all(Blank is not None for Blank in blanks):
            return Exception("Incorrect options")
            # Blanking is either all our none.
        elif len(set(blanks)) == 1 and len(self.options) != len(
            set(plate_info.keys()),
        ):
            blanking_information = 1
            blank_name_used = blanks[0]
            # All blank names are the same but we have more than one blank sample. Average
        elif len(set(blanks)) == 1:
            blanking_information = 2
            blank_name_used = blanks[0]
            # We only have one blank across all samples so single blank
        else:
            blanking_information = 3
            blank_name_used = ""

            # All blank names are not the same. Custom blank per sample.
        # determine how we are going to blank.

        column_sample_name = 0
        column_plate_id = 1
        column_plate_position = 2
        column_sample_group = 3
        column_analyte = 4
        column_buffer = 5
        column_e1 = 6
        if blanking_information == 3:
            column_blank_plate_id = 7
            column_blank_plate_position = 8
        else:
            column_blank_plate_id = -1
            column_blank_plate_position = -1
        # Define our columns

        sample_definition = ""
        for opt in self.options:
            line = []
            line.append(opt.sample_name)
            line.append(opt.sample_plate_id)
            line.append(opt.sample_plate_position)
            line.append(f"SG{opt.sample_group}")
            line.append(str(opt.analyte_meta_data))
            line.append(str(opt.buffer_meta_data))
            line.append(str(opt.extinction_coefficient * 10))

            if blanking_information == 3:
                line.append(plate_info[str(opt.blank_sample_name)][0])
                line.append(plate_info[str(opt.blank_sample_name)][1])

            sample_definition += ",".join(line) + "\n"
        # Assemble Sample Definition

        experiment_definition = "[Experiment definition]"
        experiment_definition += "\n"
        experiment_definition += f'experiment_name="{self.options.experiment_name}"'
        experiment_definition += "\n"
        experiment_definition += (
            f'application_name="{self.options.application_name.value}"'
        )
        experiment_definition += "\n"
        experiment_definition += 'dropplate_type="Stunner Plate"'
        experiment_definition += "\n"
        experiment_definition += "\n"
        experiment_definition += "[Import samples]"
        experiment_definition += "\n"
        experiment_definition += f"column_source_plate={column_source_plate}"
        experiment_definition += "\n"
        experiment_definition += f"column_source_position={column_source_position}"
        experiment_definition += "\n"
        experiment_definition += f"column_plate_ID={column_plate_id}"
        experiment_definition += "\n"
        experiment_definition += f"column_plate_position={column_plate_position}"
        experiment_definition += "\n"
        experiment_definition += f"column_sample_name={column_sample_name}"
        experiment_definition += "\n"
        experiment_definition += f"column_blank_plate_ID={column_blank_plate_id}"
        experiment_definition += "\n"
        experiment_definition += (
            f"column_blank_plate_position={column_blank_plate_position}"
        )
        experiment_definition += "\n"
        experiment_definition += f"column_sample_group={column_sample_group}"
        experiment_definition += "\n"
        experiment_definition += f"column_analyte={column_analyte}"
        experiment_definition += "\n"
        experiment_definition += f"column_buffer={column_buffer}"
        experiment_definition += "\n"
        experiment_definition += f"column_E1%={column_e1}"
        experiment_definition += "\n"
        experiment_definition += f"blanking_information={blanking_information}"
        experiment_definition += "\n"
        experiment_definition += f'blank_plate_ID="{blank_plate_id}"'
        experiment_definition += "\n"
        experiment_definition += f'blank_plate_position="{blank_plate_position}"'
        experiment_definition += "\n"
        experiment_definition += f'blank_name_used="{blank_name_used}"'
        experiment_definition += "\n"
        experiment_definition += (
            f'stored_blanks_sample_group_name="{stored_blanks_sample_group_name}"'
        )
        experiment_definition += "\n"
        experiment_definition += f"column_stored_blanks_sample_group_name={column_stored_blanks_sample_group_name}"
        # Assemble Experiment Definition

        return {
            "status_code_raw": 0,
            "experiment_definition": experiment_definition,
            "sample_definition": sample_definition,
        }
