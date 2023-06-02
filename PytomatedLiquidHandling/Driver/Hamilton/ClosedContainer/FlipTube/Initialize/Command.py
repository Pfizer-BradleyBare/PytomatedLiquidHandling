from ....Backend import HamiltonActionCommandABC


@HamiltonActionCommandABC.Decorator_Command(__file__)
class Command(HamiltonActionCommandABC):
    def __init__(self, *, CustomErrorHandling: bool, Identifier: str = "None"):
        HamiltonActionCommandABC.__init__(self, Identifier, CustomErrorHandling)

    def ParseResponseThrowExceptions(
        self, ResponseInstance: HamiltonActionCommandABC.Response
    ):
        ...
