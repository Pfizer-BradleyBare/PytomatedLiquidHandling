from abc import ABC

# This is an abstract loader class for loading configuration files


class NonUniqueObjectABC(ABC):
    """This is a non-unique object abstract base class.
    This class enables compatibility with the non-unique tracker.
    """

    def __init__(self, Identifier: str | int):
        self.__NonUniqueObjectABC_Identifier: str | int = Identifier

    def GetIdentifier(self) -> str | int:
        """This method does NOT guarentee a unique value. Instead, this values is used as a search handle

        Returns:
            str | int: An identifier
        """
        return self.__NonUniqueObjectABC_Identifier
