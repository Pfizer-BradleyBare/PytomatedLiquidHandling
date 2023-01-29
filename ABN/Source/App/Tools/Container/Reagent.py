from ....API.Tools.Container import Reagent as APIReagent
from ....API.Tools.Container.BaseContainer import LiquidClassCategory
from ....API.Tools.Container.Reagent.ReagentProperty import (
    HomogeneityReagentProperty,
    LLDReagentProperty,
    ViscosityReagentProperty,
    VolatilityReagentProperty,
)
from ..Excel import Excel


class Reagent(APIReagent):
    def __init__(
        self,
        Name: str,
        MethodName: str,
        PreferredLabware: str,
        ExcelInstance: Excel,
        Row: int,
        Col: int,
    ):
        APIReagent.__init__(
            self,
            Name,
            MethodName,
            VolatilityReagentProperty.Low,
            ViscosityReagentProperty.Low,
            HomogeneityReagentProperty.Homogenous,
            LLDReagentProperty.Normal,
        )  # This is a default value.

        self.Filter.append(PreferredLabware)

        self.PreferredLabware: str = PreferredLabware
        self.ExcelInstance: Excel = ExcelInstance
        self.Row: int = Row
        self.Col: int = Col

    def IsCorrectSolution(self) -> bool:
        return (
            self.ExcelInstance.ReadCellValue("Solutions", self.Row, self.Col)
            == self.Name
        )

    def GetLiquidClassCategory(self) -> LiquidClassCategory:

        return LiquidClassCategory(
            VolatilityReagentProperty(
                self.ExcelInstance.ReadCellValue(
                    "Solutions", self.Row + 3, self.Col + 1
                )
            ),
            ViscosityReagentProperty(
                self.ExcelInstance.ReadCellValue(
                    "Solutions", self.Row + 4, self.Col + 1
                )
            ),
            HomogeneityReagentProperty(
                self.ExcelInstance.ReadCellValue(
                    "Solutions", self.Row + 5, self.Col + 1
                )
            ),
            LLDReagentProperty(
                self.ExcelInstance.ReadCellValue(
                    "Solutions", self.Row + 6, self.Col + 1
                )
            ),
        )
