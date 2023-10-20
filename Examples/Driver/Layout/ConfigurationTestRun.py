import os

import yaml

from PytomatedLiquidHandling import HAL

with open(os.path.join(os.path.dirname(__file__), "Carrier.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.ObjectsLists(
    Dict, HAL.Carrier.Base.CarrierABC, HAL.Carrier.GetObjects()
)


with open(os.path.join(os.path.dirname(__file__), "Backend.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Backend.Load(Dict)

with open(os.path.join(os.path.dirname(__file__), "Labware.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.ObjectsLists(
    Dict, HAL.Labware.Base.LabwareABC, HAL.Labware.GetObjects()
)

with open(os.path.join(os.path.dirname(__file__), "Transport.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.Objects(
    Dict, HAL.TransportDevice.Base.TransportDeviceABC, HAL.TransportDevice.GetObjects()
)

with open(os.path.join(os.path.dirname(__file__), "Tip.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.ObjectsLists(Dict, HAL.Tip.Base.TipABC, HAL.Tip.GetObjects())


with open(os.path.join(os.path.dirname(__file__), "DeckLocation.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.ObjectsLists(
    Dict, HAL.DeckLocation.Base.DeckLocationABC, HAL.DeckLocation.GetObjects()
)

with open(os.path.join(os.path.dirname(__file__), "LayoutItem.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.ObjectsLists(
    Dict, HAL.LayoutItem.Base.LayoutItemABC, HAL.LayoutItem.GetObjects()
)

with open(os.path.join(os.path.dirname(__file__), "ClosedContainer.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tools.ConfigLoader.ObjectsLists(
    Dict, HAL.ClosedContainer.Base.ClosedContainerABC, HAL.ClosedContainer.GetObjects()
)
