from .SolutionTracker import SolutionTracker
from .Solution import Solution
from ....Tools import Excel, ExcelOperator


def Load(SolutionTrackerInstance: SolutionTracker, ExcelInstance: Excel):
    with ExcelOperator(False, ExcelInstance) as ExcelOperatorInstance:
        ExcelOperatorInstance.SelectSheet("Solutions")
        SolutionsSheet = ExcelOperatorInstance.ReadRangeValues(1, 1, 200, 50)

    MaxRows = len(SolutionsSheet)

    for ColIndex in range(1, 10, 4):
        for RowIndex in range(1, MaxRows, 8):
            Name = SolutionsSheet[RowIndex][ColIndex]
            if Name is None:
                break

            if " - (Click Here to Update)" not in Name:
                break

            Name = Name.replace(" - (Click Here to Update)", "")

            SolutionTrackerInstance.ManualLoad(
                Solution(ExcelInstance, Name, RowIndex, ColIndex)
            )
