import os

import yaml

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, Tip

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Tools.Logger import Logger
from .BasePipette import LiquidClass, LiquidClassCategory, Pipette, PipetteTip
from .HamiltonCORE96Head import HamiltonCORE96Head
from .HamiltonPortraitCORE8Channel import HamiltonPortraitCORE8Channel


def LoadYaml(
    LoggerInstance: Logger,
    Backends: dict[str, BackendABC],
    DeckLocations: dict[str, DeckLocation.BaseDeckLocation.DeckLocationABC],
    Labwares: dict[str, Labware.BaseLabware.LabwareABC],
    Tips: dict[str, Tip.BaseTip.Tip],
    FilePath: str,
) -> dict[str, Pipette]:
    LoggerInstance.info("Loading Pipette config yaml file.")

    Pipettes: dict[str, Pipette] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return Pipettes

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return Pipettes

    PipetteDevices: dict[int, Pipette] = dict()
    for DeviceType in ConfigFile:
        for Device in ConfigFile[DeviceType]:
            if Device["Enabled"] == False:
                LoggerInstance.warning(
                    DeviceType
                    + " with unique ID "
                    + Device["Unique Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            Identifier = Device["Identifier"]
            BackendIdentifier = Device["Backend Identifier"]
            BackendInstance = Backends[BackendIdentifier]
            CustomErrorHandling = Device["Custom Error Handling"]
            NumberOfChannels = Device["Number of Channels"]

            SupportedLabwares: list[Labware.PipettableLabware] = list()
            for LabwareIdentifier in Device["Supported Labware Identifiers"]:
                LabwareInstance = Labwares[LabwareIdentifier]

                if not isinstance(LabwareInstance, Labware.PipettableLabware):
                    raise Exception("Only pipettable labware are supported")

                SupportedLabwares.append(LabwareInstance)

            SupportedDeckLocations: list[
                DeckLocation.BaseDeckLocation.DeckLocationABC
            ] = list()
            for DeckLocationIdentifier in Device["Supported Deck Location Identifiers"]:
                SupportedDeckLocations.append(DeckLocations[DeckLocationIdentifier])

            PipetteTips: list[PipetteTip] = list()
            for TipDevice in Device["Supported Tips"]:
                TipIdentifier = TipDevice["Tip Identifier"]
                DropoffSequence = TipDevice["Tip Support Dropoff Sequence"]
                PickupSequence = TipDevice["Tip Support Pickup Sequence"]
                WasteSequence = TipDevice["Waste Sequence"]
                PipetteTips.append(
                    PipetteTip(
                        Tips[TipIdentifier],
                        DropoffSequence,
                        PickupSequence,
                        WasteSequence,
                    )
                )

            LiquidClassCategories: list[LiquidClassCategory] = list()
            for Category in Device["Supported Liquid Class Categories"]:
                CategoryID = Category["Identifier"]

                LiquidClasses: list[LiquidClass] = list()
                for Class in Category["Liquid Classes"]:
                    ClassIdentifier = Class["Unique Identifier"]
                    ClassMaxVolume = Class["Max Volume"]

                    LiquidClasses.append(LiquidClass(ClassIdentifier, ClassMaxVolume))

                LiquidClassCategoryInstance = LiquidClassCategory(
                    CategoryID, LiquidClasses
                )

                LiquidClassCategories.append(LiquidClassCategoryInstance)

            if DeviceType == "Hamilton 96 Core Head":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Wrong backend selected")

                PipetteDevices[NumberOfChannels] = HamiltonCORE96Head(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    PipetteTips,
                    SupportedLabwares,
                    SupportedDeckLocations,
                    LiquidClassCategories,
                )

            elif DeviceType == "Hamilton 1mL Channels Portrait":
                ActiveChannels = Device["Active Channels"]

                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Wrong backend selected")

                PipetteDevices[NumberOfChannels] = HamiltonPortraitCORE8Channel(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    PipetteTips,
                    SupportedLabwares,
                    SupportedDeckLocations,
                    LiquidClassCategories,
                    ActiveChannels,
                )
            else:
                raise Exception("Device type not recognized")

    for NumberOfChannels, PipetteInstance in sorted(
        PipetteDevices.items(), reverse=True
    ):  # Note the () after items!
        Pipettes[PipetteInstance.Identifier] = PipetteInstance
    # This sorts the devices by number of channels from largest to smallest.

    return Pipettes
