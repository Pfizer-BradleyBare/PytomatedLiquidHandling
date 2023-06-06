from .....Tools.AbstractClasses import UniqueObjectABC
from ....Labware.BaseLabware import LabwareABC
from .TransportParameters.TransportParameters import TransportParameters
from dataclasses import dataclass, field


@dataclass
class TransportableLabware(UniqueObjectABC):
    UniqueIdentifier: str | int = field(init=False)
    LabwareInstance: LabwareABC
    TransportParametersInstance: TransportParameters

    def __post_init__(self):
        self.UniqueIdentifier = self.LabwareInstance.UniqueIdentifier
