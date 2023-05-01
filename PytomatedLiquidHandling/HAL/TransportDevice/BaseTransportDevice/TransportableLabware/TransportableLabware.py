from .....Tools.AbstractClasses import UniqueObjectABC
from ....Labware.BaseLabware import Labware
from .TransportParameters.TransportParameters import TransportParameters


class TransportableLabware(UniqueObjectABC):
    def __init__(
        self, LabwareInstance: Labware, TransportParametersInstance: TransportParameters
    ):
        self.LabwareInstance: Labware = LabwareInstance
        self.TransportParametersInstance: TransportParameters = (
            TransportParametersInstance
        )

    def GetUniqueIdentifier(self) -> str:
        return self.LabwareInstance.GetUniqueIdentifier()
