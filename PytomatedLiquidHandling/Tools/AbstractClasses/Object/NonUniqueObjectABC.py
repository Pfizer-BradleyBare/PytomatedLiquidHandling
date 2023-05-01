from abc import ABC, abstractmethod

# This is an abstract loader class for loading configuration files


class NonUniqueObjectABC(ABC):
    """This is a non-unique object abstract base class.
    This class enables compatibility with the non-unique tracker.
    """

    def GetUniqueIdentifier(self) -> str | int:
        """This method does NOT guarentee a unique value. Instead, this values is used as a search handle

        Returns:
            str | int: A value
        """
        raise Exception(
            "GetName not overloaded for NonUniqueObject. Cannot use this method"
        )
