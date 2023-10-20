import os

import yaml

from PytomatedLiquidHandling import HAL

with open(os.path.join(os.path.dirname(__file__), "Carrier.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Carrier.Load(Dict)

with open(os.path.join(os.path.dirname(__file__), "Backend.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Backend.Load(Dict)

with open(os.path.join(os.path.dirname(__file__), "Labware.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Labware.Load(Dict)

with open(os.path.join(os.path.dirname(__file__), "Transport.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.TransportDevice.Load(Dict)

with open(os.path.join(os.path.dirname(__file__), "Tip.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Tip.Load(Dict)

with open(os.path.join(os.path.dirname(__file__), "LayoutItem.yaml")) as File:
    Dict = yaml.full_load(File)

# HAL.LayoutItem.Load(Dict)

with open(os.path.join(os.path.dirname(__file__), "DeckLocation.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.DeckLocation.Load(Dict)
