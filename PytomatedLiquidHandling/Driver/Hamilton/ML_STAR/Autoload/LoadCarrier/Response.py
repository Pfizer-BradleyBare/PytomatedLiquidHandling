from dataclasses import dataclass

from ....Backend import HamiltonBlockDataPackage, HamiltonResponseABC


class Response(HamiltonResponseABC):
    CarrierRecoveryDetails: HamiltonBlockDataPackage
    LabwareRecoveryDetails: HamiltonBlockDataPackage
