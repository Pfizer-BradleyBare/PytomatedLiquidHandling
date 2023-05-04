import yaml

from ..Labware import LabwareTracker
from ..Pipette import Pipette8Channel, Pipette96Channel
from ..Tip.BaseTip import TipTracker
from .BasePipette import (
    LiquidClass,
    LiquidClassCategory,
    LiquidClassCategoryTracker,
    PipetteTip,
    PipetteTipTracker,
    PipetteTracker,
    PipettingDeviceTypes,
)


def LoadYaml(
    TipTrackerInstance: TipTracker,
    LabwareTrackerInstance: LabwareTracker,
    FilePath: str,
) -> PipetteTracker:
    PipetteTrackerInstance = PipetteTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for Device in ConfigFile["Device IDs"]:
        Enabled = ConfigFile["Device IDs"][Device]["Enabled"]

        if ConfigFile["Device IDs"][Device]["Enabled"] is True:

            SupportedLabwareTrackerInstance = LabwareTracker()

            for LabwareName in ConfigFile["Device IDs"][Device]["Supported Labware"]:
                SupportedLabwareTrackerInstance.LoadSingle(
                    LabwareTrackerInstance.GetObjectByName(LabwareName)
                )

            PipetteTipTrackerInstance = PipetteTipTracker()

            for Tip in ConfigFile["Device IDs"][Device]["Supported Tips"]:

                TipInstance = TipTrackerInstance.GetObjectByName(Tip)
                PickupSequence = ConfigFile["Device IDs"][Device]["Supported Tips"][
                    Tip
                ]["Pickup Sequence"]
                DropoffSequence = ConfigFile["Device IDs"][Device]["Supported Tips"][
                    Tip
                ]["Drop Off Sequence"]
                WasteSequence = ConfigFile["Device IDs"][Device]["Supported Tips"][Tip][
                    "Waste Sequence"
                ]

                LiquidClassCategoryTrackerInstance = LiquidClassCategoryTracker()

                for LiquidClassID in ConfigFile["Device IDs"][Device]["Supported Tips"][
                    Tip
                ]["Liquid Class IDs"]:
                    LiquidClassCategoryInstance = LiquidClassCategory(LiquidClassID)

                    for LiquidClassItem in ConfigFile["Device IDs"][Device][
                        "Supported Tips"
                    ][Tip]["Liquid Class IDs"][LiquidClassID]:

                        MaxVolume = LiquidClassItem["Max Volume"]

                        Name = LiquidClassItem["Liquid Class"]

                        LiquidClassCategoryInstance.LoadSingle(
                            LiquidClass(Name, MaxVolume)
                        )

                    LiquidClassCategoryTrackerInstance.LoadSingle(
                        LiquidClassCategoryInstance
                    )

                PipetteTipTrackerInstance.LoadSingle(
                    PipetteTip(
                        TipInstance,
                        LiquidClassCategoryTrackerInstance,
                        PickupSequence,
                        DropoffSequence,
                        WasteSequence,
                    )
                )

            PipetteDeviceType = PipettingDeviceTypes(Device)

            if PipetteDeviceType == PipettingDeviceTypes.Pipette8Channel:

                PipetteTrackerInstance.LoadSingle(
                    Pipette8Channel(
                        Enabled,
                        PipetteTipTrackerInstance,
                        SupportedLabwareTrackerInstance,
                        ConfigFile["Device IDs"][Device]["Active Channels"],
                    )
                )

            if PipetteDeviceType == PipettingDeviceTypes.Pipette96Channel:
                PipetteTrackerInstance.LoadSingle(
                    Pipette96Channel(
                        Enabled,
                        PipetteTipTrackerInstance,
                        SupportedLabwareTrackerInstance,
                    )
                )

    return PipetteTrackerInstance
