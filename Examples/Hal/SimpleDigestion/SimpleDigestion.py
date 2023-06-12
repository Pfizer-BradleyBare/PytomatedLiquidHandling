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

# BackendTrackerInstance.GetObjectByName("Hammy").StartBackend()

TransportOptionsTrackerInstance = HAL.TransportDevice.TransportOptions.OptionsTracker()
TransportOptionsTrackerInstance.LoadSingle(
    HAL.TransportDevice.TransportOptions.Options(
        SourceLayoutItem=LayoutItemTrackerInstance.GetObjectByName("Sample Plate"),
        DestinationLayoutItem=LayoutItemTrackerInstance.GetObjectByName(
            "Digestion Plate"
        ),
    )
)
TransportDeviceTrackerInstance.Transport(TransportOptionsTrackerInstance)
