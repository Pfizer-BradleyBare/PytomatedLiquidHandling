class SolutionPropertyValue:
    NumericValue = 1

    def __init__(
        self,
        Weight: int,
        MinAspirateMix: int,
        MinDispenseMix: int,
    ):
        self.Weight: int = Weight
        self.NumericValue: int = SolutionPropertyValue.NumericValue
        self.MinAspirateMix: int = MinAspirateMix
        self.MinDispenseMix: int = MinDispenseMix

        SolutionPropertyValue.NumericValue += 1

    def GetWeight(self) -> int:
        return self.Weight

    def GetNumericValue(self) -> int:
        return self.NumericValue

    def GetMinAspirateMix(self) -> int:
        return self.MinAspirateMix

    def GetMinDispenseMix(self) -> int:
        return self.MinDispenseMix
