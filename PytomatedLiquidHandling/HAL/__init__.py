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

_IsHALInit: bool = False
ClosedContainers: dict[str, ClosedContainer.Base.ClosedContainerABC] = dict()
DeckLoaders: dict[str, DeckLoader.Base.DeckLoaderABC] = dict()
MagneticRacks: dict[str, MagneticRack.Base.MagneticRackABC] = dict()
Pipettes: dict[str, Pipette.Base.PipetteABC] = dict()
StorageDevices: dict[str, StorageDevice.Base.StorageDeviceABC] = dict()
HeatCoolShakeDevices: dict[
    str, HeatCoolShakeDevice.Base.HeatCoolShakeDeviceABC
] = dict()
TransportDevices: dict[str, TransportDevice.Base.TransportDeviceABC] = dict()


def Initialize(ConfigFolderPath: str):
    global _IsHALInit
    _IsHALInit = True

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

    global HeatCoolShakeDevices
    HeatCoolShakeDevices = HeatCoolShakeDevice.Loader.LoadYaml(
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
