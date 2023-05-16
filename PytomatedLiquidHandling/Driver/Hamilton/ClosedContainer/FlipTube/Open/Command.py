from ....Backend import HamiltonCommandABC
from .....Tools.AbstractClasses import CommandOptionsTracker
from .OptionsTracker import OptionsTracker


@HamiltonCommandABC.Decorator_Command(__file__)
class Command(HamiltonCommandABC, CommandOptionsTracker[OptionsTracker]):
    def __init__(
        self,
        *,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: OptionsTracker,
        Identifier: str = "None"
    ):
        HamiltonCommandABC.__init__(self, Identifier, CustomErrorHandling)
        CommandOptionsTracker.__init__(self, OptionsTrackerInstance)

    def HandleErrors(self):
        ...
