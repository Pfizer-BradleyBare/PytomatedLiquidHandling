from ....Tools import Excel
from ....Tools.AbstractClasses import ObjectABC
from .Value.Value import SolutionPropertyValue
from .Value.ValueTracker import SolutionPropertyValueTracker

SolutionPropertyValues = SolutionPropertyValueTracker()

SolutionPropertyValues.ManualLoad(SolutionPropertyValue("Volatility Low", 1, 0, 0))
SolutionPropertyValues.ManualLoad(SolutionPropertyValue("Volatility Medium", 1, 0, 0))
SolutionPropertyValues.ManualLoad(SolutionPropertyValue("Volatility High", 1, 0, 0))
SolutionPropertyValues.ManualLoad(
    SolutionPropertyValue("Volatility Very High", 1, 0, 0)
)

SolutionPropertyValues.ManualLoad(SolutionPropertyValue("Viscosity Low", 1, 0, 0))
SolutionPropertyValues.ManualLoad(SolutionPropertyValue("Viscosity Medium", 1, 0, 0))
SolutionPropertyValues.ManualLoad(SolutionPropertyValue("Viscosity High", 1, 0, 0))
SolutionPropertyValues.ManualLoad(SolutionPropertyValue("Viscosity Very High", 1, 0, 0))

SolutionPropertyValues.ManualLoad(
    SolutionPropertyValue("Homogeneity Homogenous", 1, 0, 0)
)
SolutionPropertyValues.ManualLoad(
    SolutionPropertyValue("Homogeneity Emulsion", 1, 0, 0)
)
SolutionPropertyValues.ManualLoad(
    SolutionPropertyValue("Homogeneity Suspension", 1, 0, 0)
)
SolutionPropertyValues.ManualLoad(
    SolutionPropertyValue("Homogeneity Heterogenous", 1, 0, 0)
)


SolutionPropertyValues.ManualLoad(SolutionPropertyValue("LLD Normal", 1, 0, 0))
SolutionPropertyValues.ManualLoad(SolutionPropertyValue("LLD Organic", 1, 0, 0))


class Solution(ObjectABC):
    def __init__(self, ExcelInstance: Excel, Name: str, Row: int, Col: int):
        self.ExcelInstance: Excel = ExcelInstance
        self.Name: str = Name
        self.Row: int = Row
        self.Col: int = Col

    def GetName(self) -> str:
        return self.Name

    def GetCategory(self):
        return self.ExcelInstance.ReadSolutionsSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetStorageTemp(self):
        return self.ExcelInstance.ReadSolutionsSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def GetVolatility(self) -> SolutionPropertyValue:
        return SolutionPropertyValues.GetObjectByName(
            "Volatility "
            + self.ExcelInstance.ReadSolutionsSheetArea(
                self.Row + 4, self.Col + 2, self.Row + 4, self.Col + 2
            )
        )

    def GetViscosity(self) -> SolutionPropertyValue:
        return SolutionPropertyValues.GetObjectByName(
            "Viscosity "
            + self.ExcelInstance.ReadSolutionsSheetArea(
                self.Row + 5, self.Col + 2, self.Row + 5, self.Col + 2
            )
        )

    def GetHomogeneity(self) -> SolutionPropertyValue:
        return SolutionPropertyValues.GetObjectByName(
            "Homogeneity "
            + self.ExcelInstance.ReadSolutionsSheetArea(
                self.Row + 6, self.Col + 2, self.Row + 6, self.Col + 2
            )
        )

    def GetLLD(self) -> SolutionPropertyValue:
        return SolutionPropertyValues.GetObjectByName(
            "LLD "
            + self.ExcelInstance.ReadSolutionsSheetArea(
                self.Row + 7, self.Col + 2, self.Row + 7, self.Col + 2
            )
        )
