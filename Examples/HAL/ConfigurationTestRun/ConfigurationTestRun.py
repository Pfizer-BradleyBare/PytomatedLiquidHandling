import os

import yaml

from PytomatedLiquidHandling import HAL

with open(os.path.join(os.path.dirname(__file__), "Carrier.yaml")) as File:
    Dict = yaml.full_load(File)

HAL.Carrier.Load(Dict)
