from typing import Generic, TypeVar, cast, get_args

from PytomatedLiquidHandling.API.Tools import Validator

from ...Workbook import Workbook
from .BaseBlockParameter import BlockParameter

T = TypeVar("T", bound="int | float | str")


class List(BlockParameter, Generic[T]):
    def Read(
        self,
        WorkbookInstance: Workbook,
    ) -> list[T]:  # type:ignore

        Value = WorkbookInstance.ExcelInstance.ReadCellValue(
            self.ExcelSheet, self.Row, self.Col
        )

        if WorkbookInstance.WorklistInstance.IsWorklistColumn(str(Value)):
            Value = WorkbookInstance.WorklistInstance.ReadWorklistColumn(str(Value))

        else:
            Value = WorkbookInstance.WorklistInstance.ConvertToWorklistColumn(Value)

        Checks = [
            bool(Factor.GetFactor())
            for Factor in WorkbookInstance.GetContextTracker()
            .GetObjectByName(self.BlockInstance.GetContext())
            .GetWellFactorTracker()
            .GetObjectsAsList()
        ]
        ValidateList = [Value for Value, Check in zip(Value, Checks) if Check is True]
        # Basically, we only validate the value if the factor is non-zero

        if not Validator.ValidateListInput(
            ValidateList,
            get_args(self.__orig_class__)[0],  # type:ignore
            # NOTE this is clever as hell way to get the type info from the generic class. Bad form, so beware
            self.ValCriterias,
        ):
            raise Exception("TODO")
        else:
            return cast(list[T], Value)

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
