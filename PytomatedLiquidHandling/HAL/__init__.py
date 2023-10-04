import os

from . import (
    Backend,
    Carrier,
    ClosedContainer,
    DeckLoader,
    DeckLocation,
    HeatCoolShakeDevice,
    Labware,
    LayoutItem,
    MagneticRack,
    Pipette,
    StorageDevice,
    Tip,
    TransportDevice,
)

ClosedContainers: dict[str, ClosedContainer.Base.ClosedContainerABC]
# DeckLoaders: dict[str, DeckLoader.Base.DeckLoaderABC]
LayoutItems: dict[str, LayoutItem.Base.LayoutItemABC]
# MagneticRacks: dict[str, MagneticRack.Base.MagneticRackABC]
Pipettes: dict[str, Pipette.Base.PipetteABC]
StorageDevices: dict[str, StorageDevice.Base.StorageDeviceABC]
TempControlDevices: dict[str, HeatCoolShakeDevice.Base.HeatCoolShakeDeviceABC]
TransportDevices: dict[str, TransportDevice.Base.TransportDeviceABC]


def Initialize(ConfigFolderPath: str):
    Backends = Backend.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Backend.yaml"))

    Carriers = Carrier.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Carrier.yaml"))

    Labwares = Labware.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Labware.yaml"))

    global TransportDevices
    TransportDevices = TransportDevice.Loader.LoadYaml(
        Backends,
        Labwares,
        os.path.join(ConfigFolderPath, "Transport.yaml"),
    )

    DeckLocations = DeckLocation.Loader.LoadYaml(
        Carriers,
        TransportDevices,
        os.path.join(ConfigFolderPath, "DeckLocation.yaml"),
    )

    global LayoutItems
    LayoutItems = LayoutItem.Loader.LoadYaml(
        Labwares,
        DeckLocations,
        os.path.join(ConfigFolderPath, "LayoutItem.yaml"),
    )

    global ClosedContainers
    ClosedContainers = ClosedContainer.Loader.LoadYaml(
        Backends,
        DeckLocations,
        Labwares,
        os.path.join(ConfigFolderPath, "ClosedContainer.yaml"),
    )

    global TempControlDevices
    TempControlDevices = HeatCoolShakeDevice.Loader.LoadYaml(
        Backends,
        LayoutItems,
        os.path.join(ConfigFolderPath, "TempControlDevice.yaml"),
    )

    Tips = Tip.Loader.LoadYaml(
        Backends,
        os.path.join(ConfigFolderPath, "Tip.yaml"),
    )

    global Pipettes
    Pipettes = Pipette.Loader.LoadYaml(
        Backends,
        DeckLocations,
        Labwares,
        Tips,
        os.path.join(ConfigFolderPath, "Pipette.yaml"),
    )

    global StorageDevices
    StorageDevices = StorageDevice.Loader.LoadYaml(
        LayoutItems,
        os.path.join(ConfigFolderPath, "Storage.yaml"),
    )
