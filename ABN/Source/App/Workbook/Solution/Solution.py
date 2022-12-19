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
        self.ExcelInstance.SelectSheet("Solutions")
        return self.ExcelInstance.ReadCellValue(2, 2)

    def GetStorageTemp(self):
        self.ExcelInstance.SelectSheet("Solutions")
        return self.ExcelInstance.ReadCellValue(3, 2)

    def GetVolatility(self) -> SolutionPropertyValue:
        self.ExcelInstance.SelectSheet("Solutions")
        return "Volatility " + self.ExcelInstance.ReadCellValue(4, 2)

    def GetViscosity(self) -> SolutionPropertyValue:
        self.ExcelInstance.SelectSheet("Solutions")
        return "Viscosity " + self.ExcelInstance.ReadCellValue(5, 2)

    def GetHomogeneity(self) -> SolutionPropertyValue:
        self.ExcelInstance.SelectSheet("Solutions")
        return "Homogeneity " + self.ExcelInstance.ReadCellValue(6, 2)

    def GetLLD(self) -> SolutionPropertyValue:
        self.ExcelInstance.SelectSheet("Solutions")
        return "LLD " + self.ExcelInstance.ReadCellValue(7, 2)
