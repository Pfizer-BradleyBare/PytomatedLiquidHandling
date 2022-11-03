from .....AbstractClasses import TrackerABC
from .Value import SolutionPropertyValue


class SolutionPropertyValueTracker(TrackerABC[SolutionPropertyValue]):
    def GetObjectByNumericValue(self, NumericValue: int) -> SolutionPropertyValue:  # type: ignore

        for Object in self.GetObjectsAsList():
            if Object.GetNumericValue() == NumericValue:
                return Object
