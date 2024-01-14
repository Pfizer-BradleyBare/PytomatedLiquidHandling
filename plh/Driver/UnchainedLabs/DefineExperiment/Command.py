import dataclasses
from typing import Any

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import (
    CommandOptionsListMixin,
)

from ..Backend import UnchainedLabsCommandABC
from .options import ListedOptions


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandABC, CommandOptionsListMixin[ListedOptions]):
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        ColumnSourcePlate = -1
        ColumnSourcePosition = -1
        BlankPlateID = ""
        BlankPlatePosition = ""
        StoredBlanksSampleGroupName = ""
        ColumnStoredBlanksSampleGroupName = -1
        # Do not use so set as default

        PlateInfo: dict[str, tuple[str, str]] = {
            Opt.SampleName: (Opt.SamplePlateID, Opt.SamplePlatePosition)
            for Opt in self.Options
        }

        Blanks = [
            Opt.BlankSampleName
            for Opt in self.Options
            if Opt.BlankSampleName is not None
        ]

        if all(Blank is None for Blank in Blanks):
            BlankingInformation = 0
            BlankNameUsed = ""
            # If no blanks then we are going to autoblank
        elif not all(Blank is not None for Blank in Blanks):
            return Exception("Incorrect options")
            # Blanking is either all our none.
        else:
            if len(set(Blanks)) == 1 and len(self.Options) != len(
                set(PlateInfo.keys()),
            ):
                BlankingInformation = 1
                BlankNameUsed = Blanks[0]
                # All blank names are the same but we have more than one blank sample. Average
            elif len(set(Blanks)) == 1:
                BlankingInformation = 2
                BlankNameUsed = Blanks[0]
                # We only have one blank across all samples so single blank
            else:
                BlankingInformation = 3
                BlankNameUsed = ""

                # All blank names are not the same. Custom blank per sample.
        # determine how we are going to blank.

        ColumnSampleName = 0
        ColumnPlateID = 1
        ColumnPlatePosition = 2
        ColumnSampleGroup = 3
        ColumnAnalyte = 4
        ColumnBuffer = 5
        ColumnE1 = 6
        if BlankingInformation == 3:
            ColumnBlankPlateID = 7
            ColumnBlankPlatePosition = 8
        else:
            ColumnBlankPlateID = -1
            ColumnBlankPlatePosition = -1
        # Define our columns

        SampleDefinition = ""
        for Opt in self.Options:
            Line = []
            Line.append(Opt.SampleName)
            Line.append(Opt.SamplePlateID)
            Line.append(Opt.SamplePlatePosition)
            Line.append(f"SG{Opt.SampleGroup}")
            Line.append(str(Opt.AnalyteMetaData))
            Line.append(str(Opt.BufferMetaData))
            Line.append(str(Opt.ExtinctionCoefficient * 10))

            if BlankingInformation == 3:
                Line.append(PlateInfo[str(Opt.BlankSampleName)][0])
                Line.append(PlateInfo[str(Opt.BlankSampleName)][1])

            SampleDefinition += ",".join(Line) + "\n"
        # Assemble Sample Definition

        ExperimentDefinition = "[Experiment definition]"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f'experiment_name="{self.Options.ExperimentName}"'
        ExperimentDefinition += "\n"
        ExperimentDefinition += (
            f'application_name="{self.Options.ApplicationName.value}"'
        )
        ExperimentDefinition += "\n"
        ExperimentDefinition += 'dropplate_type="Stunner Plate"'
        ExperimentDefinition += "\n"
        ExperimentDefinition += "\n"
        ExperimentDefinition += "[Import samples]"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_source_plate={ColumnSourcePlate}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_source_position={ColumnSourcePosition}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_plate_ID={ColumnPlateID}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_plate_position={ColumnPlatePosition}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_sample_name={ColumnSampleName}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_blank_plate_ID={ColumnBlankPlateID}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += (
            f"column_blank_plate_position={ColumnBlankPlatePosition}"
        )
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_sample_group={ColumnSampleGroup}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_analyte={ColumnAnalyte}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_buffer={ColumnBuffer}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_E1%={ColumnE1}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"blanking_information={BlankingInformation}"
        ExperimentDefinition += "\n"
        ExperimentDefinition += f'blank_plate_ID="{BlankPlateID}"'
        ExperimentDefinition += "\n"
        ExperimentDefinition += f'blank_plate_position="{BlankPlatePosition}"'
        ExperimentDefinition += "\n"
        ExperimentDefinition += f'blank_name_used="{BlankNameUsed}"'
        ExperimentDefinition += "\n"
        ExperimentDefinition += (
            f'stored_blanks_sample_group_name="{StoredBlanksSampleGroupName}"'
        )
        ExperimentDefinition += "\n"
        ExperimentDefinition += f"column_stored_blanks_sample_group_name={ColumnStoredBlanksSampleGroupName}"
        # Assemble Experiment Definition

        StatusCode, DefinedPlateIDs = StunnerDLLObject.Define_Experiment(
            ExperimentDefinition,
            SampleDefinition,
        )

        return dict(StatusCode=StatusCode, DefinedPlateIDs=DefinedPlateIDs)
