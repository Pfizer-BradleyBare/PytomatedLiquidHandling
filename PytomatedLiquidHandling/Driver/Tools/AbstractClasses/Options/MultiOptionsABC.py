from ..AdvancedOptions import AdvancedMultiOptionsABC
from .....Tools.AbstractClasses import NonUniqueObjectABC


class MultiOptionsABC(NonUniqueObjectABC):
    def __init__(
        self, Identifier: str | int, AdvancedOptionsInstance: AdvancedMultiOptionsABC
    ):
        self.AdvancedOptionsInstance: AdvancedMultiOptionsABC = AdvancedOptionsInstance
        NonUniqueObjectABC.__init__(self, Identifier)
