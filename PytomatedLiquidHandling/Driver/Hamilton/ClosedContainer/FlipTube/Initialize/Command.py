from ....Backend import HamiltonCommandABC


@HamiltonCommandABC.Decorator_Command(__file__)
class Command(HamiltonCommandABC):
    def __init__(self, *, CustomErrorHandling: bool, Identifier: str = "None"):
        HamiltonCommandABC.__init__(self, Identifier, CustomErrorHandling)

    def HandleErrors(self):
        ...
