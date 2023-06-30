from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import Labware

from .....Tools.AbstractClasses import UniqueObjectABC
from .TransportParameters.TransportParameters import TransportParameters


@dataclass
class TransportableLabware(UniqueObjectABC):
    UniqueIdentifier: str | int = field(init=False)
    LabwareInstance: Labware.BaseLabware.LabwareABC
    TransportParametersInstance: TransportParameters

    def __post_init__(self):
        self.UniqueIdentifier = self.LabwareInstance.UniqueIdentifier
