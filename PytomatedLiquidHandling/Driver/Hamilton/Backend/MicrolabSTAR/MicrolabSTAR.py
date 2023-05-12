from ....Tools.AbstractClasses import BackendABC


class MicrolabSTAR(BackendABC):
    def __init__(self, InstrumentIPAddress: str, InstrumentPort: int):
        ...
