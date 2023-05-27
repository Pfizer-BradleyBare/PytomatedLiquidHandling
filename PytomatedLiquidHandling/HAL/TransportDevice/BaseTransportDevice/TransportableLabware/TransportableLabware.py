from .....Tools.AbstractClasses import UniqueObjectABC
from ....Labware.BaseLabware import LabwareABC
from .TransportParameters.TransportParameters import TransportParameters


class TransportableLabware(UniqueObjectABC):
    def __init__(
        self,
        LabwareInstance: LabwareABC,
        TransportParametersInstance: TransportParameters,
    ):
        UniqueObjectABC.__init__(self, LabwareInstance.GetUniqueIdentifier())
        self.LabwareInstance: LabwareABC = LabwareInstance
        self.TransportParametersInstance: TransportParameters = (
            TransportParametersInstance
        )
