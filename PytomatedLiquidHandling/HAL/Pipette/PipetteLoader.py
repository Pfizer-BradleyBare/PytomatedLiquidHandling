import yaml

from ..Labware import LabwareTracker
from ..DeckLocation import DeckLocationTracker
from ..Backend import BackendTracker
from .HamiltonCORE96Head import HamiltonCORE96Head
from .HamiltonPortraitCORE8Channel import HamiltonPortraitCORE8Channel
from ..Tip.BaseTip import TipTracker
from .BasePipette import (
    LiquidClass,
    LiquidClassCategory,
    LiquidClassCategoryTracker,
    PipetteTip,
    PipetteTipTracker,
    PipetteTracker,
    Pipette,
)
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


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
            for Tip in Device["Supported Tips"]:
                TipIdentifier = Tip["Tip Unique Identifier"]
                WasteSequence = Tip["Waste Sequence"]
                TipInstance = TipTrackerInstance.GetObjectByName(TipIdentifier)

                LiquidClassCategoryTrackerInstance = LiquidClassCategoryTracker()
                for Category in Tip["Liquid Class Categories"]:
                    CategoryID = Category["Unique Identifier"]

                    LiquidClassCategoryInstance = LiquidClassCategory(CategoryID)
                    for Class in Category["Liquid Classes"]:
                        ClassIdentifier = Class["Unique Identifier"]
                        ClassMaxVolume = Class["Max Volume"]

                        LiquidClassCategoryInstance.LoadSingle(
                            LiquidClass(ClassIdentifier, ClassMaxVolume)
                        )

                    LiquidClassCategoryTrackerInstance.LoadSingle(
                        LiquidClassCategoryInstance
                    )

                PipetteTipTrackerInstance.LoadSingle(
                    PipetteTip(
                        TipInstance, LiquidClassCategoryTrackerInstance, WasteSequence
                    )
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
