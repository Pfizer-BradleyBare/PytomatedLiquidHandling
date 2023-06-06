from abc import ABC
from dataclasses import dataclass

# This is an abstract loader class for loading configuration files


@dataclass
class UniqueObjectABC(ABC):
    """This is a unique object abstract base class.
    This class enables compatibility with the unique tracker.
    """

    UniqueIdentifier: str | int

    def GetUniqueIdentifier(self) -> str | int:
        """This method guarentees a unique value as either a string or an int.
        This guarentee is required for the unique tracker.

        Returns:
            str | int: A unique value
        """
        return self.UniqueIdentifier
