import os

import yaml

from PytomatedLiquidHandling.HAL import Backend, DeckLocation, Labware, Tip

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Tools.Logger import Logger
from .BaseIMCSDesalting import (
    DesaltingTip,
    DesaltingTipTracker,
    ElutionParameters,
    IMCSDesaltingTracker,
)
from .HamiltonCORE96HeadIMCSDesalting import HamiltonCORE96HeadIMCSDesalting
from .HamiltonPortraitCORE8ChannelIMCSDesalting import (
    HamiltonPortraitCORE8ChannelIMCSDesalting,
)


def LoadYaml(
    LoggerInstance: Logger,
    BackendTrackerInstance: Backend.BackendTracker,
    DeckLocationTrackerInstance: DeckLocation.DeckLocationTracker,
    LabwareTrackerInstance: Labware.LabwareTracker,
    TipTrackerInstance: Tip.TipTracker,
    FilePath: str,
) -> IMCSDesaltingTracker:
    IMCSDesaltingTrackerInstance = IMCSDesaltingTracker()

    if not os.path.exists(FilePath):
        return IMCSDesaltingTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        return IMCSDesaltingTrackerInstance

    TipUniqueIdentifier = ConfigFile["300uL Tip Unique Identifier"]
    TipSupportDropOffSequence = ConfigFile["300uL Tip Support Drop Off Sequence"]
    TipSupportPickupSequence = ConfigFile["300uL Tip Support Pickup Sequence"]
    IMCSTipSupportDropOffSequence = ConfigFile["IMCS Tip Support Drop Off Sequence"]
    IMCSTipSupportPickupSequence = ConfigFile["IMCS Tip Support Pickup Off Sequence"]

    del ConfigFile["300uL Tip Unique Identifier"]
    del ConfigFile["300uL Tip Support Drop Off Sequence"]
    del ConfigFile["300uL Tip Support Pickup Sequence"]
    del ConfigFile["IMCS Tip Support Drop Off Sequence"]
    del ConfigFile["IMCS Tip Support Pickup Off Sequence"]
    # pull shared info then remove it

    TipInstance = TipTrackerInstance.GetObjectByName(TipUniqueIdentifier)
    if not TipInstance.MaxVolume == 300:
        raise Exception("Wrong tip selected...")

    for DeviceType in ConfigFile:
        Device = ConfigFile[DeviceType]

        LoadLiquidClass = Device["Load Liquid Class"]
        EluteLiquidClass = Device["Elute Liquid Class"]
        del Device["Load Liquid Class"]
        del Device["Elute Liquid Class"]

        SupportedSourceLabwareTrackerInstance = Labware.LabwareTracker()
        for LabwareID in Device["Supported Source Labware Unique Identifiers"]:
            SupportedSourceLabwareTrackerInstance.LoadSingle(
                LabwareTrackerInstance.GetObjectByName(LabwareID)
            )
        del Device["Supported Source Labware Unique Identifiers"]

        SupportedDestinationLabwareTrackerInstance = Labware.LabwareTracker()
        for LabwareID in Device["Supported Destination Labware Unique Identifiers"]:
            SupportedDestinationLabwareTrackerInstance.LoadSingle(
                LabwareTrackerInstance.GetObjectByName(LabwareID)
            )
        del Device["Supported Destination Labware Unique Identifiers"]

        SupportedDeckLocationTrackerInstance = DeckLocation.DeckLocationTracker()
        for DeckLocationID in Device["Supported Deck Location Unique Identifiers"]:
            SupportedDeckLocationTrackerInstance.LoadSingle(
                DeckLocationTrackerInstance.GetObjectByName(DeckLocationID)
            )
        del Device["Supported Deck Location Unique Identifiers"]

        DesaltingTipTrackerInstance = DesaltingTipTracker()
        for Tip in Device["Elution Method Tip Types"]:
            DesaltingTipInstance = DesaltingTip(Tip["Unique Identifier"])

            for ElutionMethod in Tip["Elution Methods"]:
                DesaltingTipInstance.LoadSingle(
                    ElutionParameters(
                        ElutionMethod["Unique Identifier"],
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

            ID = DeviceItem["Unique Identifier"]
            BackendID = DeviceItem["Backend Unique Identifier"]
            BackendInstance = BackendTrackerInstance.GetObjectByName(BackendID)
            CustomErrorHandling = DeviceItem["Custom Error Handling"]

            IMCSTipDropOffSequence = DeviceItem["IMCS Tip Drop Off Sequence"]
            IMCSTipPickupSequence = DeviceItem["IMCS Tip Pickup Sequence"]
            IMCSTipPipetteSequence = DeviceItem["IMCS Tip Pipette Sequence"]

            if DeviceType == "Hamilton CORE 96 Head IMCS Desalting":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Wrong backend selected.")

                HamiltonCORE96HeadIMCSDesalting(
                    ID,
                    BackendInstance,
                    CustomErrorHandling,
                    TipInstance,
                    TipSupportDropOffSequence,
                    TipSupportPickupSequence,
                    IMCSTipSupportDropOffSequence,
                    IMCSTipSupportPickupSequence,
                    LoadLiquidClass,
                    EluteLiquidClass,
                    SupportedSourceLabwareTrackerInstance,
                    SupportedDestinationLabwareTrackerInstance,
                    SupportedDeckLocationTrackerInstance,
                    DesaltingTipTrackerInstance,
                    IMCSTipDropOffSequence,
                    IMCSTipPickupSequence,
                    IMCSTipPipetteSequence,
                )

            elif DeviceType == "Hamilton Portrait CORE 8 Channel IMCS Desalting":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Wrong backend selected.")

                HamiltonPortraitCORE8ChannelIMCSDesalting(
                    ID,
                    BackendInstance,
                    CustomErrorHandling,
                    TipInstance,
                    TipSupportDropOffSequence,
                    TipSupportPickupSequence,
                    IMCSTipSupportDropOffSequence,
                    IMCSTipSupportPickupSequence,
                    LoadLiquidClass,
                    EluteLiquidClass,
                    SupportedSourceLabwareTrackerInstance,
                    SupportedDestinationLabwareTrackerInstance,
                    SupportedDeckLocationTrackerInstance,
                    DesaltingTipTrackerInstance,
                    IMCSTipDropOffSequence,
                    IMCSTipPickupSequence,
                    IMCSTipPipetteSequence,
                )

            else:
                raise Exception("Device type not recognized")

    return IMCSDesaltingTrackerInstance
