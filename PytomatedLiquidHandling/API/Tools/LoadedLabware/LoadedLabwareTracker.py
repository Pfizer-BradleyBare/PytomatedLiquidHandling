from typing import Self

from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from ..Container.BaseContainer import Container
from .LoadedLabware import LoadedLabware


class LoadedLabwareTracker(UniqueObjectTrackerABC[LoadedLabware]):
    def GetLabwareAssignments(self, ContainerInstance: Container) -> Self:

        ReturnLoadedLabwareTrackerInstance = LoadedLabwareTracker()
        # We need to keep in mind that there is a very slim possibility that
        # Container can be loaded in 2 different physical labware. We may prevent
        # this entirely but it is good to support here

        from ...Handler import GetHandler

        HandlerInstance = GetHandler()
        LoadedLabwareTrackerInstance = HandlerInstance.LoadedLabwareTrackerInstance

        for LoadedLabwareInstance in LoadedLabwareTrackerInstance.GetObjectsAsList():

            for (
                WellAssignmentInstance
            ) in LoadedLabwareInstance.GetWellAssignmentTracker().GetObjectsAsList():
                if (
                    ContainerInstance.GetMethodName()
                    in WellAssignmentInstance.GetAssignment()
                    and ContainerInstance.GetName()
                    in WellAssignmentInstance.GetAssignment()
                ):
                    ReturnLoadedLabwareTrackerInstance.ManualLoad(LoadedLabwareInstance)
                    break

        return ReturnLoadedLabwareTrackerInstance
