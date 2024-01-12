import dataclasses

from ....Backend import HamiltonBlockDataPackage, HamiltonResponseABC


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    RawRecoveryDetails: dataclasses.InitVar[str]
    RecoveryDetails: HamiltonBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(self, RawRecoveryDetails: str) -> None:
        self.RecoveryDetails = HamiltonResponseABC.ParseHamiltonBlockData(
            RawRecoveryDetails
        )
        super().__post_init__()
