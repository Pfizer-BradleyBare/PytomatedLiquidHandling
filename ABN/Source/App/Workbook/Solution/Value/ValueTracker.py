from .....Tools.AbstractClasses import TrackerABC
from .Value import SolutionPropertyValue


class SolutionPropertyValueTracker(TrackerABC[SolutionPropertyValue]):
    def GetObjectByNumericValue(self, NumericValue: int) -> SolutionPropertyValue:  # type: ignore

        ReturnSolution: SolutionPropertyValue | None
        ReturnSolution = None

        for Object in self.GetObjectsAsList():
            if Object.GetNumericValue() == NumericValue:
                ReturnSolution = Object

        if ReturnSolution is None:
            raise Exception(
                "SolutionPropertyValueTracker - "
                + str(NumericValue)
                + " is not tracked."
            )

        return ReturnSolution
