import yaml

from ..Labware import LabwareTracker, NonPipettableLabware, PipettableLabware
from .BaseLabware import Dimensions, WellEquation, WellEquationTracker, Wells


def LoadYaml(FilePath: str) -> LabwareTracker:
    LabwareTrackerInstance = LabwareTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for Labware in ConfigFile:
        UniqueIdentifier = Labware["Unique Identifier"]
        LongSide = Labware["Dimensions"]["Long Side"]
        ShortSide = Labware["Dimensions"]["Short Side"]

        DimensionsInstance = Dimensions(LongSide, ShortSide)
        # Create Dimensions Class

        if "Wells" in Labware:
            LabwareWells = Labware["Wells"]

            Columns = LabwareWells["Columns"]
            Rows = LabwareWells["Rows"]
            SequencesPerWell = LabwareWells["Sequences Per Well"]
            MaxVolume = LabwareWells["Max Volume"]
            DeadVolume = LabwareWells["Dead Volume"]

            WellEquationTrackerInstance = WellEquationTracker()
            for Segment in LabwareWells["Segment Equations"]:
                WellEquationTrackerInstance.ManualLoad(
                    WellEquation(Segment["Segment Height"], Segment["Segment Equation"])
                )
            # Create WellsEquation Class List

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
                UniqueIdentifier, DimensionsInstance, WellsInstance
            )

        else:
            LabwareInstance = NonPipettableLabware(UniqueIdentifier, DimensionsInstance)

        LabwareTrackerInstance.ManualLoad(LabwareInstance)

        # Create Labware Class and append

    return LabwareTrackerInstance


# Populate list of Items
