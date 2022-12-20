from typing import Self

from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ....Tools.AbstractClasses import TrackerABC
from ..Labware.BaseLabware import Labware as APILabware
from .LoadedLabware import LoadedLabware


class LoadedLabwareTracker(TrackerABC[LoadedLabware]):
    def GetLabwareAssignments(
        self, MethodName: str, APILabwareInstance: APILabware
    ) -> Self:

        ReturnLoadedLabwareTrackerInstance = LoadedLabwareTracker()

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
                    MethodName, APILabwareInstance.GetName()
                ):
                    ReturnLoadedLabwareTrackerInstance.ManualLoad(LoadedLabwareInstance)
                    break

        return ReturnLoadedLabwareTrackerInstance
