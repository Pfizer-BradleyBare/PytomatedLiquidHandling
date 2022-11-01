class DriverABC:
    def __init__(self, SimulateState: bool):
        self.SimulateState: bool = SimulateState

    def GetSimulateState(self):
        return self.SimulateState
