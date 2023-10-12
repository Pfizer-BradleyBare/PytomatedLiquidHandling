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

Backends: dict[str, Backend.Base.BackendABC] = dict()
Carriers: dict[str, Carrier.Base.CarrierABC] = dict()
Labwares: dict[str, Labware.Base.LabwareABC] = dict()
TransportDevices: dict[str, TransportDevice.Base.TransportDeviceABC] = dict()
DeckLocations: dict[str, DeckLocation.Base.DeckLocationABC] = dict()
LayoutItems: dict[str, LayoutItem.Base.LayoutItemABC] = dict()
ClosedContainerDevices: dict[str, ClosedContainer.Base.ClosedContainerABC] = dict()
HeatCoolShakeDevices: dict[
    str, HeatCoolShakeDevice.Base.HeatCoolShakeDeviceABC
] = dict()
PipetteDevices: dict[str, Pipette.Base.PipetteABC] = dict()
StorageDevices: dict[str, StorageDevice.Base.StorageDeviceABC] = dict()


def Initialize(ConfigFolderPath: str):
    global _IsHALInit
    _IsHALInit = True

    global Backends
    Backends = Backend.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Backend.yaml"))

    global Carriers
    Carriers = Carrier.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Carrier.yaml"))

    global Labwares
    Labwares = Labware.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Labware.yaml"))

    global TransportDevices
    TransportDevices = TransportDevice.Loader.LoadYaml(
        Backends,
        Labwares,
        os.path.join(ConfigFolderPath, "Transport.yaml"),
    )

    global DeckLocations
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

    global ClosedContainerDevices
    ClosedContainerDevices = ClosedContainer.Loader.LoadYaml(
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

    TipDevices = Tip.Loader.LoadYaml(
        Backends,
        os.path.join(ConfigFolderPath, "Tip.yaml"),
    )

    global PipetteDevices
    PipetteDevices = Pipette.Loader.LoadYaml(
        Backends,
        DeckLocations,
        Labwares,
        TipDevices,
        os.path.join(ConfigFolderPath, "Pipette.yaml"),
    )

    global StorageDevices
    StorageDevices = StorageDevice.Loader.LoadYaml(
        LayoutItems,
        os.path.join(ConfigFolderPath, "Storage.yaml"),
    )
