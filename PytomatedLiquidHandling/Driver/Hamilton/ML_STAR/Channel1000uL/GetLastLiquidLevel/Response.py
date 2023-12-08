from pydantic import dataclasses

from ....Backend import HamiltonBlockDataPackage, HamiltonResponseABC


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    ChannelLiquidLevels: HamiltonBlockDataPackage
