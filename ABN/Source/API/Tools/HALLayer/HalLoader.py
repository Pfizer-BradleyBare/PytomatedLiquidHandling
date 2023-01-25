import os

from ....HAL.ClosedContainer import ClosedContainerLoader
from ....HAL.DeckLocation import DeckLocationLoader
from ....HAL.Labware import LabwareLoader
from ....HAL.Layout import LayoutItemLoader
from ....HAL.Lid import LidLoader

# from .MagneticRack import MagneticRackLoader, MagneticRackTracker
from ....HAL.Notify import NotifyLoader
from ....HAL.Pipette import PipetteLoader
from ....HAL.TempControlDevice import TempControlDeviceLoader
from ....HAL.Tip import TipLoader
from ....HAL.TransportDevice import TransportDeviceLoader
from ....Server.Globals import LOG
from .HALLayer import HALLayer


def Load(BasePath: str) -> HALLayer:

    HALLayerInstance = HALLayer()
    LOG.info("Loading Labware...")

    LabwareTrackerInstance = LabwareLoader.LoadYaml(
        os.path.join(BasePath, "Labware\\Labware.yaml"),
    )
    HALLayerInstance.LabwareTrackerInstance = LabwareTrackerInstance
    for Labware in LabwareTrackerInstance.GetObjectsAsList():
        LOG.debug(Labware)

    LOG.info("Success!")

    LOG.info("Loading Transport...")

    TransportDeviceTrackerInstance = TransportDeviceLoader.LoadYaml(
        LabwareTrackerInstance,
        os.path.join(BasePath, "Transport\\Transport.yaml"),
    )
    HALLayerInstance.TransportDeviceTrackerInstance = TransportDeviceTrackerInstance
    for TransportDevice in TransportDeviceTrackerInstance.GetObjectsAsList():
        LOG.debug(TransportDevice)

    LOG.info("Success!")

    LOG.info("Loading DeckLocation...")

    DeckLocationTrackerInstance = DeckLocationLoader.LoadYaml(
        TransportDeviceTrackerInstance,
        os.path.join(BasePath, "DeckLocation\\DeckLocation.yaml"),
    )
    HALLayerInstance.DeckLocationTrackerInstance = DeckLocationTrackerInstance
    for Location in DeckLocationTrackerInstance.GetObjectsAsList():
        LOG.debug(Location)

    LOG.info("Success!")

    LOG.info("Loading Layout...")

    LayoutItemTrackerInstance = LayoutItemLoader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        os.path.join(BasePath, "Layout\\Layout.yaml"),
    )
    HALLayerInstance.LayoutItemGroupingTrackerInstance = LayoutItemTrackerInstance
    for Layout in LayoutItemTrackerInstance.GetObjectsAsList():
        LOG.debug(Layout)

    LOG.info("Success!")

    LOG.info("Loading Lid...")

    LidTrackerInstance = LidLoader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        os.path.join(BasePath, "Lid\\Lid.yaml"),
    )
    HALLayerInstance.LidTrackerInstance = LidTrackerInstance
    for Lid in LidTrackerInstance.GetObjectsAsList():
        LOG.debug(Lid)

    LOG.info("Success!")

    LOG.info("Loading TempControlDevice...")

    TempControlDeviceTrackerInstance = TempControlDeviceLoader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        os.path.join(BasePath, "TempControlDevice\\TempControlDevice.yaml"),
    )
    HALLayerInstance.TempControlDeviceTrackerInstance = TempControlDeviceTrackerInstance
    for TempControlDevice in TempControlDeviceTrackerInstance.GetObjectsAsList():
        LOG.debug(TempControlDevice)

    LOG.info("Success!")

    LOG.info("Loading Tip...")

    TipTrackerInstance = TipLoader.LoadYaml(
        os.path.join(BasePath, "Tip\\Tip.yaml"),
    )
    HALLayerInstance.TipTrackerInstance = TipTrackerInstance
    for Tip in TipTrackerInstance.GetObjectsAsList():
        LOG.debug(Tip)

    LOG.info("Success!")

    LOG.info("Loading Pipette...")

    PipetteTrackerInstance = PipetteLoader.LoadYaml(
        TipTrackerInstance,
        LabwareTrackerInstance,
        os.path.join(BasePath, "Pipette\\Pipette.yaml"),
    )
    HALLayerInstance.PipetteTrackerInstance = PipetteTrackerInstance
    for Pipette in PipetteTrackerInstance.GetObjectsAsList():
        LOG.debug(Pipette)

    LOG.info("Success!")

    LOG.info("Loading Magnetic Rack...")

    #    MagneticRackLoader.LoadYaml(
    #        MagneticRacks,
    #        os.path.join(BasePath, "\\MagneticRack\\MagneticRack.yaml",
    #    )
    #    HALLayerInstance.MagneticRackTrackerInstance = MagneticRacks
    #    for MagneticRack in MagneticRacks.GetObjectsAsList():
    #        LOG.debug(MagneticRack)

    LOG.info("Success!")

    LOG.info("Loading Notify...")

    NotifyTrackerInstance = NotifyLoader.LoadYaml(
        os.path.join(BasePath, "Notify\\Notify.yaml"),
    )
    HALLayerInstance.NotifyTrackerInstance = NotifyTrackerInstance
    for NotifyDevice in NotifyTrackerInstance.GetObjectsAsList():
        LOG.debug(NotifyDevice)

    LOG.info("Success!")

    LOG.info("Loading FlipTube...")

    ClosedContainerTrackerInstance = ClosedContainerLoader.LoadYaml(
        LabwareTrackerInstance,
        os.path.join(BasePath, "ClosedContainers\\ClosedContainers.yaml"),
    )
    HALLayerInstance.ClosedContainerTrackerInstance = ClosedContainerTrackerInstance
    for FlipTube in ClosedContainerTrackerInstance.GetObjectsAsList():
        LOG.debug(FlipTube)

    LOG.info("Success!")

    return HALLayerInstance
