from typing import cast

from ....API.Tools import Validator
from ...Workbook import Block, Workbook


def CheckAndConvertItem(
    WorkbookInstance: Workbook,
    BlockInstance: Block,
    Input: object,
    TypeCriterias: list[type],
    ValCriterias: list,
) -> any:  # type:ignore

    if WorkbookInstance.WorklistInstance.IsWorklistColumn(str(Input)):
        raise Exception("TODO")

    if Validator.ValidateInput(Input, TypeCriterias, ValCriterias):
        return Input
    else:
        raise Exception("TODO")


def CheckAndConvertList(
    WorkbookInstance: Workbook,
    BlockInstance: Block,
    Input: object,
    TypeCriterias: list[type],
    ValCriterias: list,
) -> list[any]:  # type:ignore

    if WorkbookInstance.WorklistInstance.IsWorklistColumn(str(Input)):
        Input = WorkbookInstance.WorklistInstance.ReadWorklistColumn(str(Input))

    else:
        Input = WorkbookInstance.WorklistInstance.ConvertToWorklistColumn(Input)

    Checks = [
        bool(Factor.GetFactor())
        for Factor in WorkbookInstance.GetContextTracker()
        .GetObjectByName(BlockInstance.GetContext())
        .GetWellFactorTracker()
        .GetObjectsAsList()
    ]

    ValidateList = [Input for Input, Check in zip(Input, Checks) if Check is True]

    if not Validator.ValidateListInput(ValidateList, TypeCriterias, ValCriterias):
        raise Exception("TODO")
    else:
        return Input

    # OLD Implementation Below
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
