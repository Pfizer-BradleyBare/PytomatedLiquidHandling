import logging
import os

from PytomatedLiquidHandling import HAL, Logger

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

BackendTrackerInstance = HAL.Backend.Loader.LoadYaml(
    LoggerInstance,
    os.path.join(os.path.dirname(__file__), "Config", "Config_Backend.yaml"),
)

LabwareTrackerInstance = HAL.Labware.Loader.LoadYaml(
    os.path.join(os.path.dirname(__file__), "Config", "Config_Labware.yaml")
)

CarrierTrackerInstance = HAL.Carrier.Loader.LoadYaml(
    os.path.join(os.path.dirname(__file__), "Config", "Config_Carrier.yaml")
)

DeckLocationTrackerInstance = HAL.DeckLocation.Loader.LoadYaml(
    CarrierTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config", "Config_DeckLocation.yaml"),
)

TransportDeviceTrackerInstance = HAL.TransportDevice.Loader.LoadYaml(
    BackendTrackerInstance,
    LabwareTrackerInstance,
    DeckLocationTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config", "Config_Transport.yaml"),
)

LayoutItemTrackerInstance = HAL.LayoutItem.Loader.LoadYaml(
    LabwareTrackerInstance,
    DeckLocationTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config", "Config_LayoutItem.yaml"),
)

ClosedContainerTrackerInstance = HAL.ClosedContainer.Loader.LoadYaml(
    BackendTrackerInstance,
    DeckLocationTrackerInstance,
    LabwareTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config", "Config_ClosedContainer.yaml"),
)

TempControlDeviceTrackerInstance = HAL.TempControlDevice.Loader.LoadYaml(
    BackendTrackerInstance,
    LayoutItemTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config", "Config_TempControlDevice.yaml"),
)

TipTrackerInstance = HAL.Tip.Loader.LoadYaml(
    BackendTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config", "Config_Tip.yaml"),
)

PipetteTrackerInstance = HAL.Pipette.Loader.LoadYaml(
    BackendTrackerInstance,
    DeckLocationTrackerInstance,
    LabwareTrackerInstance,
    TipTrackerInstance,
    os.path.join(os.path.dirname(__file__), "Config", "Config_Pipette.yaml"),
)
# Load everything

PlateTransporter = TransportDeviceTrackerInstance
# devices
SamplePlate = LayoutItemTrackerInstance.GetObjectByName("Plate1")
DigestionPlate = LayoutItemTrackerInstance.GetObjectByName("Plate2")

OptionsTrackerInstance = HAL.TransportDevice.TransportOptions.OptionsTracker()
OptionsTrackerInstance.LoadSingle(
    HAL.TransportDevice.TransportOptions.Options(
        SourceLayoutItem=SamplePlate, DestinationLayoutItem=DigestionPlate
    )
)
PlateTransporter.Transport(OptionsTrackerInstance)
