from .....Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .Command import Command


class CommandTracker(NonUniqueObjectTrackerABC[Command]):
    def ManualLoad(self, NonUniqueObjectABCInstance: Command):
        if self.GetNumObjects() != 0:
            raise Exception(
                "Command Trackers can only have one Command at a time. Please unload the current Command before trying to load another Command."
            )

        super().ManualLoad(NonUniqueObjectABCInstance)

        return
