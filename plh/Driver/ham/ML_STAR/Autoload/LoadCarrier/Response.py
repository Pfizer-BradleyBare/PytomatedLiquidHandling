import dataclasses

from ....Backend import HamiltonBlockDataPackage, HamiltonResponseABC


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    RawCarrierRecoveryDetails: dataclasses.InitVar[str]
    RawLabwareRecoveryDetails: dataclasses.InitVar[str]

    CarrierRecoveryDetails: HamiltonBlockDataPackage = dataclasses.field(init=False)
    LabwareRecoveryDetails: HamiltonBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(
        self, RawCarrierRecoveryDetails: str, RawLabwareRecoveryDetails: str
    ) -> None:
        self.CarrierRecoveryDetails = HamiltonResponseABC.ParseHamiltonBlockData(
            RawCarrierRecoveryDetails
        )
        self.LabwareRecoveryDetails = HamiltonResponseABC.ParseHamiltonBlockData(
            RawLabwareRecoveryDetails
        )
        super().__post_init__()
