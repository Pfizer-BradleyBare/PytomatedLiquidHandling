import os

import yaml

from PytomatedLiquidHandling import HAL, Driver


class Test(Driver.Hamilton.Backend.HamiltonResponseABC):
    T: Driver.Hamilton.Backend.HamiltonResponse.HamiltonBlockDataPackage


Test(
    ErrorDescription="",
    T="1[01,05,00,2,Barcode01,car24_cup15x100_0001,1[02,20,00,2,Barcode02,car24_cup15x100_0001,2[03,00,00,0,Barcode03,car24_cup15x100_0001,3[04,00,00,0,Barcode04,car24_cup15x100_0001,4[05,00,00,0,Barcode05,car24_cup15x100_0001,5[06,00,00,0,Barcode06,car24_cup15x100_0001,6",
)

quit()

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
    Dict, HAL.Transport.Base.TransportABC, HAL.Transport.Devices
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
    HAL.HeatCoolShake.Base.HeatCoolShakeABC,
    HAL.HeatCoolShake.Devices,
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

with open(os.path.join(os.path.dirname(__file__), "MagneticRack.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.DevicesLists(
    Dict, HAL.MagneticRack.Base.MagneticRackABC, HAL.MagneticRack.Devices
)
