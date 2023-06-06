from abc import ABC
from dataclasses import dataclass

# This is an abstract loader class for loading configuration files


@dataclass
class NonUniqueObjectABC(ABC):
    """This is a non-unique object abstract base class.
    This class enables compatibility with the non-unique tracker.
    """

    Identifier: str | int

    def GetIdentifier(self) -> str | int:
        """This method does NOT guarentee a unique value. Instead, this values is used as a search handle

        Returns:
            str | int: An identifier
        """
        return self.Identifier
