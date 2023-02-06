from abc import ABC, abstractmethod

from ....Workbook import Block, Workbook


class BlockParameter(ABC):
    def __init__(
        self,
        BlockInstance: Block,
        RowOffset: int,
        ValCriterias: list = list(),
    ):
        self.BlockInstance: Block = BlockInstance

        self.ExcelSheet: str = "Method"
        self.Row: int = BlockInstance.Row + RowOffset
        self.Col: int = BlockInstance.Col + 1

        self.ValCriterias: list = ValCriterias

    @abstractmethod
    def Read(self, WorkbookInstance: Workbook) -> any:  # type:ignore
        ...
