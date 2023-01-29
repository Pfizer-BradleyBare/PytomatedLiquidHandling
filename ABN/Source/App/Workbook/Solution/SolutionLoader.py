from ....API.Tools.Container.Reagent.ReagentTracker import ReagentTracker
from ...Tools.Container import Reagent
from ...Tools.Excel import Excel
from ..Worklist import Worklist


def Load(
    MethodName: str, ExcelInstance: Excel, WorklistInstance: Worklist
) -> ReagentTracker:
    ReagentTrackerInstance: ReagentTracker = ReagentTracker()

    SolutionsSheet = ExcelInstance.ReadRangeValues("Solutions", 1, 1, 200, 50)

    MaxRows = len(SolutionsSheet)

    for ColIndex in range(1, 10, 4):
        for RowIndex in range(1, MaxRows, 8):
            Name = SolutionsSheet[RowIndex][ColIndex]
            if Name is None:
                break

            Name = str(Name)

            if " - (Click Here to Update)" not in Name:
                break

            Name = Name.replace(" - (Click Here to Update)", "")

            if WorklistInstance.IsWorklistColumn(Name) is True:
                Names = set(WorklistInstance.ReadWorklistColumn(Name))
            else:
                Names = set([Name])
            # If we have a worklist column then that means the actual name is not a solution. We need to deal with that

            for Name in Names:
                ReagentTrackerInstance.ManualLoad(
                    Reagent(
                        str(Name),
                        MethodName,
                        str(
                            ExcelInstance.ReadCellValue(
                                "Solutions", RowIndex + 2, ColIndex + 2
                            )
                        ),
                        ExcelInstance,
                        RowIndex + 1,
                        ColIndex + 1,
                    )
                )

    return ReagentTrackerInstance
