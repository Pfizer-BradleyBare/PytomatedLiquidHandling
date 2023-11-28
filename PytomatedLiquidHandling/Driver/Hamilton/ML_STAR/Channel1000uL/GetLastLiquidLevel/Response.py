from dataclasses import dataclass

from ....Backend import HamiltonBlockDataPackage, HamiltonResponseABC


class Response(HamiltonResponseABC):
    ChannelLiquidLevels: HamiltonBlockDataPackage
