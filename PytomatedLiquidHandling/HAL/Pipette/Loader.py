import os

import yaml
import logging
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, Tip

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from .Base import LiquidClass, LiquidClassCategory, PipetteABC, PipetteTip
from .HamiltonCORE96Head import HamiltonCORE96Head
from .HamiltonPortraitCORE8Channel import HamiltonPortraitCORE8Channel

Logger = logging.getLogger(__name__)


def LoadYaml(
    Backends: dict[str, BackendABC],
    DeckLocations: dict[str, DeckLocation.Base.DeckLocationABC],
    Labwares: dict[str, Labware.Base.LabwareABC],
    Tips: dict[str, Tip.Base.TipABC],
    FilePath: str,
) -> dict[str, PipetteABC]:
    Logger.info("Loading Pipette config yaml file.")

    Pipettes: dict[str, PipetteABC] = dict()

    if not os.path.exists(FilePath):
        Logger.warning("Config file does not exist. Skipped")
        return Pipettes

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        Logger.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return Pipettes

    PipetteDevices: dict[int, PipetteABC] = dict()
    for DeviceType in ConfigFile:
        for Device in ConfigFile[DeviceType]:
            if Device["Enabled"] == False:
                Logger.warning(
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

            SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC] = list()
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
