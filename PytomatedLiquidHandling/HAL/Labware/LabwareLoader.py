import yaml

from ..Labware import LabwareTracker, NonPipettableLabware, PipettableLabware
from .BaseLabware import Dimensions, WellEquation, WellEquationTracker, Wells


def LoadYaml(FilePath: str) -> LabwareTracker:
    LabwareTrackerInstance = LabwareTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for LabwareID in ConfigFile["Labware IDs"]:

        LongSide = ConfigFile["Labware IDs"][LabwareID]["Dimensions"]["Long Side"]
        ShortSide = ConfigFile["Labware IDs"][LabwareID]["Dimensions"]["Short Side"]
        DimensionsInstance = Dimensions(LongSide, ShortSide)
        # Create Dimensions Class

        Filters = ConfigFile["Labware IDs"][LabwareID]["Labware Filter"]

        if "Wells" in ConfigFile["Labware IDs"][LabwareID].keys():

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
            LabwareInstance = PipettableLabware(
                LabwareID, Filters, DimensionsInstance, WellsInstance
            )

        else:
            LabwareInstance = NonPipettableLabware(
                LabwareID, Filters, DimensionsInstance
            )

        LabwareTrackerInstance.ManualLoad(LabwareInstance)

        # Create Labware Class and append

    return LabwareTrackerInstance


# Populate list of Items
