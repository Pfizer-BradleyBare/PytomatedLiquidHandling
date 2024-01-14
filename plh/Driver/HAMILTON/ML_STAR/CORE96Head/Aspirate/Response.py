import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBlockDataPackage, HamiltonResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    RawRecoveryDetails: dataclasses.InitVar[str]
    RecoveryDetails: HamiltonBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(self, RawRecoveryDetails: str) -> None:
        self.RecoveryDetails = HamiltonResponseBase.parse_block_data(
            RawRecoveryDetails,
        )
        super().__post_init__()
