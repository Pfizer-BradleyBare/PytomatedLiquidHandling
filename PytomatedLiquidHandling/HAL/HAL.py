import os
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import (
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
from PytomatedLiquidHandling.Tools.Logger import Logger


@dataclass
class HAL:
    ConfigFolderPath: str
    LoggerInstance: Logger
    Backends: dict[str, BackendABC] = field(init=False)
    Carriers: dict[str, Carrier.Base.CarrierABC] = field(init=False)
    ClosedContainers: dict[str, ClosedContainer.Base.ClosedContainerABC] = field(
        init=False
    )
    DeckLoaders: dict[str, DeckLoader.Base.DeckLoaderABC] = field(init=False)
    DeckLocations: dict[str, DeckLocation.Base.DeckLocationABC] = field(init=False)
    # IMCSDesaltings: dict[str, IMCSDesalting.Base.IMCSDesaltingABC] = field(init=False)
    Labwares: dict[str, Labware.Base.LabwareABC] = field(init=False)
    LayoutItems: dict[str, LayoutItem.Base.LayoutItemABC] = field(init=False)
    MagneticRacks: dict[str, MagneticRack.Base.MagneticRackABC] = field(init=False)
    Pipettes: dict[str, Pipette.Base.PipetteABC] = field(init=False)
    StorageDevices: dict[str, StorageDevice.Base.StorageDeviceABC] = field(init=False)
    TempControlDevices: dict[
        str, HeatCoolShakeDevice.Base.HeatCoolShakeDeviceABC
    ] = field(init=False)
    Tips: dict[str, Tip.Base.TipABC] = field(init=False)
    TransportDevices: dict[str, TransportDevice.Base.TransportDeviceABC] = field(
        init=False
    )

    def __post_init__(self):
        self.Backends = Backend.Loader.LoadYaml(
            self.LoggerInstance,
            os.path.join(self.ConfigFolderPath, "Backend.yaml"),
        )

        self.Carriers = Carrier.Loader.LoadYaml(
            self.LoggerInstance, os.path.join(self.ConfigFolderPath, "Carrier.yaml")
        )

        self.Labwares = Labware.Loader.LoadYaml(
            self.LoggerInstance, os.path.join(self.ConfigFolderPath, "Labware.yaml")
        )

        self.TransportDevices = TransportDevice.Loader.LoadYaml(
            self.LoggerInstance,
            self.Backends,
            self.Labwares,
            os.path.join(self.ConfigFolderPath, "Transport.yaml"),
        )

        self.DeckLocations = DeckLocation.Loader.LoadYaml(
            self.LoggerInstance,
            self.Carriers,
            self.TransportDevices,
            os.path.join(self.ConfigFolderPath, "DeckLocation.yaml"),
        )

        self.LayoutItems = LayoutItem.Loader.LoadYaml(
            self.LoggerInstance,
            self.Labwares,
            self.DeckLocations,
            os.path.join(self.ConfigFolderPath, "LayoutItem.yaml"),
        )

        self.ClosedContainers = ClosedContainer.Loader.LoadYaml(
            self.LoggerInstance,
            self.Backends,
            self.DeckLocations,
            self.Labwares,
            os.path.join(self.ConfigFolderPath, "ClosedContainer.yaml"),
        )

        self.TempControlDevices = HeatCoolShakeDevice.Loader.LoadYaml(
            self.LoggerInstance,
            self.Backends,
            self.LayoutItems,
            os.path.join(self.ConfigFolderPath, "TempControlDevice.yaml"),
        )

        self.Tips = Tip.Loader.LoadYaml(
            self.LoggerInstance,
            self.Backends,
            os.path.join(self.ConfigFolderPath, "Tip.yaml"),
        )

        self.Pipettes = Pipette.Loader.LoadYaml(
            self.LoggerInstance,
            self.Backends,
            self.DeckLocations,
            self.Labwares,
            self.Tips,
            os.path.join(self.ConfigFolderPath, "Pipette.yaml"),
        )

        self.StorageDevices = StorageDevice.Loader.LoadYaml(
            self.LoggerInstance,
            self.LayoutItems,
            os.path.join(self.ConfigFolderPath, "Storage.yaml"),
        )

        # self.IMCSDesaltingTrackerInstance
        # self.MagneticRackTrackerInstance
        # self.DeckLoaderInstance
