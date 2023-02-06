from typing import Generic, TypeVar, cast, get_args

from PytomatedLiquidHandling.API.Tools import Validator

from ...Workbook import Workbook
from .BaseBlockParameter import BlockParameter

T = TypeVar("T", bound="int | float | str")


class Item(BlockParameter, Generic[T]):
    def Read(
        self,
        WorkbookInstance: Workbook,
    ) -> T:  # type:ignore

        Value = WorkbookInstance.ExcelInstance.ReadCellValue(
            self.ExcelSheet, self.Row, self.Col
        )

        if WorkbookInstance.WorklistInstance.IsWorklistColumn(str(Value)):
            raise Exception("TODO")

        if Validator.ValidateInput(
            Value,
            get_args(self.__orig_class__)[0],  # type:ignore
            # NOTE this is clever as hell way to get the type info from the generic class. Bad form, so beware
            self.ValCriterias,
        ):
            return cast(T, Value)
        else:
            raise Exception("TODO")
