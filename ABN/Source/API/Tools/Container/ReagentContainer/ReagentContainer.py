from ..Container import Container, ContainerTypes


class ReagentContainer(Container):
    def __init__(self, Name: str):
        Container.__init__(self, Name, ContainerTypes.Reagent)
        self.UsedVolume: int = 0

    def GetUsedVolume(self) -> int:
        return self.UsedVolume
