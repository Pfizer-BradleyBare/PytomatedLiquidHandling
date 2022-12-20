from ......Tools.AbstractClasses import TrackerABC
from .WellAssignment import WellAssignment


class WellAssignmentTracker(TrackerABC[WellAssignment]):
    def GetObjectByName(
        self, MethodName: str, SampleNumber: int, SampleDescription: str
    ) -> WellAssignment:
        return super().GetObjectByName(
            MethodName + " - " + str(SampleNumber) + ":" + SampleDescription
        )

    def IsTracked(
        self, MethodName: str, SampleNumber: int, SampleDescription: str
    ) -> bool:
        return super().IsTracked(
            MethodName + " - " + str(SampleNumber) + ":" + SampleDescription
        )
