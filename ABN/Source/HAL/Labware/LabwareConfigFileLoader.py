import yaml
from .Labware import (
    Labware,
    PipettableLabware,
    LabwareDimensions,
    LabwareFilters,
    Wells,
    WellsEquation,
)
from .LabwareTracker import LabwareTracker


def LoadYaml(LabwareTrackerInstance: LabwareTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for LabwareID in ConfigFile["Labware IDs"]:

        LongSide = ConfigFile["Labware IDs"][LabwareID]["Dimensions"]["Long Side"]
        ShortSide = ConfigFile["Labware IDs"][LabwareID]["Dimensions"]["Short Side"]
        Dimensions = LabwareDimensions(LongSide, ShortSide)
        # Create Dimensions Class

        Filter = LabwareFilters(ConfigFile["Labware IDs"][LabwareID]["Labware Filter"])

        if "Wells" in ConfigFile["Labware IDs"][LabwareID].keys():
            EquationsList = list()
            SegmentEquations = ConfigFile["Labware IDs"][LabwareID]["Wells"][
                "Segment Equations"
            ]
            for Segment in SegmentEquations:
                EquationsList.append(
                    WellsEquation(
                        Segment["Segment Height"], Segment["Segment Equation"]
                    )
                )
            # Create WellsEquation Class List

            Columns = ConfigFile["Labware IDs"][LabwareID]["Wells"]["Columns"]
            Rows = ConfigFile["Labware IDs"][LabwareID]["Wells"]["Rows"]
            SequencesPerWell = ConfigFile["Labware IDs"][LabwareID]["Wells"][
                "Sequences Per Well"
            ]
            MaxVolume = ConfigFile["Labware IDs"][LabwareID]["Wells"]["Max Volume"]
            DeadVolume = ConfigFile["Labware IDs"][LabwareID]["Wells"]["Dead Volume"]

            LabwareWells = Wells(
                Columns,
                Rows,
                SequencesPerWell,
                MaxVolume,
                DeadVolume,
                EquationsList,
            )
            # Create Wells Class

            LabwareTrackerInstance.LoadManual(
                PipettableLabware(
                    LabwareID,
                    Filter,
                    LabwareWells,
                    Dimensions,
                )
            )
        else:
            LabwareTrackerInstance.LoadManual(Labware(LabwareID, Filter, Dimensions))

        # Create Labware Class and append


# Populate list of Items
