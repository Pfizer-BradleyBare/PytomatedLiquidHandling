from typing import Self

from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ....Tools.AbstractClasses import TrackerABC
from ..Labware.BaseLabware import Labware as APILabware
from .LoadedLabware import LoadedLabware


class LoadedLabwareTracker(TrackerABC[LoadedLabware]):
    def GetLabwareAssignments(self, APILabwareInstance: APILabware) -> Self:

        ReturnLoadedLabwareTrackerInstance = LoadedLabwareTracker()
        # We need to keep in mind that there is a very slim possibility that
        # APIlabware can be loaded in 2 different physical labware. We may prevent
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
                    APILabwareInstance.GetMethodName(), APILabwareInstance.GetName()
                ):
                    ReturnLoadedLabwareTrackerInstance.ManualLoad(LoadedLabwareInstance)
                    break

        return ReturnLoadedLabwareTrackerInstance
