import yaml

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ..Backend import BackendTracker
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..Tip.BaseTip import Tip, TipTracker
from .BasePipette import (
    LiquidClass,
    LiquidClassCategory,
    LiquidClassCategoryTracker,
    Pipette,
    PipetteTip,
    PipetteTipTracker,
)
from . import PipetteTracker
from .HamiltonCORE96Head import HamiltonCORE96Head
from .HamiltonPortraitCORE8Channel import HamiltonPortraitCORE8Channel


def LoadYaml(
    BackendTrackerInstance: BackendTracker,
    DeckLocationTrackerInstance: DeckLocationTracker,
    LabwareTrackerInstance: LabwareTracker,
    TipTrackerInstance: TipTracker,
    FilePath: str,
) -> PipetteTracker:
    PipetteTrackerInstance = PipetteTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    PipetteDevices: dict[int, Pipette] = dict()
    for DeviceType in ConfigFile:
        for Device in ConfigFile[DeviceType]:
            if Device["Enabled"] == False:
                continue

            UniqueIdentifier = Device["Unique Identifier"]
            BackendIdentifier = Device["Backend Unique Identifier"]
            BackendInstance = BackendTrackerInstance.GetObjectByName(BackendIdentifier)
            CustomErrorHandling = Device["Custom Error Handling"]
            NumberOfChannels = Device["Number of Channels"]

            SupportedLabwareTrackerInstance = LabwareTracker()
            for LabwareIdentifier in Device["Supported Labware Unique Identifiers"]:
                SupportedLabwareTrackerInstance.LoadSingle(
                    LabwareTrackerInstance.GetObjectByName(LabwareIdentifier)
                )

            SupportedDeckLocationTrackerInstance = DeckLocationTracker()
            for DeckLocationIdentifier in Device[
                "Supported Deck Location Unique Identifier"
            ]:
                SupportedDeckLocationTrackerInstance.LoadSingle(
                    DeckLocationTrackerInstance.GetObjectByName(DeckLocationIdentifier)
                )

            PipetteTipTrackerInstance = PipetteTipTracker()
            Tips: dict[float, PipetteTip] = dict()
            for TipDevice in Device["Supported Tips"]:
                TipIdentifier = TipDevice["Tip Unique Identifier"]
                DropoffSequence = TipDevice["Tip Support Dropoff Sequence"]
                PickupSequence = TipDevice["Tip Support Pickup Sequence"]
                WasteSequence = TipDevice["Waste Sequence"]
                TipInstance = TipTrackerInstance.GetObjectByName(TipIdentifier)
                Tips[TipInstance.MaxVolume] = PipetteTip(
                    TipInstance, DropoffSequence, PickupSequence, WasteSequence
                )

            for Volume, PipetteTipInstance in sorted(
                Tips.items()
            ):  # Note the () after items!
                PipetteTipTrackerInstance.LoadSingle(PipetteTipInstance)
            # This sorts the liquid class volumes from smallest to largest

            LiquidClassCategoryTrackerInstance = LiquidClassCategoryTracker()
            for Category in Device["Supported Liquid Class Categories"]:
                CategoryID = Category["Unique Identifier"]

                LiquidClassCategoryInstance = LiquidClassCategory(CategoryID)
                LiquidClasses: dict[float, LiquidClass] = dict()
                for Class in Category["Liquid Classes"]:
                    ClassIdentifier = Class["Unique Identifier"]
                    ClassMaxVolume = Class["Max Volume"]

                    LiquidClasses[ClassMaxVolume] = LiquidClass(
                        ClassIdentifier, ClassMaxVolume
                    )

                for Volume, LiquidClassInstance in sorted(
                    LiquidClasses.items()
                ):  # Note the () after items!
                    LiquidClassCategoryInstance.LoadSingle(LiquidClassInstance)
                # This sorts the liquid class volumes from smallest to largest

                LiquidClassCategoryTrackerInstance.LoadSingle(
                    LiquidClassCategoryInstance
                )

            if DeviceType == "Hamilton 96 Core Head":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Wrong backend selected")

                PipetteDevices[NumberOfChannels] = HamiltonCORE96Head(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    PipetteTipTrackerInstance,
                    LabwareTrackerInstance,
                    DeckLocationTrackerInstance,
                    LiquidClassCategoryTrackerInstance,
                )

            elif DeviceType == "Hamilton 1mL Channels Portrait":
                ActiveChannels = Device["Active Channels"]

                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Wrong backend selected")

                PipetteDevices[NumberOfChannels] = HamiltonPortraitCORE8Channel(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    PipetteTipTrackerInstance,
                    LabwareTrackerInstance,
                    DeckLocationTrackerInstance,
                    LiquidClassCategoryTrackerInstance,
                    ActiveChannels,
                )
            else:
                raise Exception("Device type not recognized")

    for NumberOfChannels, PipetteInstance in sorted(
        PipetteDevices.items(), reverse=True
    ):  # Note the () after items!
        PipetteTrackerInstance.LoadSingle(PipetteInstance)
    # This sorts the devices by number of channels from largest to smallest.

    return PipetteTrackerInstance
