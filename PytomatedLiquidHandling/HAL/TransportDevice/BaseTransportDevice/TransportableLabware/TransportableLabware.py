from .....Tools.AbstractClasses import UniqueObjectABC
from ....Labware import Labware
from .TransportParameters.TransportParameters import TransportParameters


class TransportableLabware(UniqueObjectABC):
    def __init__(
        self, LabwareInstance: Labware, TransportParametersInstance: TransportParameters
    ):
        self.LabwareInstance: Labware = LabwareInstance
        self.TransportParametersInstance: TransportParameters = (
            TransportParametersInstance
        )

    def GetName(self) -> str:
        return self.LabwareInstance.GetName()
