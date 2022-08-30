import yaml
from .PipetteTracker import PipetteTracker
from .Pipette import (
    LiquidClass,
    PipettingTip,
    DeviceTypes,
    Portrait1mLChannels,
    PipettingDevice,
    Core96HeadChannels,
)


def LoadYaml(PipetteTrackerInstance: PipetteTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for ChannelsDeviceID in ConfigFile["Device IDs"]:
        ChannelsDevice = ConfigFile["Device IDs"][ChannelsDeviceID]
        Enabled = ChannelsDevice["Enabled"]

        PipettingTips = list()
        for TipID in ChannelsDevice["Supported Tips"]:
            TipItem = PipetteTrackerInstance.TipTrackerInstance.GetObjectByName(TipID)

            LiquidClasses = list()
            for LiquidClassID in ChannelsDevice["Supported Tips"][TipID][
                "Liquid Class IDs"
            ]:
                for LiquidClassItem in ChannelsDevice["Supported Tips"][TipID][
                    "Liquid Class IDs"
                ][LiquidClassID]:
                    MaxVolume = LiquidClassItem["Max Volume"]
                    LiquidClassString = LiquidClassItem["Liquid Class"]

                    LiquidClasses.append(
                        LiquidClass(LiquidClassID, MaxVolume, LiquidClassString)
                    )
            # Do the supported Tips loading

            PipettingTips.append(PipettingTip(TipItem, LiquidClasses))

        DeviceType = DeviceTypes(ChannelsDeviceID)

        if DeviceType == DeviceTypes.Portrait1mLChannels:
            ActiveChannels = ChannelsDevice["Active Channels"]

            PipetteTrackerInstance.LoadManual(
                PipettingDevice(
                    Portrait1mLChannels(ActiveChannels, Enabled),
                    PipettingTips,
                )
            )

        elif DeviceType == DeviceTypes.Core96Head:
            PipetteTrackerInstance.LoadManual(
                PipettingDevice(
                    Core96HeadChannels(Enabled),
                    PipettingTips,
                )
            )
