import os

import yaml

from ...Tools.Logger import Logger
from . import LabwareTracker, NonPipettableLabware, PipettableLabware
from .BaseLabware import (
    Dimensions,
    TransportOffsets,
    WellEquation,
    WellEquationTracker,
    Wells,
)


def LoadYaml(LoggerInstance: Logger, FilePath: str) -> LabwareTracker:
    LoggerInstance.info("Loading Labware config yaml file.")

    LabwareTrackerInstance = LabwareTracker()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return LabwareTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return LabwareTrackerInstance

    for Labware in ConfigFile:
        if Labware["Enabled"] == False:
            LoggerInstance.warning(
                "Labware"
                + " with unique ID "
                + Labware["Unique Identifier"]
                + " is not enabled so will be skipped."
            )
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
