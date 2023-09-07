import os

import yaml

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, Tip

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Tools.Logger import Logger
from .Base import DesaltingTip, DesaltingTipTracker, ElutionParameters, IMCSDesaltingABC
from .HamiltonCORE96HeadIMCSDesalting import HamiltonCORE96HeadIMCSDesalting
from .HamiltonPortraitCORE8ChannelIMCSDesalting import (
    HamiltonPortraitCORE8ChannelIMCSDesalting,
)


def LoadYaml(
    LoggerInstance: Logger,
    Backends: dict[str, BackendABC],
    DeckLocations: dict[str, DeckLocation.Base.DeckLocationABC],
    Labwares: dict[str, Labware.Base.LabwareABC],
    Tips: dict[str, Tip.Base.TipABC],
    FilePath: str,
) -> dict[str, IMCSDesaltingABC]:
    IMCSDesaltingDevices: dict[str, IMCSDesaltingABC] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return IMCSDesaltingDevices

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return IMCSDesaltingDevices

    TipID = ConfigFile["300uL Tip Identifier"]
    TipSupportDropOffSequence = ConfigFile["300uL Tip Support Drop Off Sequence"]
    TipSupportPickupSequence = ConfigFile["300uL Tip Support Pickup Sequence"]
    IMCSTipSupportDropOffSequence = ConfigFile["IMCS Tip Support Drop Off Sequence"]
    IMCSTipSupportPickupSequence = ConfigFile["IMCS Tip Support Pickup Off Sequence"]

    del ConfigFile["300uL Tip Identifier"]
    del ConfigFile["300uL Tip Support Drop Off Sequence"]
    del ConfigFile["300uL Tip Support Pickup Sequence"]
    del ConfigFile["IMCS Tip Support Drop Off Sequence"]
    del ConfigFile["IMCS Tip Support Pickup Off Sequence"]
    # pull shared info then remove it

    TipInstance = Tips[TipID]
    if not TipInstance.MaxVolume == 300:
        raise Exception("Wrong tip selected...")

    for DeviceType in ConfigFile:
        Device = ConfigFile[DeviceType]

        LoadLiquidClass = Device["Load Liquid Class"]
        EluteLiquidClass = Device["Elute Liquid Class"]
        del Device["Load Liquid Class"]
        del Device["Elute Liquid Class"]

        SupportedSourceLabwares: list[Labware.Base.LabwareABC] = list()
        for LabwareID in Device["Supported Source Labware Identifiers"]:
            SupportedSourceLabwares.append(Labwares[LabwareID])
        del Device["Supported Source Labware Identifiers"]

        SupportedDestinationLabwares: list[Labware.Base.LabwareABC] = list()
        for LabwareID in Device["Supported Destination Labware Identifiers"]:
            SupportedDestinationLabwares.append(Labwares[LabwareID])
        del Device["Supported Destination Labware Identifiers"]

        SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC] = list()
        for DeckLocationID in Device["Supported Deck Location Identifiers"]:
            SupportedDeckLocations.append(DeckLocations[DeckLocationID])
        del Device["Supported Deck Location Identifiers"]

        DesaltingTipTrackerInstance = DesaltingTipTracker()
        for Tip in Device["Elution Method Tip Types"]:
            DesaltingTipInstance = DesaltingTip(Tip["Identifier"])

            for ElutionMethod in Tip["Elution Methods"]:
                DesaltingTipInstance.LoadSingle(
                    ElutionParameters(
                        ElutionMethod["Identifier"],
                        ElutionMethod["Equilibration Dispense Height"],
                        ElutionMethod["Sample Dispense Height"],
                        ElutionMethod["Chaser Dispense Height"],
                        ElutionMethod["Equilibration Load Volume"],
                        ElutionMethod["Sample Load Volume"],
                        ElutionMethod["Chaser Load Volume"],
                        ElutionMethod["Equilibration Dispense Volume"],
                        ElutionMethod["Sample Dispense Volume"],
                        ElutionMethod["Chaser Dispense Volume"],
                    )
                )
            DesaltingTipTrackerInstance.LoadSingle(DesaltingTipInstance)
        del Device["Elution Method Tip Types"]

        for DeviceItem in Device:
            if DeviceItem["Enabled"] == False:
                continue

            Identifier = DeviceItem["Identifier"]
            BackendID = DeviceItem["Backend Identifier"]
            BackendInstance = Backends[BackendID]
            CustomErrorHandling = DeviceItem["Custom Error Handling"]

            IMCSTipDropOffSequence = DeviceItem["IMCS Tip Drop Off Sequence"]
            IMCSTipPickupSequence = DeviceItem["IMCS Tip Pickup Sequence"]
            IMCSTipPipetteSequence = DeviceItem["IMCS Tip Pipette Sequence"]

            if DeviceType == "Hamilton CORE 96 Head IMCS Desalting":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Wrong backend selected.")

                HamiltonCORE96HeadIMCSDesalting(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    TipInstance,
                    TipSupportDropOffSequence,
                    TipSupportPickupSequence,
                    IMCSTipSupportDropOffSequence,
                    IMCSTipSupportPickupSequence,
                    LoadLiquidClass,
                    EluteLiquidClass,
                    SupportedSourceLabwares,
                    SupportedDestinationLabwares,
                    SupportedDeckLocations,
                    DesaltingTipTrackerInstance,
                    IMCSTipDropOffSequence,
                    IMCSTipPickupSequence,
                    IMCSTipPipetteSequence,
                )

            elif DeviceType == "Hamilton Portrait CORE 8 Channel IMCS Desalting":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Wrong backend selected.")

                HamiltonPortraitCORE8ChannelIMCSDesalting(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    TipInstance,
                    TipSupportDropOffSequence,
                    TipSupportPickupSequence,
                    IMCSTipSupportDropOffSequence,
                    IMCSTipSupportPickupSequence,
                    LoadLiquidClass,
                    EluteLiquidClass,
                    SupportedSourceLabwares,
                    SupportedDestinationLabwares,
                    SupportedDeckLocations,
                    DesaltingTipTrackerInstance,
                    IMCSTipDropOffSequence,
                    IMCSTipPickupSequence,
                    IMCSTipPipetteSequence,
                )

            else:
                raise Exception("Device type not recognized")

    return IMCSDesaltingDevices
