from .....Tools.AbstractClasses import ObjectABC


class DeinitializeOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        TipSequence: str,
        GeneratedWasteSequence: str,
        TransportDevice: int,
        GripperSequence: str,
        IPGParkLocation: int,
    ):

        self.Name: str = Name

        self.TipSequence: str = TipSequence

        self.GeneratedWasteSequence: str = GeneratedWasteSequence

        self.TransportDevice: int = TransportDevice
        self.GripperSequence: str = GripperSequence
        self.IPGParkLocation: int = IPGParkLocation

    def GetName(self) -> str:
        return self.Name
