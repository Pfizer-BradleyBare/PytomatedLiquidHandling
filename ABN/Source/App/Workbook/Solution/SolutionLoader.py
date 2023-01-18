from ....API.Tools.Container.Reagent.ReagentTracker import ReagentTracker
from ...Tools.Container import Reagent
from ...Tools.Excel import Excel


def Load(SolutionName: str, MethodName: str, ExcelInstance: Excel) -> ReagentTracker:
    ReagentTrackerInstance: ReagentTracker = ReagentTracker()

    ExcelInstance.SelectSheet("Solutions")
    SolutionsSheet = ExcelInstance.ReadRangeValues(1, 1, 200, 50)

    MaxRows = len(SolutionsSheet)

    for ColIndex in range(1, 10, 4):
        for RowIndex in range(1, MaxRows, 8):
            Name = SolutionsSheet[RowIndex][ColIndex]
            if Name is None:
                break

            if " - (Click Here to Update)" not in Name:
                break

            Name = Name.replace(" - (Click Here to Update)", "")

            ReagentTrackerInstance.ManualLoad(
                Reagent(
                    Name,
                    MethodName,
                    ExcelInstance.ReadCellValue(RowIndex + 2, ColIndex + 2),
                    ExcelInstance,
                    RowIndex,
                    ColIndex,
                )
            )

    return ReagentTrackerInstance
