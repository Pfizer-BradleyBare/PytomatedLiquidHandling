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
        Sequence: str,
        ChannelNumber: int,
        SequencePosition: int,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions()
    ):
        self.ChannelNumber: int = ChannelNumber
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
