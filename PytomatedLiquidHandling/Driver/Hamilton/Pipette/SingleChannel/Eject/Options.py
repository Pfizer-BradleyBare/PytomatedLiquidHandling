from enum import Enum

from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedMultiOptionsABC


class AdvancedOptions(AdvancedMultiOptionsABC):
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

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions()
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
