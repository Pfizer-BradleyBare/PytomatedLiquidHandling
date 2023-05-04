from .....Tools.AbstractClasses import UniqueObjectABC
from ....Labware.BaseLabware import Labware
from .TransportParameters.TransportParameters import TransportParameters


class TransportableLabware(UniqueObjectABC):
    def __init__(
        self, LabwareInstance: Labware, TransportParametersInstance: TransportParameters
    ):
        UniqueObjectABC.__init__(self, LabwareInstance.GetUniqueIdentifier())
        self.LabwareInstance: Labware = LabwareInstance
        self.TransportParametersInstance: TransportParameters = (
            TransportParametersInstance
        )
