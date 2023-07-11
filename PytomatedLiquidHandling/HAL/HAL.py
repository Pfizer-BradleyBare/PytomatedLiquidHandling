import os
from dataclasses import dataclass, field

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
    BackendTrackerInstance: Backend.BackendTracker = field(init=False)
    CarrierTrackerInstance: Carrier.CarrierTracker = field(init=False)
    ClosedContainerTrackerInstance: ClosedContainer.ClosedContainerTracker = field(
        init=False
    )
    DeckLoaderInstance: DeckLoader.BaseDeckLoader.DeckLoaderABC = field(init=False)
    DeckLocationTrackerInstance: DeckLocation.DeckLocationTracker = field(init=False)
    IMCSDesaltingTrackerInstance: IMCSDesalting.IMCSDesaltingTracker = field(init=False)
    LabwareTrackerInstance: Labware.LabwareTracker = field(init=False)
    LayoutItemTrackerInstance: LayoutItem.LayoutItemTracker = field(init=False)
    MagneticRackTrackerInstance: MagneticRack.MagneticRackTracker = field(init=False)
    PipetteTrackerInstance: Pipette.PipetteTracker = field(init=False)
    StorageTrackerInstance: Storage.StorageTracker = field(init=False)
    TempControlDeviceTrackerInstance: TempControlDevice.TempControlDeviceTracker = (
        field(init=False)
    )
    TipTrackerInstance: Tip.TipTracker = field(init=False)
    TransportDeviceTrackerInstance: TransportDevice.TransportDeviceTracker = field(
        init=False
    )

    def __post_init__(self):
        self.BackendTrackerInstance = Backend.Loader.LoadYaml(
            self.LoggerInstance,
            os.path.join(self.ConfigFolderPath, "Backend.yaml"),
        )

        self.CarrierTrackerInstance = Carrier.Loader.LoadYaml(
            os.path.join(self.ConfigFolderPath, "Carrier.yaml")
        )

        self.LabwareTrackerInstance = Labware.Loader.LoadYaml(
            os.path.join(self.ConfigFolderPath, "Labware.yaml")
        )

        self.DeckLocationTrackerInstance = DeckLocation.Loader.LoadYaml(
            self.CarrierTrackerInstance,
            os.path.join(self.ConfigFolderPath, "DeckLocation.yaml"),
        )

        self.TransportDeviceTrackerInstance = TransportDevice.Loader.LoadYaml(
            self.BackendTrackerInstance,
            self.LabwareTrackerInstance,
            self.DeckLocationTrackerInstance,
            os.path.join(self.ConfigFolderPath, "Transport.yaml"),
        )

        self.LayoutItemTrackerInstance = LayoutItem.Loader.LoadYaml(
            self.LabwareTrackerInstance,
            self.DeckLocationTrackerInstance,
            os.path.join(self.ConfigFolderPath, "LayoutItem.yaml"),
        )

        self.ClosedContainerTrackerInstance = ClosedContainer.Loader.LoadYaml(
            self.BackendTrackerInstance,
            self.DeckLocationTrackerInstance,
            self.LabwareTrackerInstance,
            os.path.join(self.ConfigFolderPath, "ClosedContainer.yaml"),
        )

        self.TempControlDeviceTrackerInstance = TempControlDevice.Loader.LoadYaml(
            self.BackendTrackerInstance,
            self.LayoutItemTrackerInstance,
            os.path.join(self.ConfigFolderPath, "TempControlDevice.yaml"),
        )

        self.TipTrackerInstance = Tip.Loader.LoadYaml(
            self.BackendTrackerInstance,
            os.path.join(self.ConfigFolderPath, "Tip.yaml"),
        )

        self.PipetteTrackerInstance = Pipette.Loader.LoadYaml(
            self.BackendTrackerInstance,
            self.DeckLocationTrackerInstance,
            self.LabwareTrackerInstance,
            self.TipTrackerInstance,
            os.path.join(self.ConfigFolderPath, "Pipette.yaml"),
        )

        self.StorageTrackerInstance = Storage.Loader.LoadYaml(
            self.LayoutItemTrackerInstance,
            os.path.join(self.ConfigFolderPath, "Storage.yaml"),
        )

        # self.IMCSDesaltingTrackerInstance
        # self.MagneticRackTrackerInstance
        # self.DeckLoaderInstance
