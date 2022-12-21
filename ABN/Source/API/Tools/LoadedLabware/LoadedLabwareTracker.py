from typing import Self

from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ....Tools.AbstractClasses import TrackerABC
from ..Container.BaseContainer import Container
from .LoadedLabware import LoadedLabware


class LoadedLabwareTracker(TrackerABC[LoadedLabware]):
    def GetLabwareAssignments(self, ContainerInstance: Container) -> Self:

        ReturnLoadedLabwareTrackerInstance = LoadedLabwareTracker()
        # We need to keep in mind that there is a very slim possibility that
        # Container can be loaded in 2 different physical labware. We may prevent
        # this entirely but it is good to support here

        LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
            HandlerRegistry.GetObjectByName(
                "API"
            ).LoadedLabwareTrackerInstance  # type:ignore
        )

        for LoadedLabwareInstance in LoadedLabwareTrackerInstance.GetObjectsAsList():

            for (
                WellAssignmentInstance
            ) in LoadedLabwareInstance.GetWellAssignmentTracker().GetObjectsAsList():
                if WellAssignmentInstance.TestAsignment(
                    ContainerInstance.GetMethodName(), ContainerInstance.GetName()
                ):
                    ReturnLoadedLabwareTrackerInstance.ManualLoad(LoadedLabwareInstance)
                    break

        return ReturnLoadedLabwareTrackerInstance
