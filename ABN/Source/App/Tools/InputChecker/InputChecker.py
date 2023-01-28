from ....API.Tools import Validator
from ...Workbook import Workbook


def CheckAndConvertItem(
    WorkbookInstance: Workbook,
    Input: object,
    TypeCriterias: list[type],
    ValCriterias: list[object],
) -> any:  # type:ignore

    if Validator.ValidateInput(Input, TypeCriterias, ValCriterias):
        return Input
    else:
        raise Exception("TODO")


def CheckAndConvertList(
    WorkbookInstance: Workbook,
    Input: object,
    TypeCriterias: list[type],
    ValCriterias: list[object],
    Checks: list[bool],
) -> any:  # type:ignore

    if Validator.ValidateInput(Input, [str]):
        if WorkbookInstance.WorklistInstance.IsWorklistColumn(str(Input)):
            Input = WorkbookInstance.WorklistInstance.ReadWorklistColumn(str(Input))

        else:
            Input = WorkbookInstance.WorklistInstance.ConvertToWorklistColumn(Input)

    else:
        Input = WorkbookInstance.WorklistInstance.ConvertToWorklistColumn(Input)

    ValidateList = [Input for Input, Check in zip(Input, Checks) if Check is True]

    if not Validator.ValidateListInput(ValidateList, TypeCriterias, ValCriterias):
        raise Exception("TODO")
    else:
        return Input
