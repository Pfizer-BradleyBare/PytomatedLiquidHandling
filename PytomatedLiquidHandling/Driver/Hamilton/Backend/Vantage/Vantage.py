from ....Tools.AbstractBackend import BackendABC


class Vantage(BackendABC):
    def __init__(self, InstrumentIPAddress: str, InstrumentPort: int):
        ...
