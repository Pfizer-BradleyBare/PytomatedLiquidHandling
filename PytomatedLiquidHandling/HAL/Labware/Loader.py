import os

import yaml

from . import LabwareTracker, NonPipettableLabware, PipettableLabware
from .BaseLabware import (
    Dimensions,
    TransportOffsets,
    WellEquation,
    WellEquationTracker,
    Wells,
)


def LoadYaml(FilePath: str) -> LabwareTracker:
    LabwareTrackerInstance = LabwareTracker()

    if not os.path.exists(FilePath):
        return LabwareTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        return LabwareTrackerInstance

    for Labware in ConfigFile:
        if Labware["Enabled"] == False:
            continue

        UniqueIdentifier = Labware["Unique Identifier"]
        ImageFilename = Labware["Image Filename"]
        LongSide = Labware["Dimensions"]["Long Side"]
        ShortSide = Labware["Dimensions"]["Short Side"]
        OpenOffset = Labware["Transport Offsets"]["Open"]
        CloseOffset = Labware["Transport Offsets"]["Close"]
        HeightOffset = Labware["Transport Offsets"]["Height"]

        DimensionsInstance = Dimensions(LongSide, ShortSide)
        # Create Dimensions Class

        TransportOffsetsInstance = TransportOffsets(
            OpenOffset, CloseOffset, HeightOffset
        )

        if "Wells" in Labware:
            LabwareWells = Labware["Wells"]

            Columns = LabwareWells["Columns"]
            Rows = LabwareWells["Rows"]
            SequencesPerWell = LabwareWells["Sequences Per Well"]
            MaxVolume = LabwareWells["Max Volume"]
            DeadVolume = LabwareWells["Dead Volume"]

            WellEquationTrackerInstance = WellEquationTracker()
            for Segment in LabwareWells["Segment Equations"]:
                WellEquationTrackerInstance.LoadSingle(
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
                UniqueIdentifier,
                ImageFilename,
                DimensionsInstance,
                TransportOffsetsInstance,
                WellsInstance,
            )

        else:
            LabwareInstance = NonPipettableLabware(
                UniqueIdentifier,
                ImageFilename,
                DimensionsInstance,
                TransportOffsetsInstance,
            )

        LabwareTrackerInstance.LoadSingle(LabwareInstance)

        # Create Labware Class and append

    return LabwareTrackerInstance


# Populate list of Items
