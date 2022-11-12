from ....Tools import Excel, ExcelOperator
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
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Solutions")
            return ExcelOperatorInstance.ReadCellValue(2, 2)

    def GetStorageTemp(self):
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Solutions")
            return ExcelOperatorInstance.ReadCellValue(3, 2)

    def GetVolatility(self) -> SolutionPropertyValue:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Solutions")
            return "Volatility " + ExcelOperatorInstance.ReadCellValue(4, 2)

    def GetViscosity(self) -> SolutionPropertyValue:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Solutions")
            return "Viscosity " + ExcelOperatorInstance.ReadCellValue(5, 2)

    def GetHomogeneity(self) -> SolutionPropertyValue:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Solutions")
            return "Homogeneity " + ExcelOperatorInstance.ReadCellValue(6, 2)

    def GetLLD(self) -> SolutionPropertyValue:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Solutions")
            return "LLD " + ExcelOperatorInstance.ReadCellValue(7, 2)
