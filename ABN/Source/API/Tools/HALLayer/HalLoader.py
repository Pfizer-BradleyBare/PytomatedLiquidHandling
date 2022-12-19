from ....HAL.ClosedContainers import ClosedContainersLoader
from ....HAL.ClosedContainers.BaseClosedContainers import ClosedContainersTracker
from ....HAL.DeckLocation import DeckLocationLoader, DeckLocationTracker
from ....HAL.Labware import LabwareLoader, LabwareTracker
from ....HAL.Layout import LayoutItemLoader, LayoutItemTracker
from ....HAL.Lid import LidLoader, LidTracker

# from .MagneticRack import MagneticRackLoader, MagneticRackTracker
from ....HAL.Notify import NotifyLoader, NotifyTracker

# from .Pipette import PipetteLoader, PipetteTracker
from ....HAL.TempControlDevice import TempControlDeviceLoader
from ....HAL.TempControlDevice.BaseTempControlDevice import TempControlDeviceTracker
from ....HAL.Tip import TipLoader
from ....HAL.Tip.BaseTip import TipTracker
from ....HAL.TransportDevice import TransportDeviceLoader
from ....HAL.TransportDevice.BaseTransportDevice import TransportDeviceTracker
from ....Server.Globals import LOG
from .HALLayer import HALLayer


def Load() -> HALLayer:
    HALLayerInstance = HALLayer()
    LOG.info("Loading Labware...")

    LabwareTrackerInstance = LabwareLoader.LoadYaml(
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\Labware\\Labware.yaml",
    )
    HALLayerInstance.LabwareTrackerInstance = LabwareTrackerInstance
    for Labware in LabwareTrackerInstance.GetObjectsAsList():
        LOG.debug(Labware)

    LOG.info("Success!")

    LOG.info("Loading Transport...")

    TransportDeviceTrackerInstance = TransportDeviceLoader.LoadYaml(
        LabwareTrackerInstance,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\Transport\\Transport.yaml",
    )
    HALLayerInstance.TransportDeviceTrackerInstance = TransportDeviceTrackerInstance
    for TransportDevice in TransportDeviceTrackerInstance.GetObjectsAsList():
        LOG.debug(TransportDevice)

    LOG.info("Success!")

    LOG.info("Loading DeckLocation...")

    DeckLocationTrackerInstance = DeckLocationLoader.LoadYaml(
        TransportDeviceTrackerInstance,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\DeckLocation\\DeckLocation.yaml",
    )
    HALLayerInstance.DeckLocationTrackerInstance = DeckLocationTrackerInstance
    for Location in DeckLocationTrackerInstance.GetObjectsAsList():
        LOG.debug(Location)

    LOG.info("Success!")

    LOG.info("Loading Layout...")

    LayoutItemTrackerInstance = LayoutItemLoader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\Layout\\Layout.yaml",
    )
    HALLayerInstance.LayoutItemTrackerInstance = LayoutItemTrackerInstance
    for Layout in LayoutItemTrackerInstance.GetObjectsAsList():
        LOG.debug(Layout)

    LOG.info("Success!")

    LOG.info("Loading Lid...")

    LidTrackerInstance = LidLoader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\Lid\\Lid.yaml",
    )
    HALLayerInstance.LidTrackerInstance = LidTrackerInstance
    for Lid in LidTrackerInstance.GetObjectsAsList():
        LOG.debug(Lid)

    LOG.info("Success!")

    LOG.info("Loading TempControlDevice...")

    TempControlDeviceTrackerInstance = TempControlDeviceLoader.LoadYaml(
        LabwareTrackerInstance,
        DeckLocationTrackerInstance,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\TempControlDevice\\TempControlDevice.yaml",
    )
    HALLayerInstance.TempControlDeviceTrackerInstance = TempControlDeviceTrackerInstance
    for TempControlDevice in TempControlDeviceTrackerInstance.GetObjectsAsList():
        LOG.debug(TempControlDevice)

    LOG.info("Success!")

    LOG.info("Loading Tip...")

    TipTrackerInstance = TipLoader.LoadYaml(
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\Tip\\Tip.yaml",
    )
    HALLayerInstance.TipTrackerInstance = TipTrackerInstance
    for Tip in TipTrackerInstance.GetObjectsAsList():
        LOG.debug(Tip)

    LOG.info("Success!")

    LOG.info("Loading Pipette...")

    #    PipetteLoader.LoadYaml(
    #        Pipettes,
    #        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\Pipette\\Pipette.yaml",
    #    )
    #    HALLayerInstance.PipetteTrackerInstance = Pipettes
    #    for Pipette in Pipettes.GetObjectsAsList():
    #        LOG.debug(Pipette)

    LOG.info("Success!")

    LOG.info("Loading Magnetic Rack...")

    #    MagneticRackLoader.LoadYaml(
    #        MagneticRacks,
    #        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\MagneticRack\\MagneticRack.yaml",
    #    )
    #    HALLayerInstance.MagneticRackTrackerInstance = MagneticRacks
    #    for MagneticRack in MagneticRacks.GetObjectsAsList():
    #        LOG.debug(MagneticRack)

    LOG.info("Success!")

    LOG.info("Loading Notify...")

    NotifyTrackerInstance = NotifyLoader.LoadYaml(
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\Notify\\Notify.yaml",
    )
    HALLayerInstance.NotifyTrackerInstance = NotifyTrackerInstance
    for NotifyDevice in NotifyTrackerInstance.GetObjectsAsList():
        LOG.debug(NotifyDevice)

    LOG.info("Success!")

    LOG.info("Loading FlipTube...")

    ClosedContainersTrackerInstance = ClosedContainersLoader.LoadYaml(
        LabwareTrackerInstance,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\ABN\\AutomationBareNecessitiesConfiguration\\HAL\\ClosedContainers\\ClosedContainers.yaml",
    )
    HALLayerInstance.ClosedContainersTrackerInstance = ClosedContainersTrackerInstance
    for FlipTube in ClosedContainersTrackerInstance.GetObjectsAsList():
        LOG.debug(FlipTube)

    LOG.info("Success!")

    return HALLayerInstance
