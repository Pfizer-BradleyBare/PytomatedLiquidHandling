from ....Tools import Excel
from ....AbstractClasses import ObjectABC


class Solution(ObjectABC):
    def __init__(self, ExcelInstance: Excel, Name: str, Row: int, Col: int):
        self.ExcelInstance: Excel = ExcelInstance
        self.Name: str = Name
        self.Row: int = Row
        self.Col: int = Col

    def GetName(self) -> str:
        return self.Name

    def GetCoordinates(self) -> tuple[int, int]:
        return self.Coordinates

    def GetCategory(self):
        return self.ExcelInstance.ReadSolutionsSheet()[self.Row + 1][self.Col + 1]

    def GetStorageTemp(self):
        return self.ExcelInstance.ReadSolutionsSheet()[self.Row + 2][self.Col + 1]

    def GetVolatility(self):
        return self.ExcelInstance.ReadSolutionsSheet()[self.Row + 3][self.Col + 1]

    def GetViscosity(self):
        return self.ExcelInstance.ReadSolutionsSheet()[self.Row + 4][self.Col + 1]

    def GetHomogeneity(self):
        return self.ExcelInstance.ReadSolutionsSheet()[self.Row + 5][self.Col + 1]

    def GetLLD(self):
        return self.ExcelInstance.ReadSolutionsSheet()[self.Row + 6][self.Col + 1]
