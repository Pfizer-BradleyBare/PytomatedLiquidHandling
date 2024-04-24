import dataclasses

from plh.device.HAMILTON.backend import HamiltonBlockDataPackage, HamiltonResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    RawChannelLiquidLevels: dataclasses.InitVar[str]
    ChannelLiquidLevels: HamiltonBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(self, RawChannelLiquidLevels: str) -> None:
        self.ChannelLiquidLevels = HamiltonResponseBase.parse_block_data(
            RawChannelLiquidLevels,
        )
        super().__post_init__()
