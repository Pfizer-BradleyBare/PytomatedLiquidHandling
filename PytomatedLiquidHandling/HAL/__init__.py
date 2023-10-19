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


__Backends: dict[str, Backend.Base.BackendABC]


def GetBackends() -> dict[str, Backend.Base.BackendABC]:
    global __Backends
    if _IsHALInit:
        return __Backends
    else:
        raise RuntimeError(
            "Backends do not exist yet. Did you call the Initialize method first?"
        )


__Carriers: dict[str, Carrier.Base.CarrierABC]


def GetCarriers() -> dict[str, Carrier.Base.CarrierABC]:
    global __Carriers
    if _IsHALInit:
        return __Carriers
    else:
        raise RuntimeError(
            "Carriers do not exist yet. Did you call the Initialize method first?"
        )


__Labwares: dict[str, Labware.Base.LabwareABC]


def GetLabwares() -> dict[str, Labware.Base.LabwareABC]:
    global __Labwares
    if _IsHALInit:
        return __Labwares
    else:
        raise RuntimeError(
            "Labwares do not exist yet. Did you call the Initialize method first?"
        )


__TransportDevices: dict[str, TransportDevice.Base.TransportDeviceABC]


def GetTransportDevices() -> dict[str, TransportDevice.Base.TransportDeviceABC]:
    global __TransportDevices
    if _IsHALInit:
        return __TransportDevices
    else:
        raise RuntimeError(
            "TransportDevices do not exist yet. Did you call the Initialize method first?"
        )


__DeckLocations: dict[str, DeckLocation.Base.DeckLocationABC]


def GetDeckLocations() -> dict[str, DeckLocation.Base.DeckLocationABC]:
    global __DeckLocations
    if _IsHALInit:
        return __DeckLocations
    else:
        raise RuntimeError(
            "DeckLocations do not exist yet. Did you call the Initialize method first?"
        )


__LayoutItems: dict[str, LayoutItem.Base.LayoutItemABC]


def GetLayoutItems() -> dict[str, LayoutItem.Base.LayoutItemABC]:
    global __LayoutItems
    if _IsHALInit:
        return __LayoutItems
    else:
        raise RuntimeError(
            "LayoutItems do not exist yet. Did you call the Initialize method first?"
        )


__ClosedContainers: dict[str, ClosedContainer.Base.ClosedContainerABC]


def GetClosedContainers() -> dict[str, ClosedContainer.Base.ClosedContainerABC]:
    global __ClosedContainers
    if _IsHALInit:
        return __ClosedContainers
    else:
        raise RuntimeError(
            "ClosedContainers do not exist yet. Did you call the Initialize method first?"
        )


__HeatCoolShakeDevices: dict[str, HeatCoolShakeDevice.Base.HeatCoolShakeDeviceABC]


def GetHeatCoolShakeDevices() -> (
    dict[str, HeatCoolShakeDevice.Base.HeatCoolShakeDeviceABC]
):
    global __HeatCoolShakeDevices
    if _IsHALInit:
        return __HeatCoolShakeDevices
    else:
        raise RuntimeError(
            "HeatCoolShakeDevices do not exist yet. Did you call the Initialize method first?"
        )


__Pipettes: dict[str, Pipette.Base.PipetteABC]


def GetPipettes() -> dict[str, Pipette.Base.PipetteABC]:
    global __Pipettes
    if _IsHALInit:
        return __Pipettes
    else:
        raise RuntimeError(
            "Pipettes do not exist yet. Did you call the Initialize method first?"
        )


__StorageDevices: dict[str, StorageDevice.Base.StorageDeviceABC]


def GetStorageDevices() -> dict[str, StorageDevice.Base.StorageDeviceABC]:
    global __StorageDevices
    if _IsHALInit:
        return __StorageDevices
    else:
        raise RuntimeError(
            "StorageDevices do not exist yet. Did you call the Initialize method first?"
        )


_IsHALInit: bool = False


def Initialize(ConfigFolderPath: str):
    global _IsHALInit
    _IsHALInit = True

    global __Backends
    __Backends = Backend.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Backend.yaml"))

    global __Carriers
    __Carriers = Carrier.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Carrier.yaml"))

    global __Labwares
    __Labwares = Labware.Loader.LoadYaml(os.path.join(ConfigFolderPath, "Labware.yaml"))

    global __TransportDevices
    __TransportDevices = TransportDevice.Loader.LoadYaml(
        __Backends,
        __Labwares,
        os.path.join(ConfigFolderPath, "Transport.yaml"),
    )

    global __DeckLocations
    __DeckLocations = DeckLocation.Loader.LoadYaml(
        __Carriers,
        __TransportDevices,
        os.path.join(ConfigFolderPath, "DeckLocation.yaml"),
    )

    global __LayoutItems
    __LayoutItems = LayoutItem.Loader.LoadYaml(
        __Labwares,
        __DeckLocations,
        os.path.join(ConfigFolderPath, "LayoutItem.yaml"),
    )

    global __ClosedContainers
    __ClosedContainers = ClosedContainer.Loader.LoadYaml(
        __Backends,
        __DeckLocations,
        __Labwares,
        os.path.join(ConfigFolderPath, "ClosedContainer.yaml"),
    )

    global __HeatCoolShakeDevices
    __HeatCoolShakeDevices = HeatCoolShakeDevice.Loader.LoadYaml(
        __Backends,
        __LayoutItems,
        os.path.join(ConfigFolderPath, "TempControlDevice.yaml"),
    )

    __TipDevices = Tip.Loader.LoadYaml(
        __Backends,
        os.path.join(ConfigFolderPath, "Tip.yaml"),
    )

    global __Pipettes
    __Pipettes = Pipette.Loader.LoadYaml(
        __Backends,
        __DeckLocations,
        __Labwares,
        __TipDevices,
        os.path.join(ConfigFolderPath, "Pipette.yaml"),
    )

    global __StorageDevices
    __StorageDevices = StorageDevice.Loader.LoadYaml(
        __LayoutItems,
        os.path.join(ConfigFolderPath, "Storage.yaml"),
    )
