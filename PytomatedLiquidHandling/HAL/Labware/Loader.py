import os

import yaml

from ...Tools.Logger import Logger
from . import NonPipettableLabware, PipettableLabware
from .BaseLabware import Dimensions, TransportOffsets, WellEquation, Wells, LabwareABC


def LoadYaml(LoggerInstance: Logger, FilePath: str) -> dict[str, LabwareABC]:
    LoggerInstance.info("Loading Labware config yaml file.")

    Labwares: dict[str, LabwareABC] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return Labwares

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return Labwares

    for Labware in ConfigFile:
        if Labware["Enabled"] == False:
            LoggerInstance.warning(
                "Labware"
                + " with unique ID "
                + Labware["Identifier"]
                + " is not enabled so will be skipped."
            )
            continue

        Identifier = Labware["Identifier"]
        ImageFilename = Labware["Image Filename"]
        LongSide = Labware["Dimensions"]["Long Side"]
        ShortSide = Labware["Dimensions"]["Short Side"]
        OpenOffset = Labware["Transport Offsets"]["Open"]
        CloseOffset = Labware["Transport Offsets"]["Close"]
        FromTopOffset = Labware["Transport Offsets"]["Distance From Top"]
        FromBottomOffset = Labware["Transport Offsets"]["Distance From Bottom"]

        DimensionsInstance = Dimensions(LongSide, ShortSide)
        # Create Dimensions Class

        TransportOffsetsInstance = TransportOffsets(
            OpenOffset, CloseOffset, FromTopOffset, FromBottomOffset
        )

        if "Wells" in Labware:
            LabwareWells = Labware["Wells"]

            Columns = LabwareWells["Columns"]
            Rows = LabwareWells["Rows"]
            SequencesPerWell = LabwareWells["Sequences Per Well"]
            MaxVolume = LabwareWells["Max Volume"]
            DeadVolume = LabwareWells["Dead Volume"]

            WellEquations: list[WellEquation] = list()
            for Segment in LabwareWells["Segment Equations"]:
                WellEquations.append(
                    WellEquation(Segment["Segment Height"], Segment["Segment Equation"])
                )
            # Create WellsEquation Class List

            WellsInstance = Wells(
                Columns,
                Rows,
                SequencesPerWell,
                MaxVolume,
                DeadVolume,
                WellEquations,
            )
            # Create Wells Class
            LabwareInstance = PipettableLabware(
                Identifier,
                ImageFilename,
                DimensionsInstance,
                TransportOffsetsInstance,
                WellsInstance,
            )

        else:
            LabwareInstance = NonPipettableLabware(
                Identifier,
                ImageFilename,
                DimensionsInstance,
                TransportOffsetsInstance,
            )

        Labwares[Identifier] = LabwareInstance

        # Create Labware Class and append

    return Labwares


# Populate list of Items
