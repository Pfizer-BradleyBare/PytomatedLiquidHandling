import dataclasses

from plh.device.hamilton_venus.backend import (
    HamiltonBlockDataPackage,
    HamiltonResponseBase,
)


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    RawCarrierRecoveryDetails: dataclasses.InitVar[str]
    RawLabwareRecoveryDetails: dataclasses.InitVar[str]

    CarrierRecoveryDetails: HamiltonBlockDataPackage = dataclasses.field(init=False)
    LabwareRecoveryDetails: HamiltonBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(
        self,
        RawCarrierRecoveryDetails: str,
        RawLabwareRecoveryDetails: str,
    ) -> None:
        self.CarrierRecoveryDetails = HamiltonResponseBase.parse_block_data(
            RawCarrierRecoveryDetails,
        )
        self.LabwareRecoveryDetails = HamiltonResponseBase.parse_block_data(
            RawLabwareRecoveryDetails,
        )
        super().__post_init__()
