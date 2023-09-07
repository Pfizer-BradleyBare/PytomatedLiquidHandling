import os
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import (
    Backend,
    Carrier,
    ClosedContainer,
    DeckLoader,
    DeckLocation,
    IMCSDesalting,
    Labware,
    LayoutItem,
    MagneticRack,
    Pipette,
    Storage,
    TempControlDevice,
    Tip,
    TransportDevice,
)
from PytomatedLiquidHandling.Tools.Logger import Logger


@dataclass
class HAL:
    ConfigFolderPath: str
    LoggerInstance: Logger
    Backends: dict[str, BackendABC] = field(init=False)
    Carriers: dict[str, Carrier.BaseCarrier.CarrierABC] = field(init=False)
    ClosedContainers: dict[
        str, ClosedContainer.BaseClosedContainer.ClosedContainerABC
    ] = field(init=False)
    DeckLoaders: dict[str, DeckLoader.BaseDeckLoader.DeckLoaderABC] = field(init=False)
    DeckLocations: dict[str, DeckLocation.BaseDeckLocation.DeckLocationABC] = field(
        init=False
    )
    IMCSDesaltings: dict[str, IMCSDesalting.BaseIMCSDesalting.IMCSDesaltingABC] = field(
        init=False
    )
    Labwares: dict[str, Labware.BaseLabware.LabwareABC] = field(init=False)
    LayoutItems: dict[str, LayoutItem.BaseLayoutItem.LayoutItemABC] = field(init=False)
    MagneticRacks: dict[str, MagneticRack.BaseMagneticRack.MagneticRackABC] = field(
        init=False
    )
    Pipettes: dict[str, Pipette.BasePipette.Pipette] = field(init=False)
    Storages: dict[str, Storage.BaseStorage.Storage] = field(init=False)
    TempControlDevices: dict[
        str, TempControlDevice.BaseTempControlDevice.TempControlDevice
    ] = field(init=False)
    Tips: dict[str, Tip.BaseTip.Tip] = field(init=False)
    TransportDevices: dict[
        str, TransportDevice.BaseTransportDevice.TransportDevice
    ] = field(init=False)

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

        self.DeckLocations = DeckLocation.Loader.LoadYaml(
            self.LoggerInstance,
            self.Carriers,
            os.path.join(self.ConfigFolderPath, "DeckLocation.yaml"),
        )

        self.TransportDevices = TransportDevice.Loader.LoadYaml(
            self.LoggerInstance,
            self.Backends,
            self.Labwares,
            self.DeckLocations,
            os.path.join(self.ConfigFolderPath, "Transport.yaml"),
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

        self.TempControlDevices = TempControlDevice.Loader.LoadYaml(
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

        self.Storages = Storage.Loader.LoadYaml(
            self.LoggerInstance,
            self.LayoutItems,
            os.path.join(self.ConfigFolderPath, "Storage.yaml"),
        )

        # self.IMCSDesaltingTrackerInstance
        # self.MagneticRackTrackerInstance
        # self.DeckLoaderInstance
