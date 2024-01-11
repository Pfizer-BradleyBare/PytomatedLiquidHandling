import os

import yaml

from PytomatedLiquidHandling import HAL

with open(os.path.join(os.path.dirname(__file__), "Carrier.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict, HAL.Carrier.Base.CarrierABC, HAL.Carrier.Devices
)


with open(os.path.join(os.path.dirname(__file__), "Backend.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.Devices(Dict, HAL.Backend.Base.BackendABC, HAL.Backend.Devices)

with open(os.path.join(os.path.dirname(__file__), "Labware.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict, HAL.Labware.Base.LabwareABC, HAL.Labware.Devices
)

with open(os.path.join(os.path.dirname(__file__), "Transport.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.Devices(
    Dict, HAL.TransportDevice.Base.TransportABC, HAL.TransportDevice.Devices
)

with open(os.path.join(os.path.dirname(__file__), "Tip.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(Dict, HAL.Tip.Base.TipABC, HAL.Tip.Devices)


with open(os.path.join(os.path.dirname(__file__), "DeckLocation.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict, HAL.DeckLocation.Base.DeckLocationABC, HAL.DeckLocation.Devices
)

with open(os.path.join(os.path.dirname(__file__), "LayoutItem.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict, HAL.LayoutItem.Base.LayoutItemABC, HAL.LayoutItem.Devices
)

with open(os.path.join(os.path.dirname(__file__), "ClosedContainer.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict, HAL.ClosedContainer.Base.ClosedContainerABC, HAL.ClosedContainer.Devices
)

with open(os.path.join(os.path.dirname(__file__), "HeatCoolShakeDevice.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict,
    HAL.HeatCoolShakeDevice.Base.HeatCoolShakeABC,
    HAL.HeatCoolShakeDevice.Devices,
)

with open(os.path.join(os.path.dirname(__file__), "Pipette.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict, HAL.Pipette.Base.PipetteABC, HAL.Pipette.Devices
)

with open(os.path.join(os.path.dirname(__file__), "StorageDevice.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict, HAL.StorageDevice.Base.StorageDeviceABC, HAL.StorageDevice.Devices
)
