from .....Tools.AbstractClasses import ObjectABC
from ....Labware import Labware
from .TransportParameters.TransportParameters import TransportParameters


class TransportableLabware(ObjectABC):
    def __init__(
        self, LabwareInstance: Labware, TransportParametersInstance: TransportParameters
    ):
        self.LabwareInstance: Labware = LabwareInstance
        self.TransportParametersInstance: TransportParameters = (
            TransportParametersInstance
        )

    def GetName(self) -> str:
        return self.LabwareInstance.GetName()
