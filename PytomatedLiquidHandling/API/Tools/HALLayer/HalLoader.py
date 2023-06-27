import os

from ....HAL.ClosedContainer import Loader
from ....HAL.DeckLocation import Loader
from ....HAL.Labware import Loader
from ....HAL.Layout import LayoutItemLoader
from ....HAL.Lid import LidLoader

# from .MagneticRack import MagneticRackLoader, MagneticRackTracker
from ....HAL.Notify import Loader
from ....HAL.Pipette import Loader
from ....HAL.TempControlDevice import Loader
from ....HAL.Tip import Loader
from ....HAL.TransportDevice import Loader
from .HALLayer import HALLayer


def Load(BasePath: str) -> HALLayer:
    from ...Handler import GetHandler

    LoggerInstance = GetHandler().GetLogger()

    HALLayerInstance = HALLayer()
    LoggerInstance.info("Loading Labware...")

    LabwareTrackerInstance = Loader.LoadYaml(
        os.path.join(BasePath, "Labware\\Labware.yaml"),
    )
    HALLayerInstance.LabwareTrackerInstance = LabwareTrackerInstance
    for Labware in LabwareTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(Labware)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading Transport...")

    TransportDeviceTrackerInstance = Loader.LoadYaml(
        LabwareTrackerInstance,
        os.path.join(BasePath, "Transport\\Transport.yaml"),
    )
    HALLayerInstance.TransportDeviceTrackerInstance = TransportDeviceTrackerInstance
    for TransportDevice in TransportDeviceTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(TransportDevice)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading DeckLocation...")

    DeckLocationTrackerInstance = Loader.LoadYaml(
        TransportDeviceTrackerInstance,
        os.path.join(BasePath, "DeckLocation\\DeckLocation.yaml"),
    )
    HALLayerInstance.DeckLocationTrackerInstance = DeckLocationTrackerInstance
    for Location in DeckLocationTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(Location)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading Layout...")

    LayoutItemTrackerInstance = LayoutItemLoader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        os.path.join(BasePath, "Layout\\Layout.yaml"),
    )
    HALLayerInstance.LayoutItemGroupingTrackerInstance = LayoutItemTrackerInstance
    for Layout in LayoutItemTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(Layout)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading Lid...")

    LidTrackerInstance = LidLoader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        os.path.join(BasePath, "Lid\\Lid.yaml"),
    )
    HALLayerInstance.LidTrackerInstance = LidTrackerInstance
    for Lid in LidTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(Lid)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading TempControlDevice...")

    TempControlDeviceTrackerInstance = Loader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        os.path.join(BasePath, "TempControlDevice\\TempControlDevice.yaml"),
    )
    HALLayerInstance.TempControlDeviceTrackerInstance = TempControlDeviceTrackerInstance
    for TempControlDevice in TempControlDeviceTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(TempControlDevice)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading Tip...")

    TipTrackerInstance = Loader.LoadYaml(
        os.path.join(BasePath, "Tip\\Tip.yaml"),
    )
    HALLayerInstance.TipTrackerInstance = TipTrackerInstance
    for Tip in TipTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(Tip)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading Pipette...")

    PipetteTrackerInstance = Loader.LoadYaml(
        TipTrackerInstance,
        LabwareTrackerInstance,
        os.path.join(BasePath, "Pipette\\Pipette.yaml"),
    )
    HALLayerInstance.PipetteTrackerInstance = PipetteTrackerInstance
    for Pipette in PipetteTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(Pipette)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading Magnetic Rack...")

    #    MagneticRackLoader.LoadYaml(
    #        MagneticRacks,
    #        os.path.join(BasePath, "\\MagneticRack\\MagneticRack.yaml",
    #    )
    #    HALLayerInstance.MagneticRackTrackerInstance = MagneticRacks
    #    for MagneticRack in MagneticRacks.GetObjectsAsList():
    #        LoggerInstance.debug(MagneticRack)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading Notify...")

    NotifyTrackerInstance = Loader.LoadYaml(
        os.path.join(BasePath, "Notify\\Notify.yaml"),
    )
    HALLayerInstance.NotifyTrackerInstance = NotifyTrackerInstance
    for NotifyDevice in NotifyTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(NotifyDevice)

    LoggerInstance.info("Success!")

    LoggerInstance.info("Loading FlipTube...")

    ClosedContainerTrackerInstance = Loader.LoadYaml(
        LabwareTrackerInstance,
        os.path.join(BasePath, "ClosedContainers\\ClosedContainers.yaml"),
    )
    HALLayerInstance.ClosedContainerTrackerInstance = ClosedContainerTrackerInstance
    for FlipTube in ClosedContainerTrackerInstance.GetObjectsAsList():
        LoggerInstance.debug(FlipTube)

    LoggerInstance.info("Success!")

    return HALLayerInstance
