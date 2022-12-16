import yaml

from ..Labware import (
    Labware,
    LabwareDimensions,
    WellEquation,
    WellEquationTracker,
    Wells,
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

        Filter = None
        WellsInstance = None

        if "Wells" in ConfigFile["Labware IDs"][LabwareID].keys():
            Filter = ConfigFile["Labware IDs"][LabwareID]["Labware Filter"]

            EquationsList = list()
            WellEquationTrackerInstance = WellEquationTracker()
            SegmentEquations = ConfigFile["Labware IDs"][LabwareID]["Wells"][
                "Segment Equations"
            ]
            for Segment in SegmentEquations:
                WellEquationTrackerInstance.ManualLoad(
                    WellEquation(Segment["Segment Height"], Segment["Segment Equation"])
                )
            # Create WellsEquation Class List

            Columns = ConfigFile["Labware IDs"][LabwareID]["Wells"]["Columns"]
            Rows = ConfigFile["Labware IDs"][LabwareID]["Wells"]["Rows"]
            SequencesPerWell = ConfigFile["Labware IDs"][LabwareID]["Wells"][
                "Sequences Per Well"
            ]
            MaxVolume = ConfigFile["Labware IDs"][LabwareID]["Wells"]["Max Volume"]
            DeadVolume = ConfigFile["Labware IDs"][LabwareID]["Wells"]["Dead Volume"]

            WellsInstance = Wells(
                Columns,
                Rows,
                SequencesPerWell,
                MaxVolume,
                DeadVolume,
                WellEquationTrackerInstance,
            )
            # Create Wells Class

        LabwareTrackerInstance.ManualLoad(
            Labware(LabwareID, Filter, WellsInstance, Dimensions)
        )

        # Create Labware Class and append


# Populate list of Items
