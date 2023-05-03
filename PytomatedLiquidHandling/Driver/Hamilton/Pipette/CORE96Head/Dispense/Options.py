from enum import Enum

from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedMultiOptionsABC, AdvancedOptionsWrapper


class AdvancedOptions(AdvancedMultiOptionsABC):
    @AdvancedOptionsWrapper
    def __init__(self):
        AdvancedMultiOptionsABC.__init__(self)


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        SequencePosition: int,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.SequencePosition: int = SequencePosition

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
