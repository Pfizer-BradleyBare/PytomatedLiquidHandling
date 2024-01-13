import dataclasses

from ....Backend import HamiltonBlockDataPackage, HamiltonResponseABC


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    RawChannelLiquidLevels: dataclasses.InitVar[str]
    ChannelLiquidLevels: HamiltonBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(self, RawChannelLiquidLevels: str) -> None:
        self.ChannelLiquidLevels = HamiltonResponseABC.ParseHamiltonBlockData(
            RawChannelLiquidLevels
        )
        super().__post_init__()
