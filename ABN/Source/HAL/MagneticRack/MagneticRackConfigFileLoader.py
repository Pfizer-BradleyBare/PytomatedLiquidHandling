import yaml
from .MagneticRackTracker import MagneticRackTracker
from ..Layout import LayoutItem
from ..Pipette import PipettingDevice, PipettingTip, LiquidClass
from .MagneticRack import MagneticRack


def LoadYaml(MagneticRackTrackerInstance: MagneticRackTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for RackID in ConfigFile["Rack IDs"]:
        Rack = ConfigFile["Rack IDs"][RackID]

        Enabled = Rack["Enabled"]
        DeckLocation = (
            MagneticRackTrackerInstance.DeckLocationTrackerInstance.GetObjectByName(
                Rack["Deck Location ID"]
            )
        )

        LayoutItems = list()
        for LabwareID in Rack["Supported Labware"]:
            Labware = (
                MagneticRackTrackerInstance.LabwareTrackerInstance.GetObjectByName(
                    LabwareID
                )
            )
            Seqeunce = Rack["Supported Labware"][LabwareID]["Plate Sequence"]

            LayoutItems.append(LayoutItem(Seqeunce, DeckLocation, Labware))

        AspiratePipettingDevices = list()
        DispensePipettingDevices = list()

        for PipetteDeviceID in Rack["Supported Pipetting IDs"]:
            PipetteDevice = MagneticRackTrackerInstance.PipetteDeviceTrackerInstance.GetObjectByName(
                PipetteDeviceID
            ).GetPipettingChannel()

            AspiratePipettingTips = list()
            DispensePipettingTips = list()
            for TipID in Rack["Supported Pipetting IDs"][PipetteDeviceID][
                "Supported Tips"
            ]:
                LiquidClasses = Rack["Supported Pipetting IDs"][PipetteDeviceID][
                    "Supported Tips"
                ][TipID]["Liquid Classes"]

                Tip = MagneticRackTrackerInstance.TipTrackerInstance.GetObjectByName(
                    TipID
                )
                MaxVolume = Tip.GetMaxVolume()

                AspiratePipettingTips.append(
                    PipettingTip(
                        Tip,
                        [LiquidClass("Default", MaxVolume, LiquidClasses["Aspirate"])],
                    )
                )

                DispensePipettingTips.append(
                    PipettingTip(
                        Tip,
                        [LiquidClass("Default", MaxVolume, LiquidClasses["Dispense"])],
                    )
                )

            AspiratePipettingDevices.append(
                PipettingDevice(PipetteDevice, AspiratePipettingTips)
            )

            DispensePipettingDevices.append(
                PipettingDevice(PipetteDevice, DispensePipettingTips)
            )

        MagneticRackTrackerInstance.LoadManual(
            MagneticRack(
                RackID,
                Enabled,
                LayoutItems,
                AspiratePipettingDevices,
                DispensePipettingDevices,
            )
        )
