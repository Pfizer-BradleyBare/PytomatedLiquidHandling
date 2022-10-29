from ..Container import Container, WellSolution


class ContainerCalculator:
    def __init__(self, ContainerInstance: Container):
        self.ContainerInstance: Container = ContainerInstance

    def AddVolumeToWell(self, WellNumber: int, WellSolutionInstance: WellSolution):
        pass

    def RemoveVolumeFromWell(self, WellNumber: int, Volume: float):
        pass
