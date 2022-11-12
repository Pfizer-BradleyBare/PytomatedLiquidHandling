class Excel:
    def __init__(self, ExcelFilePath: str):
        self.ExcelFilePath: str = ExcelFilePath

    def GetExcelFilePath(self) -> str:
        return self.ExcelFilePath
