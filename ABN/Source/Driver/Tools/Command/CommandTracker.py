from ....Tools.AbstractClasses import TrackerABC
from .Command import Command


class CommandTracker(TrackerABC[Command]):
    def ManualLoad(self, ObjectABCInstance: Command):
        if self.GetNumObjects() != 0:
            raise Exception(
                "Command Trackers can only have one object at a time. Please unload the current Command before trying to load another Command."
            )

        return super().ManualLoad(ObjectABCInstance)
