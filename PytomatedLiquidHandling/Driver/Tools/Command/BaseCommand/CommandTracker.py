from .....Tools.AbstractClasses import NonUniqueItemTrackerABC
from .Command import Command


class CommandTracker(NonUniqueItemTrackerABC[Command]):
    pass
    # def ManualLoad(self, ObjectABCInstance: Command):
    #    if self.GetNumObjects() != 0:
    #        raise Exception(
    #            "Command Trackers can only have one Command at a time. Please unload the current Command before trying to load another Command."
    #        )
    #
    #    super().ManualLoad(ObjectABCInstance)

    #    return
    # This was something from the past. Not sure if it is necessary yet...
