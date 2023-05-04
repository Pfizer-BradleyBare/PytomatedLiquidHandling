from abc import ABC

# This is an abstract loader class for loading configuration files


class UniqueObjectABC(ABC):
    """This is a unique object abstract base class.
    This class enables compatibility with the unique tracker.
    """

    def __init__(self, UniqueIdentifier: str | int):
        self.__UniqueObjectABC_Identifier: str | int = UniqueIdentifier

    def GetUniqueIdentifier(self) -> str | int:
        """This method guarentees a unique value as either a string or an int.
        This guarentee is required for the unique tracker.

        Returns:
            str | int: A unique value
        """
        return self.__UniqueObjectABC_Identifier
