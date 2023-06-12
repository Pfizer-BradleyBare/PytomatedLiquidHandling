import logging
import os

from PytomatedLiquidHandling import HAL, Logger

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

BackendTrackerInstance = HAL.Backend.BackendLoader.LoadYaml(
    LoggerInstance, os.path.join(os.path.dirname(__file__), "Config_Backend.yaml")
)

LabwareTrackerInstance = HAL.Labware.LabwareLoader.LoadYaml(
    os.path.join(os.path.dirname(__file__), "Config_Labware.yaml")
)

TransportDeviceTrackerInstance = HAL.TransportDevice.TransportDeviceLoader.LoadYaml(
    BackendTrackerInstance,
    LabwareTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config_Transport.yaml"),
)

DeckLocationTrackerInstance = HAL.DeckLocation.DeckLocationLoader.LoadYaml(
    TransportDeviceTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config_DeckLocation.yaml"),
)

LayoutItemTrackerInstance = HAL.LayoutItem.LayoutItemLoader.LoadYaml(
    LabwareTrackerInstance,
    DeckLocationTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config_LayoutItem.yaml"),
)

ClosedContainerTrackerInstance = HAL.ClosedContainer.ClosedContainerLoader.LoadYaml(
    BackendTrackerInstance,
    DeckLocationTrackerInstance,
    LabwareTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config_ClosedContainer.yaml"),
)

TempControlDeviceTrackerInstance = (
    HAL.TempControlDevice.TempControlDeviceLoader.LoadYaml(
        BackendTrackerInstance,
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        TransportDeviceTrackerInstance,
        os.path.join(os.path.dirname(__file__), "Config_TempControlDevice.yaml"),
    )
)

TipTrackerInstance = HAL.Tip.TipLoader.LoadYaml(
    BackendTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config_Tip.yaml"),
)

PipetteTrackerInstance = HAL.Pipette.PipetteLoader.LoadYaml(
    BackendTrackerInstance,
    DeckLocationTrackerInstance,
    LabwareTrackerInstance,
    TipTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config_Pipette.yaml"),
)
# Load everything

LiquidHandler = BackendTrackerInstance.GetObjectByName("Hammy")
Heater = TempControlDeviceTrackerInstance.GetObjectByName("Heater")
FlipTube = ClosedContainerTrackerInstance.GetObjectByName("Special Fliptube")
PlateTransporter = TransportDeviceTrackerInstance
Pipette = PipetteTrackerInstance.GetObjectByName("Pipette")
# devices
SamplePlate = LayoutItemTrackerInstance.GetObjectByName("Sample Plate")
DigestionPlate = LayoutItemTrackerInstance.GetObjectByName("Digestion Plate")
FlipTubes = LayoutItemTrackerInstance.GetObjectByName("FlipTubes")
ReagentReservoirs = LayoutItemTrackerInstance.GetObjectByName("Reagent Reservoirs")
# Containers
RRPosWater = 1
FTPosTCEP = 32
FTPosIAA = 31
FTPosTFA = 30
FTPosLysC = 29
# Reagent Positions
# Get varables I care about

NumSamples = 8
StartingPosition = 1

TransferOptions = HAL.Pipette.TransferOptions

WaterTransferOptionsTracker = TransferOptions.OptionsTracker()
for Count in range(0, NumSamples):
    WaterTransferOptionsTracker.LoadSingle(
        TransferOptions.Options(
            SourceLayoutItemInstance=ReagentReservoirs,
            SourcePosition=RRPosWater,
            CurrentSourceVolume=5000,
            SourceMixCycles=0,
            SourceLiquidClassCategory="Default",
            DestinationLayoutItemInstance=DigestionPlate,
            DestinationPosition=StartingPosition + Count,
            CurrentDestinationVolume=0,
            DestinationMixCycles=0,
            DestinationLiquidClassCategory="Default",
            TransferVolume=90,
        )
    )
Pipette.Transfer(WaterTransferOptionsTracker)
# Water Transfer
# Sample Transfer
# Dilute sample into denaturation plate with water. All samples are assumed to be 10mg/mL

# Add TCEP

# Incubate

# Add IAA

# Incubate

# Add LysC

# Incubate

# Quench
